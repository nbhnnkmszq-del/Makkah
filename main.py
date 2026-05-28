from flask import Flask, request, Response
import requests
import uuid
import time

app = Flask(__name__)

# إعدادات ثابتة تحاكي إصداراً قديماً
TARGET_BASE_URL = "https://app.snapchat.com"
APP_VERSION = "12.80.0" 

def generate_spoof_headers(original_headers):
    """توليد هيدرات ديناميكية لكل طلب"""
    new_headers = {
        'User-Agent': f'Snapchat/{APP_VERSION} (iPhone14,2; iOS 15.5; scale=3.00)',
        'X-Snapchat-App-Version': APP_VERSION,
        'X-Snapchat-Device-ID': str(uuid.uuid4()), # هوية جديدة لكل طلب لتجاوز الحظر
        'X-Snapchat-Client-Auth': original_headers.get('X-Snapchat-Client-Auth', ''),
        'X-Snapchat-Device-Model': 'iPhone14,2',
        'X-Snapchat-Platform': 'iOS',
        'Accept-Language': 'en-US,en;q=0.9',
    }
    return new_headers

@app.route('/proxy_login', methods=['POST', 'GET'])
def proxy():
    # 1. استخراج المسار المطلوب من الهيدر (الذي أرسلناه من التويك)
    original_path = request.headers.get('X-Original-URL', '/api/loq/login')
    target_url = f"{TARGET_BASE_URL}{original_path}"

    # 2. توليد هيدرات نظيفة
    headers = generate_spoof_headers(request.headers)

    # 3. تعديل الـ Payload (إذا كان الطلب يحتوي على بيانات جهاز قديم)
    data = request.get_data()

    try:
        # إرسال الطلب للسناب
        resp = requests.request(
            method=request.method,
            url=target_url,
            headers=headers,
            data=data,
            verify=False,
            timeout=10
        )
        
        # 4. إرجاع الرد للسناب مع تنظيف الهيدرز
        excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection', 'x-frame-options']
        headers_to_return = {k: v for k, v in resp.headers.items() if k.lower() not in excluded_headers}
        
        return Response(resp.content, resp.status_code, headers_to_return)
        
    except Exception as e:
        return f"Proxy Error: {str(e)}", 502

if __name__ == '__main__':
    # تشغيل السيرفر بأداء عالي
    app.run(host='0.0.0.0', port=10000, threaded=True)
