# snap_proxy_server.py
# سيرفر وسيط متكامل - مع Base64 مطابق

from flask import Flask, request, jsonify
import requests
import base64
import json
import time
import hashlib
from datetime import datetime

app = Flask(__name__)

# ============================================
# 1. البيانات النظيفة (كنزك - نفس اللي استخرجته)
# ============================================

# التوكنات الأساسية
ACCESS_TOKEN = "gEgIIARrGASHYUNaM8ScYAmymOmpHjoCXlPjPVLOO9p0aRI-wVSJSE3n72FT24W5ngP4eFA3uLaOVuHV"
ACCESS_TOKEN_ALT = "hCgwKCjE3Nzk2NzA4MjASgAHPo67ALSrMM9NeAahNE3jdlHSkQ-UzFQdCMXtlsYfixAZXA7omp_H7jlk"
USER_ID = "55a118bf-16cd-4527-9ea7-9f90fdab8faf"
DEVICE_UUID = "D7B3CF66-C29D-46B9-82A2-0783CECF4866"
ATT_TOKEN = "Ci1iNFCsaIvuN4FmwoMSXqFN1o531mchZS20Zbt9Sv2TDy8ACaUEsYDd88NjSwoVAQAAAA=="

# التواقيع (مطابقة للي طلع لك)
PRIMARY_SIGNATURE = "JSiSYlxuy6dglS1wIydQBJjL0un5nr4AuOWhvV3W+N8="
SECONDARY_SIGNATURE = "Ck3M9q284yKxKYWyRfdekCTm8SJ2jLOxT+oJ9UJgQQI="
SESSION_SIGNATURE = "xCyN1+/6r+JJwR+5Zzy9efUpb0fNPahJgsio8P881OUbQsasNaNukAe0hFQ0XafooCI+qkYPDpWcES5a2O/iEw=="

# مفاتيح التشفير (EC Keys)
CRYPTO_KEY_1 = "MFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAEOEj9CnZKFfmE6nYT68kCW2C+2olmgkS/jMtoQNYut4SX7cQiejkrLM6sCzl/T3jkdb1PmWueOA3hGQlEMUm/1Q=="
CRYPTO_KEY_2 = "MFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAEWNtVqirepxhJtZWQfPhW3ZInUIe4/75f78nRDU2mH2qvWpUS/K+GEIh32cv1aktL"

# Nonces (مطابقة)
NONCES = [
    "LPjmLnbbQ1uS3hVyphdHNw==",
    "Z0VahBNXQxWxinfAkBDaRw==",
    "1GhuGPbZS+ueWKQM0FaZkw==",
    "0hsiXQ+7R+CIFDcmQKvKDQ==",
    "aposO1gSSjG97rRATnFsjg==",
    "8NHu4JNoTfmtUYHcpfaFaQ=="
]

# Protobuf المشفر
PROTOBUF_ENCODED = "AgAAAJzu4/c6Ed24KehpIIjYMpIEUNk0+me89vLfv5ZingpyOOkgXXXyjPzYTzWmWSu+BYqcD47byirLZ++3dJccpF99hWppT7G5"

# فحوصات السلامة
INTEGRITY_CHECKS = {
    "app_integrity": "MAVKkZBbT0mpv68qaiih/g==",
    "jailbreak_detection": "qRYWiILERoyCcvGqrSBuYA==",
    "tamper_detection": "S0aV5hCyQLmDLebW0oc7SA==",
    "memory_check": "fe8Xrmh+S0yXUB6ZlSLXRQ=="
}

# OAuth
OAUTH_TOKEN = "iOrtcHZ2cUYvBuLztJo4NQ=="
OAUTH_REFRESH = "FAKd41UfNbQD9+4+5Ol3FvPR8Jw1hNNy+rL3dsXW3t4="

# Feature Flags
FEATURE_FLAGS = "CODvv5v4/////wESJQofUE9EX00xX1BVQkxJQ19TVE9SWV9GRUFUVVJFX1NFVBICIAESHAoWUE9EX00yX0RFRkFVTFRfUFJPRklM"

# معلومات الجهاز النظيف
DEVICE_INFO = {
    "model": "iPhone9,3",
    "name": "iPhone 7",
    "chip": "Apple A10",
    "os_version": "15.7.9",
    "country_code": "ar",
    "language": "ar",
    "username": "NL"
}

