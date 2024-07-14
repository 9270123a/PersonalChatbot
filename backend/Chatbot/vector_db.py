import faiss
import numpy as np
import pickle
import os
import sys
backend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, backend_path)
from utlities import ultis



class VectorDB:

    def __init__(self,faiss_file = "faiss_index", mapping_file ="text_to_id"):

        self.faiss_file = faiss_file
        self.mapping_file = mapping_file
        
        self.load_and_create_faiss()
        self.load_and_create_mapping_file()

    def load_and_create_faiss(self):

        try:
            self.index = faiss.read_index(self.faiss_file)
            print(f"已加載faiss索引{self.faiss_file}")
        except:

            self.index = None
            print(f"已創建faiss索引{self.faiss_file}")

    def load_and_create_mapping_file(self):

        try:
            with open(self.mapping_file, "rb") as f:
                self.text_to_id = pickle.load(f)
        
        except:
            self.text_to_id ={}



    def save_vectorDB(self, Chat_messenge):
    
        vector = ultis.text_to_vector(Chat_messenge)
        vector_np = np.array(vector).astype("float32")
        d = vector_np.size
        self.index.add(vector_np.reshape(1, -1))
        faiss.write_index(self.index, self.faiss_file)
        text_id = self.index.ntotal -1
        self.text_to_id [text_id] = Chat_messenge

        with open(self.mapping_file, "wb") as f:
            pickle.dump(self.text_to_id, f) 


    def load_VectorDB(self, query_text ,k=1 ):
        query_text_np = np.array(ultis.text_to_vector(query_text)).astype('float32').reshape(1, -1)

        index = faiss.read_index(self.faiss_file)

        with open(self.mapping_file, "rb") as f:
            text_to_id = pickle.load(f)

        distances,indices = index.search(query_text_np, k)

        result = {}
        for idx, dist in zip(indices[0], distances[0]):
            text = text_to_id[int(idx)]
            result.append(text, dist)

        return result




