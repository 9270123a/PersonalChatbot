from typing import List


class System_prompt:

    def __init__(self):
        Chatbot
    
    def get_user_system_prompt(self, username: str) -> str:
        embedding = self.get_embedding(self.db_manager.system_prompt_key)
        prompt = self.db_manager.get_system_prompt(username, embedding)
        if prompt is None:
            prompt = self.default_system_prompt
        print(f"Retrieved system prompt for user {username}: {prompt[:30]}...")
        return prompt
    
    def set_user_system_prompt(self, username: str, system_prompt: str):
        embedding = self.get_embedding(system_prompt)
        self.db_manager.add_texts(username, [self.db_manager.system_prompt_key], [embedding])
        print(f"Setting system prompt for user {username}: {system_prompt[:30]}...")

    def should_update_system_prompt(self, username: str, message: str, history: List) -> bool:
        # 每三條對話更新一次 system prompt
        return len(history) % 3 == 2
    
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
    
