from flask import Flask, request, Response
import requests

app = Flask(__name__)

# هذا المسار مخصص لاستقبال طلبات السناب وتمريرها
@app.route('/v1/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def proxy(path):
    target_url = f"https://app.snapchat.com/{path}"
    
    # طباعة في سجلات (Logs) موقع Render عشان نتأكد أنه استلم الطلب
    print(f"--- [الوزير رصد طلب]: {request.method} {target_url} ---")
    
    # تحضير الـ Headers
    headers = {key: value for key, value in request.headers if key != 'Host'}
    headers['Host'] = 'app.snapchat.com'
    
    try:
        resp = requests.request(
            method=request.method,
            url=target_url,
            headers=headers,
            data=request.get_data(),
            params=request.args,
            timeout=15
        )
        # إرجاع الرد للسناب (أو للنسخة)
        return Response(resp.content, status=resp.status_code, headers=dict(resp.headers))
    except Exception as e:
        print(f"!!! [خطأ في الطلب]: {str(e)} !!!")
        return str(e), 500

if __name__ == '__main__':
    app.run()
