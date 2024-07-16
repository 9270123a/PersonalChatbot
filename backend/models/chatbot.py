from openai import OpenAI
import os , sys
from dotenv import load_dotenv
backend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, backend_path)
from .vector_db import VectorDB

class Chatbot:
    def __init__(self, username = "user"):

        load_dotenv()
        self.client = OpenAI(
            # This is the default and can be omitted
            api_key=os.environ.get("OPENAI_API_KEY"),
        )
        self.conversation_history = []
        self.model = "gpt-3.5-turbo"
        self.default_system_prompt = "You are a helpful assistant."
        self.username = username
        os.makedirs(f"./user_data_{self.username}", exist_ok=True)
        self.vc_db = VectorDB(f"./user_data_{self.username}")
        self.history_info =[]

    
    def send_messages(self, text = "hello"):

        
        relevant_info = self.vc_db.load_VectorDB(text)
        messages = [
            {'role':'system', "content":self.default_system_prompt},
            {'role':'system', "content": f"Relevant information: {relevant_info}"}
            
        ]
        messages.extend(self.history_info)
        messages.append({'role': 'user', 'content': text})
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages

        )

        response_dict = response.to_dict()
        assistant_message = response_dict['choices'][0]['message']['content']
        self.conversation_history.append({'role': 'user', 'content': text})
        self.conversation_history.append({'role': 'assistant', 'content': assistant_message})
        return assistant_message

    def create_system_prompt(self, pre_chat=-5):

        history_text = dict(list(self.chat_history.items())[pre_chat:])

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
        return response_dict['choices'][0]['message']['content']

        

