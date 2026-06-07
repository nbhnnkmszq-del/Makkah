from flask import Flask, request, jsonify
import requests
import base64

app = Flask(__name__)

# هنا نضع "الكنز" (البيانات التي استخرجناها)
DEVICE_IDENTITY = {
    "user_id": "55a118bf-16cd-4527-9ea7-9f90fdab8faf",
    "access_token": "gEgIIARrGASHYUNaM8ScYAmymOmpHjoCXlPjPVLOO9p0aRI-wVSJSE3n72FT24W5ngP4eFA3uLaOVuHV",
    "att_token": "Ci1iNFCsaIvuN4FmwoMSXqFN1o531mchZS20Zbt9Sv2TDy8ACaUEsYDd88NjSwoVAQAAAA==",
    "signature": "JSiSYlxuy6dglS1wIydQBJjL0un5nr4AuOWhvV3W+N8="
}

@app.route('/proxy_login', methods=['POST'])
def proxy_login():
    # 1. استلام الطلب من النسخة المعدلة
    raw_data = request.data
    
    # 2. تجهيز الـ Headers المطابقة للنسخة الأصلية
    headers = {
        "Content-Type": "application/grpc+proto",
        "Authorization": f"Bearer {DEVICE_IDENTITY['access_token']}",
        "X-Snapchat-Att": DEVICE_IDENTITY['att_token'],
        "User-Agent": "Snapchat/12.80.0.44 (iPhone9,3; iOS 15.7.5; gzip)"
    }
    
    # 3. إعادة توجيه الطلب لسيرفر سناب شات الأصلي
    snap_url = "https://us-east1-aws.api.snapchat.com/snapchat.janus.api.LoginService/LoginWithPassword"
    response = requests.post(snap_url, data=raw_data, headers=headers)
    
    # 4. إرجاع النتيجة للنسخة المعدلة
    return response.content, response.status_code, {'Content-Type': 'application/grpc+proto'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
