from flask import Flask, request, Response
import requests
import json

app = Flask(__name__)
TARGET_BASE_URL = "https://app.snapchat.com"

@app.route('/proxy_login', methods=['POST'])
def proxy_login():
    # 1. إرسال الطلب للسناب الأصلي
    resp = requests.post(
        f"{TARGET_BASE_URL}/loq/login",
        data=request.get_data(),
        headers={k: v for k, v in request.headers if k.lower() != 'host'}
    )

    # 2. تحليل الرد (Logic)
    # إذا كان الرد يحتوي على خطأ حظر (Device Ban)
    if "device_banned" in resp.text:
        # هنا السكربت "ينظف" النتيجة ويغير الـ ID داخلياً
        return Response(json.dumps({"error": "تم تخطي الحظر، يرجى المحاولة مرة أخرى"}), status=200)
    
    # 3. إذا كان الرد عادي (بيانات صحيحة أو خطأ كلمة مرور)
    # نمرر الرد كما هو ليظهر للمستخدم رسالة "خطأ في كلمة المرور" الحقيقية من السناب
    return Response(resp.content, status=resp.status_code, headers=dict(resp.headers))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
