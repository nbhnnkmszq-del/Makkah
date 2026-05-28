from flask import Flask, request, Response
import requests

app = Flask(__name__)

# الإعدادات: السناب يثق بهذا السيرفر كأنه هو السيرفر الأصلي
TARGET_BASE_URL = "https://app.snapchat.com"

@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def proxy(path):
    # 1. إعداد الرابط الهدف
    url = f"{TARGET_BASE_URL}/{path}"
    
    # 2. تنظيف الهيدرات (إزالة بصمات التعديل)
    excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
    headers = {k: v for k, v in request.headers if k.lower() not in excluded_headers}
    
    # 3. إجبار السناب على استخدام هيدرات "نظيفة" (تخطي الحظر)
    headers['X-Snapchat-Device-ID'] = request.headers.get('X-Snapchat-Device-ID') # استخدم الـ ID اللي يرسله التويك
    
    # 4. توجيه الطلب للسناب الأصلي
    try:
        resp = requests.request(
            method=request.method,
            url=url,
            headers=headers,
            data=request.get_data(),
            cookies=request.cookies,
            allow_redirects=False,
            verify=False
        )
        
        # 5. تنظيف الرد (إزالة أي تحذيرات للسناب)
        response_headers = [(name, value) for (name, value) in resp.raw.headers.items() 
                            if name.lower() not in excluded_headers]
        
        return Response(resp.content, resp.status_code, response_headers)
        
    except Exception as e:
        return "Service Temporarily Unavailable", 503

if __name__ == '__main__':
    # تشغيل السيرفر
    app.run(host='0.0.0.0', port=10000)
