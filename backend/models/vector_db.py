import faiss
import numpy as np
import pickle
import os
import sys
backend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, backend_path)
from utlities import ultis



class VectorDB:

    def __init__(self, data_dir="./user_data"):

        self.faiss_file = os.path.join(data_dir, "faiss_index")
        self.mapping_file = os.path.join(data_dir,"text_to_id")
        self.index = None
        self.text_to_id = {}
        self.load_and_create_faiss()
        self.load_and_create_mapping_file()

    def load_and_create_faiss(self):

        try:
            self.index = faiss.read_index(self.faiss_file)
            print(f"已加載faiss索引{self.faiss_file}")
        except:
            print(f"無法加載{self.faiss_file}已創建新的")
            dimension = 1536
            self.index = faiss.IndexFlatL2(dimension)
            
            empty_vector = np.zeros((1, dimension), dtype=np.float32)
            self.index.add(empty_vector)
            
            faiss.write_index(self.index, self.faiss_file)
            

    def load_and_create_mapping_file(self):

        try:
            with open(self.mapping_file, "rb") as f:
                self.text_to_id = pickle.load(f)
        
        except:
            with open(self.mapping_file, "wb") as f:
                pickle.dump(self.text_to_id, f)
                

            print(f"已創建並保存新的映射文件 {self.mapping_file}")


    def save_vectorDB(self, Chat_messenge):
    
        vector = ultis.text_to_vector(Chat_messenge)
        vector_np = np.array(vector).astype("float32")
        self.index.add(vector_np.reshape(1, -1))
        faiss.write_index(self.index, self.faiss_file)
        text_id = self.index.ntotal -1
        self.text_to_id [text_id] = Chat_messenge

        with open(self.mapping_file, "wb") as f:
            pickle.dump(self.text_to_id, f) 


    def load_VectorDB(self, query_text ,k=1 ):
        
        query_text_np = np.array(ultis.text_to_vector(query_text)).astype('float32').reshape(1, -1)


        
        distances,indices = self.index.search(query_text_np, k)
        result = {}
        if self.text_to_id is None or len(self.text_to_id) == 0:
            print("警告：text_to_id 为空或为 None，返回空结果")
            return result
    
        for idx, dist in zip(indices[0], distances[0]):
            if int(idx) in self.text_to_id:
                text = self.text_to_id[int(idx)]
                result.append((text, float(dist)))
            else:
                print(f"警告：索引 {idx} 在 text_to_id 中未找到")

        return result




