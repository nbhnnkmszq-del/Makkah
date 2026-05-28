from flask import Flask, request, Response
import requests

app = Flask(__name__)

# المسار الذي يرسل له السناب طلباته
@app.route('/proxy_login', methods=['POST'])
def handle_snap_login():
    # الرابط المستهدف الحقيقي
    target_url = "https://app.snapchat.com/loq/login"
    
    # نقل الهيدرات مع تعديل الـ Host
    headers = {k: v for k, v in request.headers if k.lower() != 'host'}
    headers['Host'] = 'app.snapchat.com'
    
    try:
        resp = requests.post(
            target_url,
            data=request.get_data(),
            headers=headers,
            verify=False
        )
        return Response(resp.content, status=resp.status_code, headers=dict(resp.headers))
    except Exception as e:
        return str(e), 500

# مسار إضافي ليتجنب الـ 404 عند فحص السيرفر
@app.route('/', methods=['GET'])
def home():
    return "Proxy is running", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
