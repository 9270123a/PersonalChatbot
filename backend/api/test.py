import requests

API_URL = "http://localhost:5000"
token = None  # 用於存儲身份驗證令牌

def test_register(username, password):
    response = requests.post(f"{API_URL}/register", json={"username": username, "password": password})
    print("Register:", response.json())

def test_login(username, password):
    global token
    response = requests.post(f"{API_URL}/login", json={"username": username, "password": password})
    result = response.json()
    print("Login:", result)
    if result.get('success'):
        token = result.get('token')
        print(f"Received token: {token}")

def test_chat(message):
    if not token:
        print("Error: Not logged in")
        return
    headers = {'Authorization': token}
    response = requests.post(f"{API_URL}/chat", json={"message": message}, headers=headers)
    print("Chat:", response.json())

def test_system_prompt():
    if not token:
        print("Error: Not logged in")
        return
    headers = {'Authorization': token}
    response = requests.get(f"{API_URL}/systemprompt", headers=headers)
    print("System Prompt:", response.json())

# 測試註冊
test_register("testuser", "testpassword")

# 測試登錄
test_login("testuser", "testpassword")

# 測試聊天
test_chat("Hello, how are you?")

# 測試系統提示
test_system_prompt()