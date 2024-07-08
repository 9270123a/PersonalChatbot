from openai import OpenAI
from backend.vector_db import VectorDatabase, VectorDatabaseManager
import os



class Chatbot:
    def __init__(self, api_key, model="gpt-3.5-turbo", max_history=5, data_dir="./user_data"):

        self.client = OpenAI(api_key=api_key)
        self.model = model
        
        self.default_system_prompt = "You are a helpful assistant."
        self.data_dir = data_dir

        dimension = 1536  # 或者你获取 dimension 值的代码

        os.makedirs(self.data_dir, exist_ok=True)

        # 使用持久化的存儲路徑初始化 VectorDatabaseManager
        self.db_manager = VectorDatabaseManager(dimension=dimension, base_path=self.data_dir)
        
        self.user_histories = {}
        self.load_user_histories()





    def generate_response(self, username: str, message: str):
        
        history = self.get_user_history(username)
        
        current_system_prompt = self.get_user_system_prompt(username)
        if self.should_update_system_prompt(username, message, history):
            system_prompt = self.generate_system_prompt(username, message, history)
        else:
            system_prompt = current_system_prompt
        
        message_embedding = self.get_embedding(message)
        relevant_contexts = self.db_manager.search(username, message_embedding, k=2)

        messages = [
            {"role": "system", "content": system_prompt}
        ]
        print("System message content:", messages[0]['content'])

        # 添加相关上下文
        for _, context, _ in relevant_contexts:
            context_message = {"role": "system", "content": f"Relevant context: {context}"}
            messages.append(context_message)
            print("Context message content:", context_message['content'])

        # 使用新的 process_history 函数处理历史记录
        recent_history = history[-self.max_history:]
        messages.extend(self.process_history(recent_history))

        # 打印处理后的历史消息（可选，用于调试）
        for msg in messages:
            if msg['role'] != 'system':
                print(f"{msg['role'].capitalize()} message content: {msg['content']}")

        current_user_message = {"role": "user", "content": message}
        messages.append(current_user_message)
        print("Current user message content:", current_user_message['content'])

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages
        )

        ai_message = response.choices[0].message.content
        print("AI response content:", ai_message)

        # 将新的对话添加到向量数据库
        self.db_manager.add_texts(username, [message, ai_message],
                                  [self.get_embedding(message), self.get_embedding(ai_message)])
        if system_prompt != current_system_prompt:
            self.set_user_system_prompt(username, system_prompt)

        return ai_message, system_prompt    
        
    def get_embedding(self, text):
        response = self.client.embeddings.create(input=text, model="text-embedding-ada-002")
        return response.data[0].embedding
