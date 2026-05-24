from flask import Flask, request, Response
import requests
import random

app = Flask(__name__)

# قائمة بمعرفات أجهزة وهمية (تحديث دوري لها يمنع الحظر)
DEVICE_IDS = ["331942", "442055", "882910", "119203"]

@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def proxy(path):
    # 1. تغيير هوية الجهاز عشوائياً لكل طلب
    new_device_id = random.choice(DEVICE_IDS)
    
    # 2. بناء الطلب الجديد
    target_url = f"https://app.snapchat.com/{path}"
    
    # 3. تعديل الهيدرز (هنا قلب التزوير)
    headers = {k: v for k, v in request.headers if k.lower() != 'host'}
    headers['Host'] = 'app.snapchat.com'
    headers['X-Snapchat-Device-ID'] = new_device_id # تزوير معرف الجهاز
    
    # 4. إرسال الطلب للسناب
    resp = requests.request(
        method=request.method,
        url=target_url,
        headers=headers,
        data=request.get_data(),
        params=request.args
    )
    return Response(resp.content, status=resp.status_code, headers=dict(resp.headers))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
