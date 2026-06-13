from flask import Flask, request, jsonify
import uuid

app = Flask(__name__)

@app.route('/proxy_login', methods=['POST'])
def proxy_login():
    # توليد بصمة فريدة متجددة
    generated_uuid = str(uuid.uuid4()).upper()
    
    # صياغة قاموس الترويسات الكامل بنسخة قديمة متناسقة تماماً
    custom_headers = {
        "X-Snapchat-UUID": generated_uuid,
        "x-snapchat-att-token": "Ci1iNFCsaIvuN4FmwoMSXqFN1o531mchZS20Zbt9Sv2TDy8ACaUEsYDd88NjSwoVAQAAAA==",
        "X-Snap-Access-Token": "hCgwKCjE3Nzk2NzA4MjASgAHPo67ALSrMM9NeAahNE3jdlHSkQ-UzFQdCMXtlsYfixAZXA7omp_H7jlk",
        "User-Agent": "Snapchat/12.10.0.34 (iPhone9,3; iOS 15.8.6; gzip)",
        "Accept-Language": "en-US;q=1.0",
        "X-Snap-Client-Type": "0",
        "x-snapchat-argos-strict-enforcement": "false"
    }
    
    # إرسال الحزمة الكاملة إلى التويك
    response_data = {
        "success": True,
        "headers": custom_headers,
        "device_model": "iPhone9,3",
        "os_version": "15.8.6",
        "uuid": generated_uuid
    }
    
    return jsonify(response_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
