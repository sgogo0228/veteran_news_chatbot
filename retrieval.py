# === 套件載入 ===
from sentence_transformers import SentenceTransformer  # 句子向量轉換
import faiss                                           # 向量檢索工具
import numpy as np
from transformers import pipeline                      # 文字生成模型 pipeline
import chinese_converter                               # 簡繁轉換
import util.util as util                               # 自訂 util 函式

# === 模型與資料初始化 ===
model_ckpt = "sentence-transformers/all-MiniLM-L6-v2"
embedding_model = SentenceTransformer(model_ckpt)      # 載入語意嵌入模型

chunk_path = "./chunks/chunks.json"                    # 已儲存的 chunk 文件
documents = util.load_document(chunk_path)             # 載入 chunk 資料

vector_path = "./vector_store/my_index.faiss"          # 讀取vector_build.py生成並儲存的vector store
index = faiss.read_index(vector_path)                  # 載入向量索引

llm = pipeline("text-generation", model="unsloth/Qwen2.5-3B")  # 載入文字生成LLM

# === 查詢與向量檢索 ===
query = "近期在屏東是否有發生磷酸液體洩漏事件"          # 使用者查詢問題
query_embedding = embedding_model.encode(query, convert_to_tensor=False)  # 將問題轉成向量
distances, indices = index.search(np.array([query_embedding]), k=3)  # 在vectore store進行相似度搜尋，取前3個結果

# === 生成 Prompt ===
context = ""
for i in range(len(indices[0])):  # 將檢索結果的片段整理成 Prompt
    context = context + f"{i+1}. {documents[indices[0, i]].page_content[2:]}\n"

prompt = f"根據以下新聞片段回答問題：\n\n{context}\n問題：{query}\n回答："
prompt = chinese_converter.to_simplified(prompt)  # 轉換為簡體（訓練資料中較多簡中資源，表現較好）

# print(f"question: {prompt}\n")  # 印出完整 Prompt（for debug）

# === 文字生成與回應 ===
response = llm(prompt, max_length=200)  # 產生回答
print(chinese_converter.to_traditional(response[0]["generated_text"]))  # 顯示為繁體中文