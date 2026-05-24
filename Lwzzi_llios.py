from flask import Flask, request, Response
import requests
import json
import base64

app = Flask(__name__)

@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def proxy(path):
    # 1. فك الهيدرز الأصلية القادمة من التويك
    encoded_headers = request.headers.get('X-Proxy-Headers')
    headers = {}
    if encoded_headers:
        try:
            headers = json.loads(base64.b64decode(encoded_headers))
        except:
            headers = dict(request.headers)
            
    # 2. تنظيف وتزوير الهيدرز
    headers['Host'] = 'app.snapchat.com'
    headers['X-Snapchat-Device-ID'] = '331942' # معرف جهاز ثابت ومجرب
    headers.pop('Host-Original', None) # إزالة أي بقايا
    
    # 3. إرسال الطلب للسناب الأصلي
    target_url = f"https://app.snapchat.com/{path}"
    
    try:
        resp = requests.request(
            method=request.method,
            url=target_url,
            headers=headers,
            data=request.get_data(),
            params=request.args,
            timeout=10
        )
        return Response(resp.content, status=resp.status_code, headers=dict(resp.headers))
    except Exception as e:
        return f"Error: {str(e)}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
