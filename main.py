from flask import Flask, request
import os

app = Flask(__name__)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>', methods=['GET', 'POST'])
def catch_all(path):
    print(f"DEBUG: تلقيت طلباً على المسار: /{path}")
    return f"المسار المطلوب هو: {path}", 200

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
