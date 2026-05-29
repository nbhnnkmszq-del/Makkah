from flask import Flask, request, Response
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
app = Flask(__name__)

# هذا المسار يمسك طلبات تسجيل الدخول فقط
@app.route('/proxy_login', methods=['POST'])
def proxy_login():
    target_url = "https://app.snapchat.com/loq/login"
    resp = requests.post(target_url, data=request.get_data(), headers={k:v for k,v in request.headers if k.lower()!='host'}, verify=False)
    return Response(resp.content, status=resp.status_code, headers=dict(resp.headers))

# هذا المسار يمسك أي "خربطة" ثانية ويرجعها للسناب الأصلي فوراً عشان ما تطلع 404
@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def catch_all(path):
    target_url = f"https://app.snapchat.com/{path}"
    resp = requests.request(method=request.method, url=target_url, data=request.get_data(), headers={k:v for k,v in request.headers if k.lower()!='host'}, verify=False)
    return Response(resp.content, status=resp.status_code, headers=dict(resp.headers))

if __name__ == '__main__':
    import os
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
