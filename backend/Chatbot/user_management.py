import json
import os 
import pickle



# #將user存json，然後再到對應的資料夾取出過往的聊天紀錄
class UserManagement:


    def __init__(self, userfile = "user.json"):

        self.userfile = userfile
        self.users = self.load_user()
        self.current_user = None

    def get_current_user(self):
        return self.current_user
    def log_out(self):
        self.current_user = None

    def load_user(self):
        if os.path.exists(self.userfile):
            with open(self.userfile, 'r') as f:
                return json.load(f)
        self.users = {}

    def save_user(self):

        with open(self.userfile, 'w') as f:
            json.dump(self.users, f)

    def register_user(self, username, password):
        if username in self.users:
            return False, "用戶名已存在"
        self.users[username] = {'password': password}
        self.save_user()
        return True, "註冊成功"

    def login_user(self, username, password):
        if username in self.users and self.users[username]['password'] == password:
            self.current_user = username
            return True, "登錄成功"
        return False, "用戶名或密碼錯誤"


    