# ============================================
# 2. تجهيز الـ Headers الكاملة (مطابقة لسناب)
# ============================================
def get_headers(extra_headers=None):
    headers = {
        "Content-Type": "application/x-protobuf",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "ar,en;q=0.9",
        "Connection": "keep-alive",
        "User-Agent": "Snapchat/12.80.0.44 (iPhone9,3; iOS 15.7.5; gzip)",
        "X-Snap-Access-Token": ACCESS_TOKEN,
        "X-Snap-UserID": USER_ID,
        "x-snapchat-att-token": ATT_TOKEN,
        "X-Snapchat-UUID": DEVICE_UUID,
        "X-Snap-Signature": PRIMARY_SIGNATURE,
        "X-Snap-Route-Tag": "mixed-feed",
        "x-snapchat-argos-strict-enforcement": "true"
    }
    
    if extra_headers:
        headers.update(extra_headers)
    
    return headers

# ============================================
# 3. دوال مساعدة للتشفير Base64
# ============================================
def decode_base64(data):
    """فك تشفير Base64"""
    try:
        return base64.b64decode(data)
    except:
        return None

def encode_base64(data):
    """تشفير إلى Base64"""
    try:
        return base64.b64encode(data).decode('utf-8')
    except:
        return None

def base64_to_json(base64_str):
    """تحويل Base64 إلى JSON (إذا كان Protobuf مفكوك)"""
    decoded = decode_base64(base64_str)
    if decoded:
        try:
            return json.loads(decoded)
        except:
            return {"raw": base64_str}
    return None

# ============================================
# 4. نقاط النهاية (Endpoints)
# ============================================

# 4.1 تسجيل الدخول
@app.route('/proxy_login', methods=['POST'])
def proxy_login():
    raw_data = request.data
    
    headers = get_headers()
    
    snap_url = "https://us-east1-aws.api.snapchat.com/snapchat.janus.api.LoginService/LoginWithPassword"
    
    try:
        response = requests.post(snap_url, data=raw_data, headers=headers, timeout=30)
        print(f"✅ [Login] Status: {response.status_code}")
        return response.content, response.status_code, {'Content-Type': 'application/x-protobuf'}
    except Exception as e:
        print(f"❌ [Login] Error: {e}")
        return {"error": str(e)}, 500

# 4.2 إنشاء حساب جديد
@app.route('/proxy_signup', methods=['POST'])
def proxy_signup():
    raw_data = request.data
    
    headers = get_headers()
    
    snap_url = "https://us-east1-aws.api.snapchat.com/snapchat.account.api.AccountService/CreateAccount"
    
    try:
        response = requests.post(snap_url, data=raw_data, headers=headers, timeout=30)
        print(f"✅ [Signup] Status: {response.status_code}")
        return response.content, response.status_code, {'Content-Type': 'application/x-protobuf'}
    except Exception as e:
        print(f"❌ [Signup] Error: {e}")
        return {"error": str(e)}, 500

# 4.3 إرسال كود استعادة كلمة المرور
@app.route('/proxy_send_recovery', methods=['POST'])
def proxy_send_recovery():
    raw_data = request.data
    
    headers = get_headers()
    
    snap_url = "https://us-east1-aws.api.snapchat.com/snapchat.account.api.AccountService/SendRecoveryCode"
    
    try:
        response = requests.post(snap_url, data=raw_data, headers=headers, timeout=30)
        print(f"✅ [SendRecovery] Status: {response.status_code}")
        return response.content, response.status_code, {'Content-Type': 'application/x-protobuf'}
    except Exception as e:
        print(f"❌ [SendRecovery] Error: {e}")
        return {"error": str(e)}, 500

# 4.4 التحقق من كود استعادة كلمة المرور
@app.route('/proxy_verify_recovery', methods=['POST'])
def proxy_verify_recovery():
    raw_data = request.data
    
    headers = get_headers()
    
    snap_url = "https://us-east1-aws.api.snapchat.com/snapchat.account.api.AccountService/VerifyRecoveryCode"
    
    try:
        response = requests.post(snap_url, data=raw_data, headers=headers, timeout=30)
        print(f"✅ [VerifyRecovery] Status: {response.status_code}")
        return response.content, response.status_code, {'Content-Type': 'application/x-protobuf'}
    except Exception as e:
        print(f"❌ [VerifyRecovery] Error: {e}")
        return {"error": str(e)}, 500

