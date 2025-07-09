from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
import util.util as util

# === 初始化 Text Splitter（使用遞迴式字元分割器）===
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=300,  # 每段 chunk 最長 300 個字元
    chunk_overlap=30,  # chunk 之間保留 30 個字元重疊，保留上下文連貫性
    separators=["\n\n", "。", "？", "?", "！", "!", "；", ";", "，", ",", "\n"]  # 預設分割符號，從大段到句到詞，遞迴 fallback
)

# === 檔案路徑設定 ===
file_path = r'./data/news.txt'  # 原始新聞資料
# file_path = r'./data/test.txt'
chunk_path = "./chunks/chunks.json"   # 分割後儲存的 chunks 路徑

# === 逐篇讀入新聞，轉換為 Document 格式 ===
news = ""            # 累積每篇新聞的內文
documents = []       # 儲存原始 Document 清單

with open(file_path, encoding="utf-8") as f:
    while True:
        date = f.readline()         # 讀取時間（每篇新聞第一行）
        if not date:                # 若已無資料，結束迴圈
            break
        title = f.readline()        # 讀取標題（第二行）
        aline = f.readline()        # 從第三行開始是新聞內文

        # 累積內文直到遇到分隔線
        while aline != "--------------------------\n":
            aline = aline[:-1] if aline[-1] == "\n" else aline  # 移除換行符
            news = news + aline
            aline = f.readline()

        # 將每篇新聞轉為 LangChain 的 Document 格式
        documents.append(Document(
            page_content=news,
            metadata={"date": date.strip(), "title": title.strip()}
        ))
        news = ""  # 清空內文，準備讀取下一篇

# === 使用 Text Splitter 對所有文件做 chunk 切割 ===
documents = text_splitter.split_documents(documents=documents)

# === 儲存結果到 JSON 檔案中 ===
util.save_document(chunk_path, documents)