from flask import Flask, request, Response
import requests
import os

app = Flask(__name__)

# مسار تجريبي للتأكد أن الموقع يعمل
@app.route('/', methods=['GET'])
def index():
    return "Proxy is running perfectly!", 200

# المسار الذي يستقبل أي طلب (POST أو GET) من السناب
@app.route('/<path:subpath>', methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'])
def proxy_handler(subpath):
    target_url = f"https://app.snapchat.com/{subpath}"
    
    # تنظيف الهيدرات
    headers = {k: v for k, v in request.headers if k.lower() not in ['host', 'accept-encoding']}
    headers['Host'] = 'app.snapchat.com'
    
    try:
        resp = requests.request(
            method=request.method,
            url=target_url,
            data=request.get_data(),
            headers=headers,
            params=request.args,
            verify=False
        )
        return Response(resp.content, status=resp.status_code, headers=dict(resp.headers))
    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
