from flask import Flask, request, Response
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
app = Flask(__name__)

@app.route('/proxy_login', methods=['POST'])
def proxy_login():
    target_url = "https://app.snapchat.com/loq/login"
    
    # إرسال نفس البيانات للسناب الأصلي
    try:
        resp = requests.post(
            target_url,
            data=request.get_data(),
            headers={k: v for k, v in request.headers if k.lower() not in ['host', 'accept-encoding']},
            verify=False
        )
        # نرجع الرد اللي يجي من السناب للسناب (التطبيق)
        return Response(resp.content, status=resp.status_code, headers=dict(resp.headers))
    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    import os
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
