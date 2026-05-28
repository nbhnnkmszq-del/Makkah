from flask import Flask, request, Response
import requests

app = Flask(__name__)

# هذا المسار سيلتقط أي طلب POST يرسله السناب، مهما كان المسار
@app.route('/', methods=['POST'])
@app.route('/proxy_login', methods=['POST'])
def proxy_all():
    target_url = "https://app.snapchat.com/loq/login"
    try:
        resp = requests.post(
            target_url,
            data=request.get_data(),
            headers={k: v for k, v in request.headers if k.lower() != 'host'},
            verify=False
        )
        return Response(resp.content, status=resp.status_code, headers=dict(resp.headers))
    except Exception as e:
        return str(e), 500

@app.route('/', methods=['GET'])
def index():
    return "Proxy Active", 200

if __name__ == '__main__':
    app.run(port=10000)
