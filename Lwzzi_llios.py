from flask import Flask, request, jsonify, Response
import requests
import random
import uuid

app = Flask(__name__)

# بصمات أجهزة عشوائية للتمويه
DEVICE_MODELS = ["iPhone13,2", "iPhone14,2", "iPhone15,3"]
OS_VERSIONS = ["15.4.1", "16.1.0", "16.5.1"]

def generate_fingerprint():
    return {
        "X-Device-ID": str(uuid.uuid4()),
        "X-Device-Model": random.choice(DEVICE_MODELS),
        "X-OS-Version": random.choice(OS_VERSIONS),
        "X-Snapchat-Client-Version": "12.35.0.35" # نسخة قديمة ومستقرة
    }

@app.route('/proxy_login', methods=['POST'])
def proxy_login():
    # 1. استقبال البيانات من التويك
    data = request.get_json()
    
    # 2. توليد هوية جديدة بالكامل
    new_identity = generate_fingerprint()
    
    # 3. إعداد الهيدرز الجديدة لتتجاوز فحص سناب
    headers = {
        "User-Agent": f"Snapchat/{new_identity['X-Snapchat-Client-Version']} (iPhone; iOS {new_identity['X-OS-Version']}; Scale/3.00)",
        "X-Device-ID": new_identity['X-Device-ID'],
        "X-Snapchat-API-Level": "1",
        "Connection": "close"
    }
    
    # 4. التوجيه لسيرفرات سناب الحقيقية (بصورة نظيفة)
    try:
        snap_response = requests.post(
            "https://app.snapchat.com/lo/login", 
            json=data, 
            headers=headers,
            timeout=5
        )
        
        # 5. التلاعب بالرد قبل إرساله للتويك (إجبار النجاح)
        if snap_response.status_code == 200 or "success" in snap_response.text:
            return jsonify({"status": "success", "token": "CLEAN_TOKEN_GENERATED"})
        else:
            # إذا حظر سناب، السيرفر يخدع التطبيق بـ "نجاح وهمي"
            return jsonify({"status": "success", "message": "Bypassed"})
            
    except Exception as e:
        return jsonify({"status": "error", "detail": str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
