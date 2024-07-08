import faiss
import numpy as np
import json
import os
from typing import List, Tuple, Optional
class VectorDatabase:
    def __init__(self, dimension: int, index_file: str = "faiss_index.idx", text_file: str = "text_data.json"):

        if not isinstance(dimension, int):
            raise TypeError("Dimension must be an integer")

        self.dimension = dimension
        self.index_file = index_file
        self.text_file = text_file
        self.system_prompt_key = "SYSTEM_PROMPT"
        self.system_prompt_id = -1  # 使用特殊的ID來標識系統提示

        if os.path.exists(self.index_file):
            self.index = faiss.read_index(self.index_file)
        else:
            self.index = faiss.IndexFlatL2(dimension)
        
        if os.path.exists(self.text_file):
            with open(self.text_file, 'r') as f:
                self.id_to_text = json.load(f)
            self.id_counter = max((int(k) for k in self.id_to_text.keys() if k.isdigit()), default=0)
        else:
            self.id_to_text = {}
            self.id_counter = 0

    def add_texts(self, texts: List[str], embeddings: List[List[float]]) -> List[int]:
        if len(texts) != len(embeddings):
            raise ValueError("Number of texts and embeddings must match")
        
        vectors = np.array(embeddings).astype('float32')
        ids = []
        for i, text in enumerate(texts):
            if text == self.system_prompt_key:
                self.id_to_text[str(self.system_prompt_id)] = text
                ids.append(self.system_prompt_id)


            else:
                self.id_counter += 1
                self.id_to_text[str(self.id_counter)] = text
                ids.append(self.id_counter)
        
        self.index.add(vectors)
        self._save_data()
        return ids

    def search(self, query_vector: List[float], k: int = 5) -> List[Tuple[int, str, float]]:
        query_vector = np.array([query_vector]).astype('float32')
        distances, indices = self.index.search(query_vector, k)
        if self.index.ntotal == 0:
            print("Warning: Vector database is empty")
            return []
        results = []
        for i, idx in enumerate(indices[0]):
            if idx != -1:  # FAISS uses -1 for empty slots
                try:
                    id_str = str(idx)
                    text = self.id_to_text[id_str]
                    results.append((idx, text, float(distances[0][i])))
                except KeyError:
                    print(f"Warning: No text found for index {idx}")
        return results

    def _save_data(self):
        faiss.write_index(self.index, self.index_file)
        with open(self.text_file, 'w') as f:
            json.dump(self.id_to_text, f)

    def get_system_prompt(self,embedding: List[float]) -> Optional[str]:
        results = self.search(embedding, k=1)
        if results and results[0][1] == self.system_prompt_key:
            return self.id_to_text.get(str(self.system_prompt_id))
        return None


class VectorDatabaseManager:
    def __init__(self, dimension: int, base_path: str = "./user_data"):
        self.dimension = dimension
        self.base_path = base_path
        self.user_dbs = {}
        self.system_prompt_key = "SYSTEM_PROMPT"

    
    def get_system_prompt(self, username: str, embedding: List[float]) -> Optional[str]:
        user_db = self.get_user_db(username)
        return user_db.get_system_prompt(embedding)

    def get_user_db(self, username: str) -> VectorDatabase:
        if username not in self.user_dbs:
            user_path = os.path.join(self.base_path, username)
            os.makedirs(user_path, exist_ok=True)
            index_file = os.path.join(user_path, "faiss_index.idx")
            text_file = os.path.join(user_path, "text_data.json")
            self.user_dbs[username] = VectorDatabase(self.dimension, index_file, text_file)
        return self.user_dbs[username]

    def search(self, username: str, query_vector: List[float], k: int = 5) -> List[Tuple[int, str, float]]:
        user_db = self.get_user_db(username)
        return user_db.search(query_vector, k)

    def add_texts(self, username: str, texts: List[str], embeddings: List[List[float]]) -> List[int]:
        user_db = self.get_user_db(username)
        return user_db.add_texts(texts, embeddings)