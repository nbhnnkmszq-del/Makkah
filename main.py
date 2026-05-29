from flask import Flask, request, Response
import requests

app = Flask(__name__)

# هذا الديكور يمسك أي مسار يبدأ بـ /loq/
@app.route('/loq/<path:subpath>', methods=['GET', 'POST'])
def proxy_to_snap(subpath):
    target_url = f"https://app.snapchat.com/loq/{subpath}"
    
    # تحويل الطلب
    resp = requests.request(
        method=request.method,
        url=target_url,
        data=request.get_data(),
        headers={k: v for k, v in request.headers if k.lower() != 'host'},
        params=request.args,
        verify=False
    )
    return Response(resp.content, status=resp.status_code, headers=dict(resp.headers))

if __name__ == '__main__':
    import os
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))
