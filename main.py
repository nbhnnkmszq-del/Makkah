from flask import Flask, request, Response
import requests
import urllib3
import logging

# تعطيل تحذيرات SSL لأن السناب يستخدم شهادات معقدة
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
app = Flask(__name__)

# إعداد الـ Logger عشان نشوف الردود في لوحة تحكم Render
logging.basicConfig(level=logging.INFO)

@app.route('/proxy_login', methods=['POST'])
def proxy_login():
    try:
        # 1. الرد الفوري: نجهز الطلب للسناب الأصلي
        target_url = "https://app.snapchat.com/loq/login"
        
        # 2. تنظيف الهيدرات (هذه الخطوة تمنع تعليق السناب)
        headers = {k: v for k, v in request.headers if k.lower() not in ['host', 'accept-encoding', 'content-length']}
        headers['Host'] = 'app.snapchat.com'
        
        # 3. إرسال الطلب للسناب الحقيقي
        resp = requests.post(
            target_url,
            data=request.get_data(),
            headers=headers,
            verify=False,
            timeout=10 # لا تترك الطلب معلقاً أكثر من 10 ثوانٍ
        )
        
        # 4. الرد على التويك: نرسل له الـ Response الحقيقي من السناب
        return Response(
            resp.content, 
            status=resp.status_code, 
            headers={'Content-Type': 'application/x-protobuf'} # السناب يتوقع دائماً ردود بروتوفب
        )
        
    except Exception as e:
        logging.error(f"Error in proxy: {str(e)}")
        # رد 200 وهمي في حال فشل السيرفر عشان التويك ما يكرش السناب
        return Response(status=200)

if __name__ == '__main__':
    import os
    # استخدام البورت المخصص لـ Render
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
