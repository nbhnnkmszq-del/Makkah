from flask import Flask, request, Response
import requests
import uuid
import random

app = Flask(__name__)

# قائمة يوزرات وهمية (User-Agents) للتنويع
USER_AGENTS = [
    "Snapchat/12.80.0.35 (iPhone14,2; iOS 16.5; Scale/3.00)",
    "Snapchat/12.70.0.22 (iPhone13,4; iOS 15.6; Scale/3.00)",
    "Snapchat/12.85.0.10 (iPhone15,3; iOS 17.0; Scale/3.00)"
]

@app.route('/proxy_login', methods=['POST'])
def proxy_login():
    # 1. توليد بصمة جهاز جديدة
    new_device_id = str(uuid.uuid4())
    
    # 2. تنظيف وتجهيز الهيدرات
    headers = {
        'User-Agent': random.choice(USER_AGENTS),
        'X-Snapchat-Device-ID': new_device_id,
        'Content-Type': 'application/x-protobuf',
        'Accept': '*/*'
    }
    
    # 3. إرسال الطلب للسناب الأصلي
    target_url = "https://app.snapchat.com/loq/login"
    
    try:
        resp = requests.post(
            target_url,
            data=request.get_data(),
            headers=headers,
            verify=False
        )
        return Response(resp.content, status=resp.status_code, headers=dict(resp.headers))
    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    app.run(port=8080)
