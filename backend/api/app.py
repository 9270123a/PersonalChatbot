from flask import Flask, request, jsonify
import os, sys
current_dir = os.path.dirname(os.path.abspath(__file__))
# 获取 backend 目录的路径
backend_dir = os.path.dirname(current_dir)
# 将 backend 目录添加到 Python 路径
sys.path.append(backend_dir)
from services.chat_service import Chat_Service
from services.systemprompt_service import SystemPrompt_Service
from services.user_service import Usermanagement_Service


app = Flask(__name__)
systempromptService = SystemPrompt_Service()
chatservice = Chat_Service()
userservice = Usermanagement_Service()


@app.route('/login', methods=['POST'])
def login():
    data = request.json
    result = userservice.login(data['username'],data['password'])
    return jsonify(result)

@app.route('/register', methods = ['POST'])
def register():
    data = request.json
    result = userservice.register(data['username'], data['password'])
    return jsonify(result)

@app.route('/chat', methods = ['POST'])
def chat():
    data = request.json
    result = chatservice.chat(data['message'])
    return jsonify(result)

@app.route('/systemprompt', methods = ["GET"])
def systemprompt():
    result = systempromptService.get_current_prompt()
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)