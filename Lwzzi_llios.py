import os
import random
import string
import uuid
import requests
from flask import Flask, request, jsonify, Response

app = Flask(__name__)

# --- 1. مولد بصمات عشوائي (يخدع نظام الحظر) ---
def generate_random_device():
    models = ["iPhone14,2", "iPhone15,3", "iPhone16,1", "iPhone17,1", "iPhone15,2"]
    ios_versions = ["17.0.1", "17.1.2", "17.2.1", "17.3.1"]
    return {
        "model": random.choice(models),
        "os": random.choice(ios_versions),
        "device_id": str(uuid.uuid4()).upper(),
        "idfa": str(uuid.uuid4()),
        "user_agent": f"Snapchat/12.45.0.35 ({random.choice(models)}; iOS {random.choice(ios_versions)}; en_US)"
    }

# --- 2. محرك التلاعب بالهيدرز (لإخفاء التعديلات) ---
def forge_headers(incoming_headers):
    device = generate_random_device()
    headers = {
        "User-Agent": device["user_agent"],
        "X-Snapchat-Client-Auth": incoming_headers.get("X-Snapchat-Client-Auth", ""),
        "X-Device-ID": device["device_id"],
        "X-IDFA": device["idfa"],
        "Connection": "keep-alive",
        "Accept-Language": "en-US,en;q=0.9",
        "X-Request-ID": str(uuid.uuid4())
    }
    return headers

# --- 3. بوابة التوجيه الذكي (الجوهر) ---
SNAP_BASE_URL = "https://app.snapchat.com"

@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def proxy(path):
    url = f"{SNAP_BASE_URL}/{path}"
    headers = forge_headers(request.headers)
    
    # تحويل الطلبات (Login, Forgot Password, Register)
    try:
        if request.method == 'POST':
            data = request.get_json() or request.form
            resp = requests.post(url, headers=headers, json=data)
        else:
            resp = requests.get(url, headers=headers, params=request.args)
            
        # إرجاع رد السناب للتطبيق مباشرة مع تزوير هويتنا
        return Response(resp.content, status=resp.status_code, headers=dict(resp.headers))
    except Exception as e:
        return jsonify({"error": "Proxy Error", "details": str(e)}), 502

# --- 4. منطق تجاوز التحقق (Forgot Password / Email) ---
@app.route('/auth/check_override', methods=['POST'])
def override_verification():
    # هنا يتم حقن منطق يخبر السناب أن التحدي (Challenge) قد تم تجاوزه
    # سيتم استخدامه في الـ Hook الخاص بك
    return jsonify({"status": "success", "token": "OVERRIDE_TOKEN_ACTIVE"})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port)
