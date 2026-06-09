import base64
import time
from flask import Flask, request, jsonify

app = Flask(__name__)

# ============================================================
# 1. تكوين مخرجات الجهاز النظيف والمحاكاة (Environment Spoofing)
# ============================================================
CLEAN_ENV_CONFIG = {
    "ios_version": "17.4.1",                 # إصدار النظام النظيف المستهدف
    "snap_version": "12.81.0.37",            # إصدار نسخة السناب شات
    "device_model": "iPhone15,3",            # موديل الجهاز (iPhone 14 Pro Max)
    "user_agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 Snapchat/12.81.0.37 (arm64)",
    
    # المعرفات النظيفة والتوكنات المستخرجة
    "device_uuid": "0196B3EE-508D-4FAC-9F7B-1B790E57DDBB",
    "access_token": "gEgIIARrGASHYUNaM8ScYAmymOmpHjoCXlPjPVLOO9p0aRI-wVSJSE3n72FT24W5ngP4eFA3uLaOVuHV",
    "access_token_alt": "hCgwKCjE3Nzk2NzA4MjASgAHPo67ALSrMM9NeAahNE3jdlHSkQ-UzFQdCMXtlsYfixAZXA7omp_H7jlk",
    "att_token": "Ci1iNFCsaIvuN4FmwoMSXqFN1o531mchZS20Zbt9Sv2TDy8ACaUEsYDd88NjSwoVAQAAAA==",
    "user_id": "55a118bf-16cd-4527-9ea7-9f90fdab8faf",
    
    # مصفوفة الـ Protobuf الأساسية المستخرجة كاملاً والتي تطابق التواقيع
    "protobuf_base64_payload": "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"
}

# ============================================================
# 2. الهيدرز النظيفة المعتمدة (Clean Simulated Headers Cluster)
# ============================================================
CLEAN_HEADERS = {
    "Host": "aws.api.snapchat.com",
    "Accept": "*/*",
    "Accept-Language": "ar-AE;q=1, en-AE;q=0.9",
    "Content-Type": "application/x-protobuf",
    "X-Snapchat-Client-Auth-Token": CLEAN_ENV_CONFIG["access_token"],
    "X-Snapchat-UUID": CLEAN_ENV_CONFIG["device_uuid"],
    "User-Agent": CLEAN_ENV_CONFIG["user_agent"],
    "X-Snapshat-OS": "1",  # دلالة على نظام iOS
    "X-Snapchat-App-Version": CLEAN_ENV_CONFIG["snap_version"],
    "X-Snapchat-OS-Version": CLEAN_ENV_CONFIG["ios_version"],
    "X-Snapchat-Device-Model": CLEAN_ENV_CONFIG["device_model"]
}

# ============================================================
# 3. نقطة استلام ومعالجة الطلبات (Fast Pipeline Endpoint)
# ============================================================
@app.route('/proxy_login', methods=['POST'])
def proxy_login():
    start_time = time.time()
    
    # استقبال طلب التويك
    input_json = request.get_json()
    if not input_json:
        return jsonify({"status": "failed", "reason": "Empty JSON Payload"}), 400
    
    username = input_json.get("username", "")
    password = input_json.get("password", "")
    
    print(f"\n[+] [{int(start_time)}] Intercepted Incoming Request:")
    print(f"    👤 Target Account: {username}")
    print(f"    📱 Masking OS Version: {CLEAN_ENV_CONFIG['ios_version']}")
    print(f"    📦 Masking App Version: {CLEAN_ENV_CONFIG['snap_version']}")
    
    try:
        # فك تغليف حمولة الـ Protobuf النظيفة للتحقق من سلامتها الهيكلية وإعادة بنائها برمجياً لـ Base64
        raw_proto_bytes = base64.b64decode(CLEAN_ENV_CONFIG["protobuf_base64_payload"])
        re_encoded_payload = base64.b64encode(raw_proto_bytes).decode('utf-8')
        
        # بناء حزمة الاستجابة السريعة شاملة الهيدرز والمحاكاة لضمان عدم حدوث ريجيكت أو تأخير في معالجة التويك
        response_package = {
            "status": "success",
            "timestamp": int(time.time()),
            "processing_ms": int((time.time() - start_time) * 1000),
            "environment": {
                "os": "iOS",
                "os_version": CLEAN_ENV_CONFIG["ios_version"],
                "app_version": CLEAN_ENV_CONFIG["snap_version"],
                "device": CLEAN_ENV_CONFIG["device_model"]
            },
            "headers_snapshot": CLEAN_HEADERS,
            "user_id": CLEAN_ENV_CONFIG["user_id"],
            "device_uuid": CLEAN_ENV_CONFIG["device_uuid"],
            "access_token": CLEAN_ENV_CONFIG["access_token"],
            "access_token_alt": CLEAN_ENV_CONFIG["access_token_alt"],
            "att_token": CLEAN_ENV_CONFIG["att_token"],
            "protobuf_base64": re_encoded_payload  # البيانات المغلفة والمشفرة والجاهزة للحقن الفوري
        }
        
        print(f"[-] Execution Completed Speed: {response_package['processing_ms']}ms - Sending Back Clean Payload.")
        return jsonify(response_package), 200

    except Exception as e:
        print(f"❌ Error Packaging Safe Data: {str(e)}")
        return jsonify({"status": "failed", "reason": "Internal Processing Error"}), 500

if __name__ == '__main__':
    # تشغيل السيرفر على هوست موحد ومنفذ مخصص للبيئات السحابية وسريع في الاستجابة والتمرير
    app.run(host='0.0.0.0', port=10000, threaded=True)
