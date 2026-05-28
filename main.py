from flask import Flask, request, Response
import requests
import urllib3

# إيقاف تحذيرات الشهادات لضمان عدم حدوث أخطاء في الاتصال
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

app = Flask(__name__)

TARGET_URL = "https://app.snapchat.com/loq/login"

@app.route('/proxy_login', methods=['POST'])
def proxy_login():
    # 1. تنظيف الهيدرات (إزالة أي بصمة للسيرفر أو التعديل)
    # نمرر هيدرات الجهاز الأصلية فقط
    headers = {
        'User-Agent': request.headers.get('User-Agent', 'Snapchat/12.80.0'),
        'X-Snapchat-Device-ID': request.headers.get('X-Snapchat-Device-ID'),
        'Content-Type': 'application/x-protobuf',
        'Accept': '*/*'
    }
    
    # 2. إرسال الطلب للسناب الأصلي
    try:
        resp = requests.post(
            TARGET_URL,
            data=request.get_data(),
            headers=headers,
            verify=False,
            timeout=10
        )
        
        # 3. إرجاع الرد للسناب (Buffer نظيف)
        return Response(
            resp.content,
            status=resp.status_code,
            headers={'Content-Type': 'application/x-protobuf'}
        )
        
    except Exception as e:
        # في حال حدوث خطأ، نرجع 500 عشان السناب ما يكرش
        return Response(status=500)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
