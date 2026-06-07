# test_server.py
# سيرفر بسيط لاختبار التوجيه

from flask import Flask, request, jsonify

app = Flask(__name__)

# جميع البيانات النظيفة
CLEAN_DATA = {
    "access_token": "gEgIIARrGASHYUNaM8ScYAmymOmpHjoCXlPjPVLOO9p0aRI-wVSJSE3n72FT24W5ngP4eFA3uLaOVuHV",
    "user_id": "55a118bf-16cd-4527-9ea7-9f90fdab8faf",
    "att_token": "Ci1iNFCsaIvuN4FmwoMSXqFN1o531mchZS20Zbt9Sv2TDy8ACaUEsYDd88NjSwoVAQAAAA==",
    "device_uuid": "D7B3CF66-C29D-46B9-82A2-0783CECF4866",
    "signature": "JSiSYlxuy6dglS1wIydQBJjL0un5nr4AuOWhvV3W+N8="
}

@app.route('/proxy_login', methods=['GET', 'POST'])
def proxy_login():
    print("\n" + "="*50)
    print("📥 Request received:")
    print(f"   Method: {request.method}")
    print(f"   Headers: {dict(request.headers)}")
    print(f"   Data length: {len(request.data)} bytes")
    print("="*50)
    
    if request.method == 'POST':
        # إذا كان POST، نحاول نمرر الطلب لسناب أو نرجع رد
        return jsonify({
            "status": "success",
            "message": "Login request received",
            "data": CLEAN_DATA
        }), 200
    else:
        # إذا كان GET (زي اللي جايك من Firefox)
        return jsonify({
            "status": "error",
            "message": "Use POST method for login. This endpoint requires POST.",
            "expected_format": "Protobuf binary data",
            "example": "Send a POST request with the login protobuf data"
        }), 200  # 200 حتى لا يخرب التطبيق

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "alive", "message": "Server is running"})

if __name__ == '__main__':
    print("""
╔════════════════════════════════════════════╗
║   🔥 TEST PROXY SERVER                    ║
║   POST /proxy_login - للطلبات            ║
║   GET  /proxy_login - للاختبار           ║
║   GET  /health - للتأكد من الشغل         ║
╚════════════════════════════════════════════╝
    """)
    app.run(host='0.0.0.0', port=5000, debug=True)
