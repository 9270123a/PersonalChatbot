from openai import OpenAI
import os
from dotenv import load_dotenv


class Chatbot:
    def __init__(self, api_key, max_history=5, data_dir="./user_data"):

        load_dotenv()
        OpenAI.api_key = os.getenv("OPEN_API")

        self.openai = OpenAI
        self.model = "gpt-3.5-turbo"
        self.default_system_prompt = "You are a helpful assistant."

    def send_messenges(self, text):

        response = self.openai.chat.completions.create(
            model=self.model,
            messages=[
                {'role':'system', "content":self.default_system_prompt},
                {'role':'user','content':"我想跟聊天機器人說話"}
            ]

        )

        response_dict = response.to_dict()
        return response_dict['choices'][0]['message']['content']

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

        

