from flask import Flask, request, jsonify
import os, sys
from functools import wraps
current_dir = os.path.dirname(os.path.abspath(__file__))
# 获取 backend 目录的路径
backend_dir = os.path.dirname(current_dir)
# 将 backend 目录添加到 Python 路径
sys.path.append(backend_dir)
from services.chat_service import Chat_Service
from services.user_service import Usermanagement_Service
from models.user_management import UserManagement
from models.vector_db import VectorDB
from dotenv import load_dotenv

# 加载 .env 文件
load_dotenv()
from openai import OpenAI

# 检查并获取 API 密钥
api_key = os.getenv("OPENAI_API_KEY")

# 初始化 OpenAI 客户端
client = OpenAI(api_key=api_key)

app = Flask(__name__)

usermanagement = UserManagement()
vc_db = VectorDB(client, "./user_data")
chatservice = Chat_Service(usermanagement ,vc_db , client)
userservice = Usermanagement_Service(usermanagement)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth = request.headers.get('Authorization')
        if not auth or not userservice.verify_auth_token(auth):
            return jsonify({"error": "Unauthorized"}), 401
        # 設置當前用戶
        username = userservice.get_username_from_token(auth)
        usermanagement.set_current_user(username)
        return f(*args, **kwargs)
    return decorated_function


@app.route('/login', methods=['POST'])
def login():
    data = request.json
    result = userservice.login(data['username'], data['password'])
    if result['success']:
        token = userservice.generate_auth_token(data['username'])
        result['token'] = token
    return jsonify(result)

@app.route('/register', methods = ['POST'])
def register():
    data = request.json
    result = userservice.register(data['username'], data['password'])
    return jsonify(result)

@app.route('/chat', methods = ['POST'])
@login_required
def chat():
    data = request.json
    result = chatservice.chat(data['message'])
    return jsonify(result)

@app.route('/systemprompt', methods = ["GET"])
@login_required
def systemprompt():
    result = chatservice.get_and_update_prompt()
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)