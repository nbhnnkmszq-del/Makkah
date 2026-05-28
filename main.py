from flask import Flask, request, Response
import requests
import uuid
import warnings
from urllib3.exceptions import InsecureRequestWarning

warnings.simplefilter('ignore', InsecureRequestWarning)
app = Flask(__name__)

TARGET_BASE_URL = "https://app.snapchat.com"

@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def catch_all(path):
    # بناء الرابط الأصلي
    target_url = f"{TARGET_BASE_URL}/{path}"
    
    # تنظيف الهيدرات وتجهيز الهوية الجديدة
    headers = {k: v for k, v in request.headers.items() if k.lower() not in ['host', 'x-forwarded-for']}
    headers['X-Snapchat-Device-ID'] = str(uuid.uuid4()) # فك الحظر اللحظي
    headers['User-Agent'] = 'Snapchat/12.80.0 (iPhone14,2; iOS 15.5; scale=3.00)'
    
    try:
        # إرسال الطلب للسناب
        resp = requests.request(
            method=request.method,
            url=target_url,
            headers=headers,
            data=request.get_data(),
            params=request.args,
            verify=False,
            timeout=15
        )
        return Response(resp.content, resp.status_code, resp.headers.items())
    except Exception as e:
        return str(e), 502

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
