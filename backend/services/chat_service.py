import models.chatbot
import models.user_management
import utlities.ultis


class Chat_Service:
    
    
    def __init__(self, usermanagement,VectorDB, openai_client):
        self.usermanage = usermanagement
        self.VecDB = VectorDB
        self.Uts = utlities.ultis
        self.current_user = ""
        #chat邏輯
        self.Chatbot = models.chatbot.Chatbot(openai_client)
        
        #system_prompt邏輯
        
        self.conversation_count = 0
        self.current_prompt = "default"
        
    def chat(self, text):
        

        current_user = self.usermanage.get_current_user()
        self.current_user = current_user
        self.VecDB.set_user_dir(current_user)
        message = self.Chatbot.send_messages(text, self.VecDB)
        self.current_prompt = self.Chatbot.load_system_prompt(current_user)
        self.conversation_count+=1
        return message
    
    def get_and_update_prompt(self):
        if self.conversation_count >= 3:
            print("12312313123123123123123123")
            self.current_prompt = self.Chat.create_system_prompt()
            self.conversation_count=0
            self.Chatbot.save_system_prompt(self.current_prompt)
        self.current_prompt = self.Chatbot.load_system_prompt(self.current_user)
        print(self.current_prompt, "1111111111111111111111")
        return self.current_prompt
    
        
    