# 4.5 تجديد التوكنات
@app.route('/proxy_refresh', methods=['POST'])
def proxy_refresh():
    raw_data = request.data
    
    headers = get_headers()
    
    snap_url = "https://us-east1-aws.api.snapchat.com/snapchat.janus.api.AuthService/RefreshToken"
    
    try:
        response = requests.post(snap_url, data=raw_data, headers=headers, timeout=30)
        print(f"✅ [Refresh] Status: {response.status_code}")
        return response.content, response.status_code, {'Content-Type': 'application/x-protobuf'}
    except Exception as e:
        print(f"❌ [Refresh] Error: {e}")
        return {"error": str(e)}, 500

# 4.6 الحصول على جميع البيانات النظيفة (للتوييك)
@app.route('/get_clean_data', methods=['GET'])
def get_clean_data():
    return jsonify({
        "status": "success",
        "access_token": ACCESS_TOKEN,
        "access_token_alt": ACCESS_TOKEN_ALT,
        "user_id": USER_ID,
        "device_uuid": DEVICE_UUID,
        "att_token": ATT_TOKEN,
        "primary_signature": PRIMARY_SIGNATURE,
        "secondary_signature": SECONDARY_SIGNATURE,
        "session_signature": SESSION_SIGNATURE,
        "crypto_keys": [CRYPTO_KEY_1, CRYPTO_KEY_2],
        "nonces": NONCES,
        "protobuf_encoded": PROTOBUF_ENCODED,
        "integrity_checks": INTEGRITY_CHECKS,
        "oauth_token": OAUTH_TOKEN,
        "oauth_refresh": OAUTH_REFRESH,
        "feature_flags": FEATURE_FLAGS,
        "device_info": DEVICE_INFO
    })

# 4.7 فك تشفير Base64 (اختبار)
@app.route('/decode', methods=['POST'])
def decode_base64_endpoint():
    data = request.json
    base64_str = data.get('base64_string', '')
    
    decoded = decode_base64(base64_str)
    if decoded:
        return jsonify({
            "status": "success",
            "decoded": decoded.hex(),
            "decoded_string": decoded.decode('utf-8', errors='ignore'),
            "length": len(decoded)
        })
    else:
        return jsonify({"status": "error", "message": "Invalid Base64"}), 400

# 4.8 صحة السيرفر
@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        "status": "online",
        "timestamp": datetime.now().isoformat(),
        "version": "13.20.0",
        "device_info": DEVICE_INFO,
        "endpoints": [
            "/proxy_login",
            "/proxy_signup",
            "/proxy_send_recovery",
            "/proxy_verify_recovery",
            "/proxy_refresh",
            "/get_clean_data",
            "/decode",
            "/health"
        ]
    })

# ============================================
# 5. تشغيل السيرفر
# ============================================
if __name__ == '__main__':
    print("""
╔══════════════════════════════════════════════════════════════════╗
║   🔥 ULTIMATE SNAPCHAT PROXY SERVER - BASE64 READY 🔥           ║
╠══════════════════════════════════════════════════════════════════╣
║   📦 Clean Device Identity Loaded:                              ║
║     - User ID: {}  
║     - Access Token: {}...  
║     - Device UUID: {}  
║     - Primary Signature: {}...  
║                                                                 ║
║   🔐 Base64 Encoded Data Ready:                                 ║
║     - Nonces: {}  
║     - Crypto Keys: 2  
║     - Integrity Checks: 4  
║                                                                 ║
║   🚀 Server running on http://0.0.0.0:5000                      ║
║   📡 Endpoints available for all operations                     ║
╚══════════════════════════════════════════════════════════════════╝
    """.format(
        USER_ID[:20],
        ACCESS_TOKEN[:30],
        DEVICE_UUID,
        PRIMARY_SIGNATURE[:20],
        len(NONCES)
    ))
    app.run(host='0.0.0.0', port=5000, debug=False)
