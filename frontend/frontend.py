import gradio as gr
import requests

API_URL = "http://localhost:5000"
current_user = None

def register(username, password):
    response = requests.post(f"{API_URL}/register", json={"username": username, "password": password})
    return response.json()['message']

def login(username, password):
    global current_user
    response = requests.post(f"{API_URL}/login", json={"username": username, "password": password})
    if response.json()['success']:
        current_user = username
        system_prompt = response.json()['system_prompt']
        return response.json()['message'], system_prompt, gr.update(visible=True)
    return response.json()['message'], "", gr.update(visible=False)


def get_system_prompt(username):
    response = requests.get(f"{API_URL}/get_system_prompt", json={"username": username})
    return response.json()['system_prompt']

def update_chat_tab(login_message, system_prompt):
    if "success" in login_message.lower():
        return gr.update(value=system_prompt)
    return gr.update()

def chat(message, history):
    if not current_user:
        return "Please login first.", "", history
    response = requests.post(f"{API_URL}/chat", json={'message': message, 'history': history, 'username': current_user})
    ai_message = response.json()['response']
    system_prompt = response.json()['system_prompt']
    history.append((message, ai_message))
    return "", system_prompt, history

with gr.Blocks() as iface:
    gr.Markdown("# Chatbot with Login System")
    
    with gr.Tab("Login"):
        username_login = gr.Textbox(label="Username")
        password_login = gr.Textbox(label="Password", type="password")
        login_button = gr.Button("Login")
        login_output = gr.Textbox(label="Login Status")
        login_button.click(login, inputs=[username_login, password_login], outputs=login_output)

    with gr.Tab("Register"):
        username_register = gr.Textbox(label="Username")
        password_register = gr.Textbox(label="Password", type="password")
        register_button = gr.Button("Register")
        register_output = gr.Textbox(label="Registration Status")
        register_button.click(register, inputs=[username_register, password_register], outputs=register_output)

    with gr.Tab("Chat"):
        chatbot = gr.Chatbot()
        msg = gr.Textbox()
        system_prompt_display = gr.Textbox(label="System Prompt", interactive=False)
        clear = gr.Button("Clear")
        
        msg.submit(chat, inputs=[msg, chatbot], outputs=[msg, system_prompt_display, chatbot])
        clear.click(lambda: (None, None, None), None, [msg, system_prompt_display, chatbot], queue=False)
    login_button.click(
    login,
    inputs=[username_login, password_login],
    outputs=[login_output, system_prompt_display, system_prompt_display]
)
iface.launch()