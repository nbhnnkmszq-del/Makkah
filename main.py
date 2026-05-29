from flask import Flask, request, Response
import requests

app = Flask(__name__)

@app.route('/proxy_login', methods=['POST'])
def proxy_login():
    # هذا الكود هو اللي بيستقبل الطلب من التويك ويمرره للسناب
    target_url = "https://app.snapchat.com/loq/login"
    
    try:
        # إرسال الطلب للسناب الأصلي
        resp = requests.post(
            target_url, 
            data=request.get_data(), 
            headers={k: v for k, v in request.headers if k.lower() != 'host'},
            verify=False
        )
        # إرجاع رد السناب للتويك
        return Response(resp.content, status=resp.status_code, headers=dict(resp.headers))
    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000) # تأكد أن البورت هو 10000 في Render
