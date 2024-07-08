from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import VectorStoreRetrieverMemory
from langchain.prompts import PromptTemplate
import openai
import ray

class UserProfile:
    def __init__(self, user_id):
        self.user_id = user_id
        self.vector_store = FAISS.from_texts([], OpenAIEmbeddings())
        self.retriever = self.vector_store.as_retriever()
        self.memory = VectorStoreRetrieverMemory(retriever=self.retriever)

    def update_profile(self, text):
        self.vector_store.add_texts([text])

class EmotionAnalyzer:
    def analyze(self, text):
        # 使用OpenAI API进行情感分析
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=f"Analyze the emotion and tone in this text: {text}\nEmotion:",
            max_tokens=60
        )
        return response.choices[0].text.strip()

class PromptGenerator:
    def generate(self, emotion, tone):
        template = f"You are a chatbot that responds with {emotion} emotion and {tone} tone. " \
                   "Respond to the user's message: {message}"
        return PromptTemplate(template=template, input_variables=["message"])

class ChatbotServer:
    def __init__(self, server_type):
        self.server_type = server_type
        self.llm = ChatOpenAI(temperature=0.7)

    def respond(self, prompt, message):
        chain = ConversationalRetrievalChain.from_llm(self.llm, self.retriever)
        return chain.run(prompt.format(message=message))

@ray.remote
class ChatbotSystem:
    def __init__(self):
        self.user_profiles = {}
        self.emotion_analyzer = EmotionAnalyzer()
        self.prompt_generator = PromptGenerator()
        self.servers = {
            "gentle": ChatbotServer("gentle"),
            "sassy": ChatbotServer("sassy"),
            "classical": ChatbotServer("classical")
        }

    def register_user(self, user_id, initial_info):
        if user_id not in self.user_profiles:
            self.user_profiles[user_id] = UserProfile(user_id)
        self.user_profiles[user_id].update_profile(initial_info)

    def chat(self, user_id, message):
        profile = self.user_profiles[user_id]
        profile.update_profile(message)
        
        emotion = self.emotion_analyzer.analyze(message)
        prompt = self.prompt_generator.generate(emotion, "neutral")
        
        server = self.choose_server(emotion)
        response = server.respond(prompt, message)
        
        profile.update_profile(response)
        return response

    def choose_server(self, emotion):
        if "happy" in emotion or "calm" in emotion:
            return self.servers["gentle"]
        elif "angry" in emotion or "frustrated" in emotion:
            return self.servers["sassy"]
        else:
            return self.servers["classical"]

# 初始化Ray
ray.init()

# 创建ChatbotSystem Actor
chatbot_system = ChatbotSystem.remote()

# 使用示例
user_id = "user123"
ray.get(chatbot_system.register_user.remote(user_id, "I'm a new user who likes technology."))
response = ray.get(chatbot_system.chat.remote(user_id, "Hello, how are you today?"))
print(response)