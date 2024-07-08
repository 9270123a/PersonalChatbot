import json
import os
from typing import List


class History:


    def __init__(self, max_history = 5):

        self.max_history = max_history


    def load_user_histories(self):

        for username in os.listdir(self.data_dir):
            user_dir = os.path.join(self.data_dir, username)
            if os.path.isdir(user_dir):
                history_file = os.path.join(user_dir, "history.json")
                if os.path.exists(history_file):
                    with open(history_file, 'r') as f:
                        self.user_histories[username] = json.load(f)


    def get_user_history(self, username: str) -> List:
            if username not in self.user_histories:
                history_file = f"./user_data/{username}/history.json"
                if os.path.exists(history_file):
                    with open(history_file, 'r') as f:
                        self.user_histories[username] = json.load(f)
                else:
                    self.user_histories[username] = []
            return self.user_histories[username]
        
    def process_history(self, history):

        processed_messages = []
        for h in history:
            if len(h) == 2:
                user_content = h[0] if h[0] is not None else "(No message)"
                processed_messages.append({"role": "user", "content": user_content})
                if h[1] is not None:
                    processed_messages.append({"role": "assistant", "content": h[1]})
        return processed_messages

    def add_to_user_history(self, username: str, user_message: str, ai_message: str):

        history = self.get_user_history(username)
        history.append((user_message, ai_message))
        if len(history) > self.max_history:
            history.pop(0)
        history_file = f"./user_data/{username}/history.json"
        with open(history_file, 'w') as f:
            json.dump(history, f)