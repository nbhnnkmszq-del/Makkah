from flask import Flask, request, Response
import requests
import uuid
import warnings
from urllib3.exceptions import InsecureRequestWarning

# إخفاء تحذيرات HTTPS
warnings.simplefilter('ignore', InsecureRequestWarning)
app = Flask(__name__)

# هذا المسار الذي يطلبه السناب بالضبط
@app.route('/proxy_login', methods=['POST', 'GET', 'OPTIONS'])
def proxy_handler():
    # 1. السناب يحتاج التأكد أن السيرفر شغال (Handshake)
    if request.method == 'OPTIONS':
        return '', 200

    # 2. توجيه الطلب الأساسي للسناب
    target_url = "https://app.snapchat.com/api/loq/login"
    
    # 3. تجهيز الهيدرات "الموهومة"
    headers = {
        'User-Agent': 'Snapchat/12.80.0 (iPhone14,2; iOS 15.5; scale=3.00)',
        'X-Snapchat-App-Version': '12.80.0',
        'X-Snapchat-Device-ID': str(uuid.uuid4()), # تغيير الهوية لفك الحظر
        'Content-Type': 'application/x-protobuf',  # السناب يستخدم البروتوف
    }
    
    try:
        # تنفيذ الطلب
        resp = requests.post(
            target_url,
            headers=headers,
            data=request.get_data(),
            verify=False,
            timeout=10
        )
        
        # إرجاع الرد
        return Response(resp.content, resp.status_code, resp.headers.items())
    except Exception as e:
        return f"Proxy Error: {str(e)}", 502

# مسار إضافي للتأكد أن الرابط "شغال" (Health Check)
@app.route('/', methods=['GET'])
def health():
    return "Makkah Proxy is ACTIVE and RUNNING", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
