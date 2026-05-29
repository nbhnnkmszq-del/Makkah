from flask import Flask, request, Response
import requests

app = Flask(__name__)

# هذا الرابط هو الأصل لكل طلبات السناب
SNAP_BASE_URL = "https://app.snapchat.com"

@app.route('/<path:subpath>', methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'])
def proxy_handler(subpath):
    # 1. بناء الرابط الأصلي الذي يحاول السناب الوصول إليه
    target_url = f"{SNAP_BASE_URL}/{subpath}"
    
    # 2. تنظيف الهيدرات (إزالة الـ Host الخاص بسيرفرنا وتزويد هيدرات نظيفة)
    headers = {k: v for k, v in request.headers if k.lower() not in ['host', 'accept-encoding']}
    headers['Host'] = 'app.snapchat.com'
    headers['User-Agent'] = 'Snapchat/12.80.0.35 (iPhone14,2; iOS 16.5; Scale/3.00)'
    
    # 3. إرسال الطلب (مهما كان نوعه GET أو POST)
    try:
        resp = requests.request(
            method=request.method,
            url=target_url,
            data=request.get_data(),
            headers=headers,
            params=request.args,
            verify=False,
            timeout=10
        )
        
        # 4. إعادة الرد للسناب مع تنظيف هيدرات السيرفر الأصلي
        excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
        headers_to_return = {k: v for k, v in resp.headers.items() if k.lower() not in excluded_headers}
        
        return Response(resp.content, status=resp.status_code, headers=headers_to_return)
        
    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    # Railway يستخدم متغير البيئة PORT، إذا لم يوجد استخدم 8080
    import os
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
