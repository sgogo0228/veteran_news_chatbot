# veteran_news_chatbot | 榮院新聞聊天機器人  

This project builds an LLM-based Retrieval-Augmented Generation (RAG) system for semantic search and document querying. It uses natural language processing techniques to segment raw news articles into semantic chunks, generates sentence embeddings using a Sentence-Transformer model, and constructs a FAISS vector database for approximate nearest neighbor search. When a user inputs a query, the system computes the most semantically relevant text chunks based on vector similarity and passes them as contextual information to a language generation model to produce an answer.  
本專案建構了一個基於LLM/RAG系統，用於語意檢索（Semantic Search）的檔案查詢系統。主要透過自然語言處理技術，將原始新聞切分為語意片段（Chunking），並利用Sentence-transformer模型產生向量表示，接著透過FAISS建立向量資料庫以進行近似查詢。使用者輸入問題後，系統將根據句子的語意向量自動計算最相關的語意片段，將這些語意片段作為額外資訊交由語言生成模型產生回答。

---

## Structure
```
veteran_news_chatbot/  
├── chunks/                     # 儲存切分後的語意片段
│   └── chunks.json             # 切分後的新聞文本與 metadata
├── data/                       # 原始新聞資料
│   ├── news.txt                # 主要新聞文本
│   └── test.txt                # 測試用新聞文本
├── util/                       # 工具函式
│   └── util.py                 # 儲存與讀取 document 的工具
├── vector_store/              # 向量資料庫
│   └── my_index.faiss         # FAISS 建立的向量索引檔
├── chunking.py                # 將新聞資料切成語意片段並儲存
├── news_crawler.py            # 擷取新聞內容的爬蟲
├── retrieval.py               # 根據 query 進行語意檢索與回答生成  
├── vector_build.py            # 建立句向量並儲存至 FAISS  
└── README.md                  # 專案說明文件
```
