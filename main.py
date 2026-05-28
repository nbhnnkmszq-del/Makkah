from flask import Flask, request, Response
import requests
import uuid
import warnings
from urllib3.exceptions import InsecureRequestWarning

warnings.simplefilter('ignore', InsecureRequestWarning)
app = Flask(__name__)

# قائمة المسارات الأساسية التي يستخدمها السناب في تسجيل الدخول والعمليات
SNAP_ROUTES = [
    '/api/loq/login',
    '/api/loq/registration',
    '/api/loq/upload',
    '/api/loq/config',
    '/api/loq/device_token'
]

# تعريف المسارات بدقة
@app.route('/proxy_login', methods=['GET', 'POST'])
@app.route('/api/loq/<path:path>', methods=['GET', 'POST'])
def proxy_handler(path=''):
    # توجيه الطلب إلى سيرفر السناب الحقيقي
    target_url = f"https://app.snapchat.com{request.full_path.replace('/proxy_login', '')}"
    
    headers = {k: v for k, v in request.headers.items() if k.lower() not in ['host']}
    headers['Host'] = 'app.snapchat.com'
    headers['X-Snapchat-Device-ID'] = str(uuid.uuid4()) # تغيير الهوية لفك الحظر
    
    try:
        resp = requests.request(
            method=request.method,
            url=target_url,
            headers=headers,
            data=request.get_data(),
            params=request.args,
            verify=False,
            timeout=10
        )
        return Response(resp.content, resp.status_code, resp.headers.items())
    except Exception as e:
        return f"Proxy Error: {str(e)}", 502

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
