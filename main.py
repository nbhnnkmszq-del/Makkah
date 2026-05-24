from flask import Flask, request, jsonify
import requests
import uuid
import random

app = Flask(__name__)

# قائمة بصمات أجهزة احترافية للتمويه
DEVICE_MODELS = ["iPhone15,3", "iPhone14,5", "iPhone16,2"]
OS_VERSIONS = ["16.5", "17.1", "17.2"]

def get_random_fingerprint():
    return {
        "device_id": str(uuid.uuid4()),
        "model": random.choice(DEVICE_MODELS),
        "os": random.choice(OS_VERSIONS)
    }

@app.route('/', methods=['GET'])
def home():
    return "السيرفر يعمل بكامل قوته.. الاعتراض جاهز."

@app.route('/proxy_login', methods=['POST'])
def proxy_login():
    try:
        # 1. استلام الطلب من جوالك
        data = request.get_json()
        
        # 2. توليد هوية جديدة "نظيفة"
        fp = get_random_fingerprint()
        
        # 3. بناء الهيدرز الجديدة (تزوير الهوية)
        headers = {
            "User-Agent": f"Snapchat/12.35.0.35 (iPhone; iOS {fp['os']}; Scale/3.00)",
            "X-Device-ID": fp['device_id'],
            "X-Device-Model": fp['model'],
            "X-Snapchat-Client-Version": "12.35.0.35",
            "Content-Type": "application/json"
        }
        
        # 4. إرسال الطلب الأصلي للسناب بعد "التطهير"
        # إذا كان جهازك محظور، هذا الطلب سيخرج بهوية جديدة تماماً
        response = requests.post("https://app.snapchat.com/lo/login", json=data, headers=headers, timeout=10)
        
        # 5. عرض الطلب في "اللوج" (للمراقبة من المتصفح أو الـ Console)
        print(f" [!] تم اعتراض طلب: {fp['device_id']} | Status: {response.status_code}")
        
        # 6. إرجاع النتيجة للتويك
        return jsonify(response.json()), response.status_code

    except Exception as e:
        print(f" [!] خطأ في الاعتراض: {e}")
        return jsonify({"status": "fail", "error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
