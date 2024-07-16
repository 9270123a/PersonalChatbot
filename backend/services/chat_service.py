import models.chatbot
import models.user_management



class Chat_Service:
    
    
    def __init__(self):
        self.Chatbot = models.chatbot.Chatbot(username="user")
        
    def chat(self, text):
        
        message = self.Chatbot.send_messages(text)
        return message
    
    