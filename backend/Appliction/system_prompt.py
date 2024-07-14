import Chatbot.chatbot
import Chatbot.vector_db



class System_prompt:


    def __init__(self, update_interval=5):
        self.update_interval = update_interval
        self.current_prompt = ""
        self.conversation_count = 0
        self.Chat = Chatbot.chatbot.Chatbot

    def count_chat_times(self):
        self.conversation_count+=1

    def refresh_count(self):
        self.conversation_count=0

    def update_prompt_periodically(self):
        if self.conversation_count >= self.update_interval:
            self.Chat.create_system_prompt()
        
        

    def get_current_prompt(self):
        return self.current_prompt

    def save_system_prompt(self, prompt):
        self.current_prompt = prompt




