from dotenv import load_dotenv
import openai
import os
import pickle





def text_to_vector(text, client):

    load_dotenv()
    openai.api_key = os.getenv('OPEN_API')
    response = client.embeddings.create(

        input = "text",
        model="text-embedding-ada-002"

    )

    return response.data[0].embedding




def save_pickle(text, file):
        
    with open(file, "wb") as f:
        pickle.dump(text, f)
    print("已存入", text)


def load_pickle(file):

    try:
        with open(file, "rb") as f:
            SystemPrompt = pickle.load(f)
    except:
            SystemPrompt= {}

    return SystemPrompt

