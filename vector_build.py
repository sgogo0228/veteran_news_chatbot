from sentence_transformers import SentenceTransformer    # 句子向量轉換
import faiss                # 向量檢索工具
import numpy as np
import util.util as util    # 自訂工具模組，內含 load_document 等函式

# === 載入模型與文件 ===
model_ckpt = "sentence-transformers/all-MiniLM-L6-v2"
embedding_model = SentenceTransformer(model_ckpt)  # 載入語意嵌入模型

chunk_path = "./chunks/chunks.json"                # 本地端的文本段落檔案
documents = util.load_document(chunk_path)         # 載入已切好的文本段落（List[Document]）

# === 將文本轉為向量 ===
texts = [chunk.page_content for chunk in documents]  # 提取每段 chunk 的純文本部分
embeddings = embedding_model.encode(
    texts,
    convert_to_tensor=True,        # 轉成tensor，可與 PyTorch 整合
    show_progress_bar=True         # 顯示進度條
)
embeddings_np = embeddings.cpu().detach().numpy()    # 轉為 NumPy 格式供 FAISS 使用

# === 建立 FAISS vector store ===
index = faiss.IndexFlatL2(embeddings_np.shape[1])  # 建立 L2 向量空間索引器
index.add(embeddings_np)                           # 將語意向量加入vector store

# === 建立 index 對應的原始文件對照表===
id_to_doc = {i: documents[i] for i in range(len(documents))}  # 用於查詢到的chunk的日期與新聞標題

# === 輸出vector store到local端 (模組化) ===
vector_path = "./vector_store/my_index.faiss"
faiss.write_index(index, vector_path)