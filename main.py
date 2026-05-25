from flask import Flask, request, Response
import requests

app = Flask(__name__)

# قائمة الهيدرز التي نريد استبدالها (التمويه)
SPOOF_HEADERS = {
    'User-Agent': 'Snapchat/13.20.0 (iPhone14,2; iOS 16.0; gzip)',
    'X-Snapchat-Client-ID': '00000000-0000-0000-0000-000000000000',
    'Connection': 'keep-alive'
}

@app.route('/proxy_login', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
def proxy():
    target_url = request.headers.get('X-Original-URL')
    if not target_url:
        return "Proxy Active", 200

    # 1. تجهيز الهيدرز للطلب المزور
    headers = {k: v for k, v in request.headers if k.lower() not in ['host', 'x-original-url']}
    headers.update(SPOOF_HEADERS)

    # 2. إرسال الطلب للسناب الأصلي
    try:
        resp = requests.request(
            method=request.method,
            url=target_url,
            headers=headers,
            data=request.get_data(),
            cookies=request.cookies,
            allow_redirects=False,
            timeout=10
        )
        
        # 3. إرجاع الرد للتويك
        return Response(resp.content, resp.status_code, dict(resp.headers))
    except Exception as e:
        return str(e), 502

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
