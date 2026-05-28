from flask import Flask, request, Response
import requests

app = Flask(__name__)

# 1. لا تستخدم هيدرات عامة، استخدم هيدرات حقيقية من "جهاز نظيف"
# التوقيع (Signature) هو مفتاح اللعبة
SPOOF_HEADERS = {
    'User-Agent': 'Snapchat/13.20.0 (iPhone14,2; iOS 16.0; scale=3.00)',
    'X-Snapchat-Client-Auth': 'TOKEN_FROM_CLEAN_DEVICE', # لازم تجيبه من جهاز غير محظور
    'X-Snap-Device-ID': 'GENERATE_A_NEW_UUID', # غيره في كل طلب
    'Accept-Language': 'en-US,en;q=0.9',
    'Connection': 'keep-alive'
}

@app.route('/proxy_login', methods=['POST'])
def proxy():
    # عنوان سيرفر سناب الأصلي (يجب أن يكون ثابتاً للسناب)
    target_url = "https://app.snapchat.com/..." 

    # 2. تنظيف الهيدرز من آثار الفلاسك (تجنب كشف البروكسي)
    headers = {k: v for k, v in request.headers if k.lower() not in ['host', 'x-original-url', 'x-forwarded-for']}
    headers.update(SPOOF_HEADERS)

    # 3. تعديل الـ Payload (إذا كنت تحتاج لتغيير اليوزر/الباس)
    data = request.get_data()

    try:
        resp = requests.post(
            target_url,
            headers=headers,
            data=data,
            verify=False, # عشان يتخطى شهادات السيرفر
            timeout=15
        )
        
        # 4. فلترة الهيدرز المرجعة عشان ما يكتشف التويك أنك ببروكسي
        excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
        headers_to_return = {k: v for k, v in resp.headers.items() if k.lower() not in excluded_headers}
        
        return Response(resp.content, resp.status_code, headers_to_return)
    except Exception as e:
        return str(e), 502

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
