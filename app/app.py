from flask import Flask
import os

app = Flask(__name__)

VERSION = os.environ.get('APP_VERSION', 'v1.0.0')

@app.route('/')
def home():
    return f"Application Version: {VERSION}"

@app.route('/health')
def health():
    return "OK", 200

if __name__ == '__main__':
    PORT = int(os.environ.get('APP_PORT', 5000))
    app.run(host='0.0.0.0', port=PORT)
