from flask import Flask, request, jsonify
import uuid

app = Flask(__name__)

# إعداد المسار الجديد لاستقبال طلبات POST
@app.route('/proxy_login', methods=['POST'])
def proxy_login():
    incoming_data = request.get_json(silent=True) or {}
    
    # طباعة المعطيات القادمة من التويك للمراقبة
    print(f"[+] Request received from App Version: {incoming_data.get('app_version', 'Unknown')}")
    
    # توليد بصمة UUID جديدة وديناميكية لكل جهاز يتصل لمنع تكرار المعرفات
    generated_uuid = str(uuid.uuid4()).upper()
    
    # تجهيز الحزمة المتطابقة والنظيفة بناءً على الاستخراج الناجح
    clean_payload = {
        "uuid": generated_uuid,  # بصمة متجددة فريدة
        "att_token": "Ci1iNFCsaIvuN4FmwoMSXqFN1o531mchZS20Zbt9Sv2TDy8ACaUEsYDd88NjSwoVAQAAAA==",
        "access_token": "hCgwKCjE3Nzk2NzA4MjASgAHPo67ALSrMM9NeAahNE3jdlHSkQ-UzFQdCMXtlsYfixAZXA7omp_H7jlk",
        "model": "iPhone9,3",
        "os_version": "15.8.6"
    }
    
    return jsonify(clean_payload)

if __name__ == '__main__':
    # تشغيل السيرفر محلياً أو خلف proxy (تأكد من إعدادات المنفذ على Render)
    app.run(host='0.0.0.0', port=5000)
