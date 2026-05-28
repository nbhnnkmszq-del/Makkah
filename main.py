from flask import Flask, request, Response
import requests

app = Flask(__name__)

# الرابط الأصلي للسناب شات
SNAP_API = "https://app.snapchat.com"

@app.route('/proxy_login', methods=['POST'])
def proxy_login():
    # 1. تحديد الرابط الحقيقي الذي يحاول السناب الوصول إليه
    # ملاحظة: السناب يستخدم المسارات مثل /loq/login
    target_url = f"{SNAP_API}/loq/login"
    
    # 2. إعداد الهيدرات (إزالة Host لتجنب أخطاء السيرفر)
    headers = {key: value for key, value in request.headers if key != 'Host'}
    headers['Host'] = 'app.snapchat.com' # إجبار السناب على قبول الطلب
    
    # 3. تمرير الطلب كما هو للسناب شات
    try:
        resp = requests.post(
            target_url,
            data=request.get_data(),
            headers=headers,
            verify=False
        )
        
        # 4. إعادة الرد للسناب
        return Response(
            resp.content,
            status=resp.status_code,
            headers=dict(resp.headers)
        )
    except Exception as e:
        return Response(str(e), status=500)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
