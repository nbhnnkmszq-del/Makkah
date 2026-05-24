from flask import Flask, request, jsonify

app = Flask(__name__)

# هذا المسار للجذر (عشان المتصفح يعطيك رسالة نجاح بدل 404)
@app.route('/', methods=['GET'])
def home():
    return "السيرفر يعمل يا وزير، الرابط شغال!"

# هذا المسار هو الذي يستخدمه التويك للاعتراض
@app.route('/proxy_login', methods=['POST'])
def proxy_login():
    data = request.get_json()
    print(f" [!] طلب اعتراض وصل: {data}") # هذا سيظهر في الـ Logs الخاص بـ Render
    
    # هنا كودك القديم (التلاعب بالهيدرز والتوجيه لسناب)
    # ملاحظة: تأكد من دمج كود التوجيه هنا كما كان في كودك الأصلي
    return jsonify({"status": "success", "message": "Bypassed"})

if __name__ == '__main__':
    # Render يستخدم المنفذ 10000 غالباً، جرب 8080 أو 10000
    app.run(host='0.0.0.0', port=10000)
