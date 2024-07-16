import gradio as gr
import requests

API_URL = "http://localhost:5000"
current_user = None

def login(username, password):
    global current_user
    response = requests.post(f"{API_URL}/login", json={"username": username, "password": password})
    result = response.json()
    print(result)
    if result.get('success', False):
        current_user = username
        return result["message"], gr.update(visible=True)
    return result["message"], gr.update(visible=True)

def register(username , password):
    response = requests.post(f"{API_URL}/register", json={"username": username, "password": password})
    result = response.json()
    print(result)
    return result[1]

def chat(text):
    response = requests.post(f"{API_URL}/chat", json={"message": msg})
    result = response.json()
    return result["message"]

def SystemPrompt():
    response = requests.get(f"{API_URL}/systemprompt")
    result = response.json()
    return result

with gr.Blocks() as iface:
    gr.Markdown("# Chatbot with Login System")
    
    with gr.Tab("Login"):
        username_login = gr.Textbox(label="Username")
        password_login = gr.Textbox(label="Password", type="password")
        login_button = gr.Button("Login")
        login_output = gr.Textbox(label="Login Status")
        

    with gr.Tab("Register"):
        username_register = gr.Textbox(label="Username")
        password_register = gr.Textbox(label="Password", type="password")
        register_button = gr.Button("Register")
        register_output = gr.Textbox(label="Registration Status")
        

    with gr.Tab("Chat"):
        chatbot = gr.Chatbot()
        msg = gr.Textbox()
        system_prompt_display = gr.Textbox(label="System Prompt", interactive=False)
        clear = gr.Button("Clear")
        
    login_button.click(login, inputs = [username_login, password_login], outputs = [login_output, chatbot])
    register_button.click(register, inputs=[username_register, password_register], outputs = [register_output])
    msg.submit(chat, inputs=[msg, chatbot],outputs=[msg, chatbot])
    clear.click(lambda: None, None, chatbot, queue=False)
    login_button.click(SystemPrompt, outputs=system_prompt_display)
iface.launch()