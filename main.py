from flask import Flask, request, Response
import requests

app = Flask(__name__)

# بيانات الجهاز النظيف
CLEAN_DATA = {
    "access_token": "gEgIIARrGASHYUNaM8ScYAmymOmpHjoCXlPjPVLOO9p0aRI-wVSJSE3n72FT24W5ngP4eFA3uLaOVuHV",
    "user_id": "55a118bf-16cd-4527-9ea7-9f90fdab8faf",
    "att_token": "Ci1iNFCsaIvuN4FmwoMSXqFN1o531mchZS20Zbt9Sv2TDy8ACaUEsYDd88NjSwoVAQAAAA==",
    "device_uuid": "0196B3EE-508D-4FAC-9F7B-1B790E57DDBB",
    "signature": "JSiSYlxuy6dglS1wIydQBJjL0un5nr4AuOWhvV3W+N8="
}

@app.route('/proxy_login', methods=['POST'])
def proxy_login():
    headers = {
        "X-Snap-Access-Token": CLEAN_DATA["access_token"],
        "X-Snap-UserID": CLEAN_DATA["user_id"],
        "x-snapchat-att-token": CLEAN_DATA["att_token"],
        "X-Snapchat-UUID": CLEAN_DATA["device_uuid"],
        "X-Snap-Signature": CLEAN_DATA["signature"],
        "Content-Type": "application/x-protobuf",
        "User-Agent": "Snapchat/12.80.35 (iPhone9,3; iOS 15.8.6; gzip)"
    }
    
    try:
        snap_url = "https://us-east1-aws.api.snapchat.com/snapchat.janus.api.LoginService/LoginWithPassword"
        response = requests.post(snap_url, data=request.data, headers=headers, timeout=30)
        return Response(response.content, status=200, headers={'Content-Type': 'application/x-protobuf'})
    except:
        return Response(b'', status=200)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
