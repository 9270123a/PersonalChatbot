import requests

API_URL = "http://localhost:5000"

# def test_register(username, password):
#     response = requests.post(f"{API_URL}/register", json={"username": username, "password": password})
#     print("Register:", response.json())

# def test_login(username, password):
#     response = requests.post(f"{API_URL}/login", json={"username": username, "password": password})
#     print("Login:", response.json())

# def test_chat(message, username):
#     response = requests.post(f"{API_URL}/chat", json={"message": message})
#     print("Chat:", response.json())

def test_system_prompt():
    response = requests.get(f"{API_URL}/systemprompt")
    print(response.text)
    print("System Prompt:", response.json())

# # 测试注册
# test_register("testuser", "testpassword")

# 测试登录
# test_login("testuser", "testpassword")

# 测试聊天
# test_chat("Hello, how are you?", "testuser")

# 测试系统提示
test_system_prompt()