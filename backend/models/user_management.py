import json
import os 
import faiss
import numpy as np
import pickle
# #將user存json，然後再到對應的資料夾取出過往的聊天紀錄
class UserManagement:


    def __init__(self, userfile = "user.json"):
        self.userfile = userfile
        self.users = self.load_user()
        self.current_user = None
        self.data_dir = None

    def get_data_dir(self):
        return self.data_dir
    
    def log_out(self):
        self.current_user = None

    def load_user(self):
        if os.path.exists(self.userfile):
            with open(self.userfile, 'r') as f:
                return json.load(f)
        return {} 

    def save_user(self):
        with open(self.userfile, 'w') as f:
            json.dump(self.users, f)

    def register_user(self, username, password):
        if username in self.users:
            return False, "用戶名已存在"
        self.users[username] = {'password': password}
        self.save_user()
        self.create_user_personal_data(username)
        return True, "註冊成功"
    
    def create_user_personal_data(self,username):
        self.data_dir = f"./user_data_{username}"
        os.makedirs(self.data_dir, exist_ok=True)
        self.create_userdata_faiss_systemprompt()

    def create_userdata_faiss_systemprompt(self):
        
        faiss_file = os.path.join(self.data_dir, "faiss_index")
        mapping_file = os.path.join(self.data_dir,"text_to_id")
        self.system_prompt_file = os.path.join(self.data_dir, "system_prompt.txt")
        #創建faiss檔案
        dimension = 1536
        index = faiss.IndexFlatL2(dimension)
        empty_vector = np.zeros((1, dimension), dtype=np.float32)
        index.add(empty_vector)
        faiss.write_index(index, faiss_file)
        
        #創建userdata
        text_to_id = {}
        with open(mapping_file, "wb") as f:
            pickle.dump(text_to_id, f)
        
        #創建system_prompt
        with open(self.system_prompt_file, "w") as f:
            f.write("Default system prompt")
    
    
    def login_user(self, username, password):
        if username in self.users and self.users[username]['password'] == password:
            self.current_user = username
            return True, "登錄成功"
        return False, "用戶名或密碼錯誤"

    
    def get_current_user(self):
        return self.current_user
    
    def set_current_user(self, username):
    
        print(self.current_user)
        self.current_user = username

    