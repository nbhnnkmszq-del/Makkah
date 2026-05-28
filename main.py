from flask import Flask, request, Response
import requests

app = Flask(__name__)

# إيقاف تحذيرات الشهادات
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def catch_all(path):
    # الرابط الأصلي الذي يحاول السناب الوصول إليه
    target_url = f"https://app.snapchat.com/{path}"
    
    # تجهيز الهيدرات (إزالة Host لتفادي خطأ السيرفر)
    headers = {k: v for k, v in request.headers if k.lower() != 'host'}
    headers['Host'] = 'app.snapchat.com'
    
    # إرسال الطلب للسناب
    try:
        resp = requests.request(
            method=request.method,
            url=target_url,
            data=request.get_data(),
            headers=headers,
            params=request.args,
            verify=False
        )
        
        # إرجاع الرد للسناب
        return Response(
            resp.content,
            status=resp.status_code,
            headers=dict(resp.headers)
        )
    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
