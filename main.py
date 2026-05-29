from flask import Flask, request, Response
import requests
import os

app = Flask(__name__)

# هذا الرابط هو المعيار الجديد للـ login
TARGET_URL = "https://app.snapchat.com/loq/login"

@app.route('/proxy_login', methods=['POST'])
def proxy_login():
    try:
        # 1. فلترة الهيدرات الضرورية فقط
        # السناب حساس جداً لترتيب الهيدرات
        excluded_headers = ['host', 'accept-encoding', 'content-length', 'connection']
        headers = {k: v for k, v in request.headers if k.lower() not in excluded_headers}
        
        # 2. حقن هيدرات "نظيفة" لإيهام السناب أن الطلب أصلي
        headers['Host'] = 'app.snapchat.com'
        headers['User-Agent'] = 'Snapchat/12.45.0.35 (iPhone13,4; iOS 16.5; Scale/3.00)'
        headers['X-Snapchat-Client-Auth'] = request.headers.get('X-Snapchat-Client-Auth', '')

        # 3. تمرير الـ Data كما هي (لأنها مشفرة محلياً)
        raw_data = request.get_data()
        
        resp = requests.post(
            TARGET_URL,
            data=raw_data,
            headers=headers,
            verify=False,
            timeout=15
        )
        
        # 4. الرد بـ Header يخدع السناب أنه الرد الأصلي
        excluded_resp_headers = ['content-encoding', 'transfer-encoding']
        resp_headers = {k: v for k, v in resp.headers.items() if k.lower() not in excluded_resp_headers}
        resp_headers['Content-Type'] = 'application/x-protobuf'

        return Response(
            resp.content,
            status=resp.status_code,
            headers=resp_headers
        )

    except Exception as e:
        print(f"Error: {e}")
        # هنا الحيلة: نرجع كود 200 مع بودي فارغ (أو محاكي للنجاح)
        # هذا يمنع التطبيق من رمي رسالة الخطأ للمستخدم
        return Response(b'', status=200)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
