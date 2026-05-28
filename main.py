from flask import Flask, request, Response
import requests

app = Flask(__name__)

# هذا المسار يطابق تماماً ما يرسله تطبيق السناب
@app.route('/proxy_login', methods=['POST'])
def proxy_login():
    try:
        # إرسال الطلب للسناب الأصلي
        resp = requests.post(
            "https://app.snapchat.com/loq/login",
            data=request.get_data(),
            headers={k: v for k, v in request.headers if k.lower() != 'host'},
            verify=False
        )
        return Response(resp.content, status=resp.status_code, headers=dict(resp.headers))
    except Exception as e:
        return str(e), 500

# مسار لجعل السيرفر يظهر كـ "Active"
@app.route('/', methods=['GET', 'HEAD'])
def index():
    return "Proxy Active", 200

if __name__ == '__main__':
    app.run()
