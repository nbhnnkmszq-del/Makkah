from flask import Flask, request, Response
import requests
import json
from datetime import datetime

app = Flask(__name__)

# ============================================
# بيانات الجهاز النظيف (تزوير كامل)
# ============================================
CLEAN_DATA = {
    "access_token": "gEgIIARrGASHYUNaM8ScYAmymOmpHjoCXlPjPVLOO9p0aRI-wVSJSE3n72FT24W5ngP4eFA3uLaOVuHV",
    "user_id": "55a118bf-16cd-4527-9ea7-9f90fdab8faf",
    "att_token": "Ci1iNFCsaIvuN4FmwoMSXqFN1o531mchZS20Zbt9Sv2TDy8ACaUEsYDd88NjSwoVAQAAAA==",
    "device_uuid": "0196B3EE-508D-4FAC-9F7B-1B790E57DDBB",
    "signature": "JSiSYlxuy6dglS1wIydQBJjL0un5nr4AuOWhvV3W+N8=",
    "device_model": "iPhone9,3",
    "system_version": "15.8.6",
    "headers": {
        "X-Snap-Access-Token": "gEgIIARrGASHYUNaM8ScYAmymOmpHjoCXlPjPVLOO9p0aRI-wVSJSE3n72FT24W5ngP4eFA3uLaOVuHV",
        "X-Snap-UserID": "55a118bf-16cd-4527-9ea7-9f90fdab8faf",
        "x-snapchat-att-token": "Ci1iNFCsaIvuN4FmwoMSXqFN1o531mchZS20Zbt9Sv2TDy8ACaUEsYDd88NjSwoVAQAAAA==",
        "X-Snapchat-UUID": "0196B3EE-508D-4FAC-9F7B-1B790E57DDBB",
        "X-Snap-Signature": "JSiSYlxuy6dglS1wIydQBJjL0un5nr4AuOWhvV3W+N8=",
        "User-Agent": "Snapchat/12.80.35 (iPhone9,3; iOS 15.8.6; gzip)",
        "Content-Type": "application/x-protobuf"
    }
}

@app.route('/proxy_login', methods=['POST'])
def proxy_login():
    print(f"[{datetime.now()}] POST request received, size: {len(request.data)} bytes")
    
    headers = CLEAN_DATA["headers"].copy()
    
    try:
        snap_url = "https://us-east1-aws.api.snapchat.com/snapchat.janus.api.LoginService/LoginWithPassword"
        response = requests.post(snap_url, data=request.data, headers=headers, timeout=30)
        print(f"[{datetime.now()}] Snapchat response: {response.status_code}")
        
        return Response(response.content, status=200, headers={'Content-Type': 'application/x-protobuf'})
    except Exception as e:
        print(f"[{datetime.now()}] Error: {e}")
        return Response(b'', status=200, headers={'Content-Type': 'application/x-protobuf'})

@app.route('/health', methods=['GET'])
def health():
    return {"status": "alive", "timestamp": datetime.now().isoformat()}

if __name__ == '__main__':
    print("""
    ╔════════════════════════════════════════════╗
    ║   🔥 Snapchat Proxy Server                 ║
    ║   POST /proxy_login - Login requests       ║
    ╚════════════════════════════════════════════╝
    """)
    app.run(host='0.0.0.0', port=5000)
