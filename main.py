from flask import Flask, request, Response
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
app = Flask(__name__)

@app.route('/proxy_login', methods=['GET', 'POST'])
def proxy_login():
    # 1. وجه الطلب للسناب
    target_url = "https://app.snapchat.com/loq/login"
    
    # 2. فلترة الهيدرات (حذف الهيدرات اللي تسبب مشاكل)
    headers = {k: v for k, v in request.headers if k.lower() not in ['host', 'accept-encoding', 'content-length']}
    headers['Host'] = 'app.snapchat.com'
    
    # 3. إرسال الطلب
    try:
        resp = requests.request(
            method=request.method,
            url=target_url,
            data=request.get_data(),
            headers=headers,
            verify=False
        )
        return Response(resp.content, status=resp.status_code, headers=dict(resp.headers))
    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    # Render يعطيك البورت من متغير البيئة PORT
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
