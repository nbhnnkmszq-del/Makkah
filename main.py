from flask import Flask, request, Response
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
app = Flask(__name__)

@app.route('/proxy_login', methods=['POST'])
def proxy_login():
    # الرابط الأصلي اللي السناب يكلمه
    target_url = "https://app.snapchat.com/loq/login"
    
    # 1. خذ البيانات (اليوزر والباسورد) اللي جات من السناب
    raw_data = request.get_data()
    
    # 2. انسخ الهيدرات من السناب شات
    headers = {k: v for k, v in request.headers if k.lower() != 'host'}
    headers['Host'] = 'app.snapchat.com'
    
    # 3. مرر الطلب للسناب
    resp = requests.post(target_url, data=raw_data, headers=headers, verify=False)
    
    # 4. أرجع الرد اللي يجي من السناب للتطبيق
    return Response(resp.content, status=resp.status_code, headers=dict(resp.headers))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
