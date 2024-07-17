from openai import OpenAI
import os , sys
from dotenv import load_dotenv
backend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, backend_path)
from models.vector_db import VectorDB
import utlities.ultis
class Chatbot:
    def __init__(self, openai_client):

        load_dotenv()
        self.client = openai_client
        self.conversation_history = []
        self.model = "gpt-3.5-turbo"
        self.system_prompt= ""
    
    def send_messages(self, text, VecDB):


        relevant_info = VecDB.load_VectorDB(text)
        messages = [
            {'role':'system', "content":self.system_prompt},
            {'role':'system', "content": f"Relevant information: {relevant_info}"}
            
        ]
        messages.append({'role': 'user', 'content': text})
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages

        )

        response_dict = response.to_dict()
        assistant_message = response_dict['choices'][0]['message']['content']
        self.conversation_history.append({'role': 'user', 'content': text})
        self.conversation_history.append({'role': 'assistant', 'content': assistant_message})
        VecDB.save_vectorDB(text)
        VecDB.save_vectorDB(assistant_message)
        return assistant_message

            
                 
    def create_system_prompt(self, pre_chat=-5):
        
        history_item = utlities.ultis.load_pickle(self.System_file)
        
        history_text = dict(list(history_item.items())[pre_chat:])

        prompt = f"""基於以下上下文和對話歷史，為 AI 助手生成一個系統提示。該系統提示應指導 AI 調整語氣、專業知識和個性，以最佳方式滿足使用者的需求和對話上下文。

    對話歷史：
    {history_text}

    生成一個系統提示，以幫助 AI 助手做出適當的回應："""
        response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",  
                messages=[
                    {"role": "system", "content": "你是一个为其他 AI 助手生成系统提示的有用 AI"},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=150  
            )



        response_dict = response.to_dict()
        self.default_system_prompt = response_dict
        print("已創建新的system_prompt")

        
    def save_system_prompt(self, current_prompt, current_user):
        
        system_file = f"/user_data_{current_user}/system_prompt.txt"
        with open(system_file, 'w', encoding='utf-8') as file:
            file.write(current_prompt)
        return f"已成功儲存 {system_file}"

    def load_system_prompt(self, current_user):
        system_file = f"./user_data_{current_user}/system_prompt.txt"
        
        with open(system_file, 'r', encoding='utf-8') as file:
            self.system_prompt = file.read().strip()
        return self.system_prompt