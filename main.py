from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/proxy_login', methods=['POST', 'GET'])
def proxy():
    # هذا هو الرابط الأصلي الذي كان التويك يحاول الوصول له
    target_url = request.headers.get('X-Original-URL')
    
    # هنا يتم تنظيف الهيدرز وتزويرها
    headers = {
        'User-Agent': 'Snapchat/13.20.0 (iPhone14,2; iOS 16.0; gzip)',
        'X-Snapchat-Client-ID': 'N/A', # مسح معرف الجهاز
        'Accept-Language': 'en-US'
    }
    
    # إرسال الطلب النظيف للسناب
    response = requests.request(request.method, target_url, headers=headers, data=request.data)
    
    # إعادة رد السناب للتويك (وللمستخدم)
    return response.content, response.status_code

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
