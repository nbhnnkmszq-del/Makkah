# snap_proxy_server.py
from flask import Flask, request, jsonify
import requests
import json

app = Flask(__name__)

# بياناتك اللي استخرجتها
CLEAN_DATA = {
    "access_token": "gEgIIARrGASHYUNaM8ScYAmymOmpHjoCXlPjPVLOO9p0aRI-wVSJSE3n72FT24W5ngP4eFA3uLaOVuHV",
    "user_id": "55a118bf-16cd-4527-9ea7-9f90fdab8faf",
    "att_token": "Ci1iNFCsaIvuN4FmwoMSXqFN1o531mchZS20Zbt9Sv2TDy8ACaUEsYDd88NjSwoVAQAAAA==",
    "device_uuid": "D7B3CF66-C29D-46B9-82A2-0783CECF4866",
    "signature": "JSiSYlxuy6dglS1wIydQBJjL0un5nr4AuOWhvV3W+N8=",
    "secondary_signature": "Ck3M9q284yKxKYWyRfdekCTm8SJ2jLOxT+oJ9UJgQQI=",
    "crypto_key": "MFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAEOEj9CnZKFfmE6nYT68kCW2C+2olmgkS/jMtoQNYut4SX7cQiejkrLM6sCzl/T3jk"
}

@app.route('/proxy_login', methods=['POST', 'GET'])
def proxy_login():
    if request.method == 'GET':
        # اختبار السيرفر
        return jsonify({"status": "alive", "message": "Proxy server is running", "data": CLEAN_DATA})
    
    # POST request - التعامل مع طلب تسجيل الدخول
    print("\n" + "="*50)
    print("📥 Login request received!")
    print(f"Data size: {len(request.data)} bytes")
    
    headers = {
        "Content-Type": "application/x-protobuf",
        "User-Agent": "Snapchat/13.20.0 (iPhone9,3; iOS 15.7.9; gzip)",
        "X-Snap-Access-Token": CLEAN_DATA["access_token"],
        "X-Snap-UserID": CLEAN_DATA["user_id"],
        "x-snapchat-att-token": CLEAN_DATA["att_token"],
        "X-Snapchat-UUID": CLEAN_DATA["device_uuid"],
        "X-Snap-Signature": CLEAN_DATA["signature"]
    }
    
    snapchat_url = "https://us-east1-aws.api.snapchat.com/snapchat.janus.api.LoginService/LoginWithPassword"
    
    try:
        response = requests.post(snapchat_url, data=request.data, headers=headers, timeout=15)
        print(f"✅ Response status: {response.status_code}")
        return response.content, response.status_code, {'Content-Type': 'application/x-protobuf'}
    except Exception as e:
        print(f"❌ Error: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("""
    ╔════════════════════════════════════════════╗
    ║   🔥 PROXY SERVER READY                    ║
    ║   GET  /proxy_login - Test the server      ║
    ║   POST /proxy_login - Login requests       ║
    ╚════════════════════════════════════════════╝
    """)
    app.run(host='0.0.0.0', port=5000, debug=True)
