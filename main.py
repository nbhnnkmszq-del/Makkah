from flask import Flask, request, Response
import requests
import uuid

app = Flask(__name__)

# المحرك: إجبار السناب على رؤية السيرفر كجهاز iPhone 14 جديد دائماً
def forge_headers(headers):
    spoofed = {k: v for k, v in headers.items() if k.lower() not in ['host', 'x-snap-signature']}
    spoofed['User-Agent'] = 'Snapchat/12.80.0 (iPhone14,2; iOS 15.5; scale=3.00)'
    spoofed['X-Snapchat-Device-ID'] = str(uuid.uuid4()) # تغيير هوية الجهاز فوراً
    spoofed['X-Snapchat-Client-Auth'] = headers.get('X-Snapchat-Client-Auth', '')
    return spoofed

@app.route('/proxy_login', methods=['POST'])
def proxy():
    # توجيه الطلب الأصلي للسناب
    target_url = "https://app.snapchat.com" + request.headers.get('X-Original-URL', '/api/loq/login')
    
    # تحويل الطلب ببيانات "موهومة" (Spoofed)
    headers = forge_headers(request.headers)
    
    try:
        # إرسال الطلب بدون الاعتماد على توقيع الجهاز المحظور
        resp = requests.post(target_url, headers=headers, data=request.get_data(), verify=False)
        
        # إرجاع الرد للسناب كأنه طبيعي
        return Response(resp.content, resp.status_code, resp.headers.items())
    except Exception as e:
        return str(e), 502

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
