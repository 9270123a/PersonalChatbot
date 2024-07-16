import sys
import os
import pickle
# 將 backend 資料夾加入 Python 路徑
current_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.dirname(current_dir)
sys.path.append(backend_dir)

import models.chatbot
import models.vector_db
import models.user_management
import utlities.ultis


class SystemPrompt_Service:


    def __init__(self, update_interval=5):
        self.update_interval = update_interval
        self.current_prompt = "You are a helpful assistant."
        self.conversation_count = 0
        self.Chat = models.chatbot.Chatbot()
        self.Uts = utlities.ultis
        self.System_prompt = {}
        self.usermanage = models.user_management.UserManagement()
        self.username = self.usermanage.get_current_user()
        self.System_file = f"./user_data_{self.username}"

        self.load_and_create_System_Prompt()
        
        
        
    def load_and_create_System_Prompt(self):
        try:
            with open(self.System_file, "rb") as f:
                self.System_prompt = pickle.loads(f)
        except:
            with open(self.System_file, "wb") as f:
                pickle.dump(self.System_prompt, f)
        
        
    def count_chat_times(self):
        self.conversation_count+=1

    def refresh_count(self):
        self.conversation_count=0

    def update_prompt_periodically(self):
        if self.conversation_count >= self.update_interval:
            self.current_prompt = self.Chat.create_system_prompt()
        
        self.refresh_count()
        return self.current_prompt
        

    def get_current_prompt(self):

        return self.current_prompt

    def save_system_prompt(self):
        
        System_file = f"System_prompt{self.username}"
        self.Uts.save_pickle(self.current_prompt, System_file)
        return (f"以儲存成功{System_file}")



