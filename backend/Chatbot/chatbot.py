from openai import OpenAI
from backend.vector_db import VectorDatabase, VectorDatabaseManager
import json
from typing import List
import os
class Chatbot:
    def __init__(self, api_key, model="gpt-3.5-turbo", max_history=5, data_dir="./user_data"):

        self.client = OpenAI(api_key=api_key)
        self.model = model
        self.max_history = max_history
        self.default_system_prompt = "You are a helpful assistant."
        self.data_dir = data_dir

        dimension = 1536  # 或者你获取 dimension 值的代码

        os.makedirs(self.data_dir, exist_ok=True)

        # 使用持久化的存儲路徑初始化 VectorDatabaseManager
        self.db_manager = VectorDatabaseManager(dimension=dimension, base_path=self.data_dir)
        
        self.user_histories = {}
        self.load_user_histories()

    def load_user_histories(self):
        
        for username in os.listdir(self.data_dir):
            user_dir = os.path.join(self.data_dir, username)
            if os.path.isdir(user_dir):
                history_file = os.path.join(user_dir, "history.json")
                if os.path.exists(history_file):
                    with open(history_file, 'r') as f:
                        self.user_histories[username] = json.load(f)
    def get_user_system_prompt(self, username: str) -> str:
        embedding = self.get_embedding(self.db_manager.system_prompt_key)
        prompt = self.db_manager.get_system_prompt(username, embedding)
        if prompt is None:
            prompt = self.default_system_prompt
        print(f"Retrieved system prompt for user {username}: {prompt[:30]}...")
        return prompt
    def should_update_system_prompt(self, username: str, message: str, history: List) -> bool:
        # 每三條對話更新一次 system prompt
        return len(history) % 3 == 2
    def set_user_system_prompt(self, username: str, system_prompt: str):
        embedding = self.get_embedding(system_prompt)
        self.db_manager.add_texts(username, [self.db_manager.system_prompt_key], [embedding])
        print(f"Setting system prompt for user {username}: {system_prompt[:30]}...")
    def get_user_history(self, username: str) -> List:
        if username not in self.user_histories:
            history_file = f"./user_data/{username}/history.json"
            if os.path.exists(history_file):
                with open(history_file, 'r') as f:
                    self.user_histories[username] = json.load(f)
            else:
                self.user_histories[username] = []
        return self.user_histories[username]
    def add_to_user_history(self, username: str, user_message: str, ai_message: str):
        history = self.get_user_history(username)
        history.append((user_message, ai_message))
        if len(history) > self.max_history:
            history.pop(0)
        history_file = f"./user_data/{username}/history.json"
        with open(history_file, 'w') as f:
            json.dump(history, f)
    def process_history(self, history):

        processed_messages = []
        for h in history:
            if len(h) == 2:
                user_content = h[0] if h[0] is not None else "(No message)"
                processed_messages.append({"role": "user", "content": user_content})
                if h[1] is not None:
                    processed_messages.append({"role": "assistant", "content": h[1]})
        return processed_messages
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
    def generate_system_prompt(self, username: str, message: str, history: List):
        message_embedding = self.get_embedding(message)
        relevant_contexts = self.db_manager.search(username, message_embedding, k=5)
        
        # 準備生成 system prompt 的輸入
        context_text = "\n".join([context for _, context, _ in relevant_contexts])
        history_text = "\n".join([f"User: {h[0]}\nAssistant: {h[1]}" for h in history[-self.max_history:]])
        
        prompt = f"""Based on the following context and conversation history, generate a system prompt for an AI assistant. The system prompt should guide the AI to adapt its tone, expertise, and personality to best suit the user's needs and the conversation context.

Context:
{context_text}

Conversation History:
{history_text}

Current User Message:
{message}

Generate a system prompt that will help the AI assistant respond appropriately:"""

        # 使用 OpenAI API 生成 system prompt
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",  # 或者使用更強大的模型如 "gpt-4"
            messages=[
                {"role": "system", "content": "You are a helpful AI that generates system prompts for other AI assistants."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150  # 限制 system prompt 的長度
        )

        
        return response.choices[0].message.content.strip()
    