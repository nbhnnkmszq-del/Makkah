from flask import Flask, request, Response
import requests
import uuid
import logging

# تفعيل تسجيل الأحداث لمراقبة طلبات الدخول
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('MakkahProxy')

app = Flask(__name__)

# هذا المسار يضمن أن الرابط دائماً شغال ولا يعطي 404
@app.route('/proxy_login', methods=['GET', 'POST'])
def proxy_login():
    # 1. طباعة الطلب في اللوجز عشان نشوفه
    logger.info(f"Incoming Request from Device: {request.remote_addr}")
    
    # 2. الهيدرات اللي تخدع السناب وتفك الحظر
    headers = {
        'User-Agent': 'Snapchat/12.80.0 (iPhone14,2; iOS 15.5; scale=3.00)',
        'X-Snapchat-Device-ID': str(uuid.uuid4()), # فك الحظر اللحظي
        'X-Snapchat-App-Version': '12.80.0',
        'X-Snapchat-Platform': 'iOS',
    }
    
    # 3. توجيه الطلب للسناب
    target_url = "https://app.snapchat.com/api/loq/login"
    
    try:
        resp = requests.post(
            target_url,
            headers=headers,
            data=request.get_data(),
            verify=False,
            timeout=15
        )
        
        # 4. سجل الرد في اللوجز عشان نتأكد
        logger.info(f"Snapchat Response Code: {resp.status_code}")
        
        return Response(resp.content, resp.status_code, resp.headers.items())
    except Exception as e:
        logger.error(f"Proxy Error: {str(e)}")
        return "Proxy Error", 502

# مسار للتحقق أن الرابط "شغال" (Health Check)
@app.route('/', methods=['GET'])
def health():
    return "Makkah Proxy is READY for Login", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
