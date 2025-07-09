import json
from langchain.schema import Document

# === 將分割後的 Document 物件儲存為 JSON 檔案 ===
def save_document(path, documents):
    """
    將 List[Document] 轉為 JSON 並寫入檔案。
    
    Args:
        path (str): 儲存路徑
        documents (List[Document]): LangChain 的 Document 物件清單
    """
    data = []
    for doc in documents:
        temp = {
            "metadata": {
                "date": doc.metadata.get("date"),
                "title": doc.metadata.get("title")
            },
            "page_content": doc.page_content
        }
        data.append(temp)
    
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)  # indent=2 讓格式較好閱讀

# === 從 JSON 檔案讀取並還原為 Document 物件 ===
def load_document(path):
    """
    從 JSON 檔案讀取並還原為 List[Document]。
    
    Args:
        path (str): JSON 檔案路徑
    
    Returns:
        List[Document]
    """
    with open(path, "r", encoding="utf-8") as f:
        documents = json.load(f)

    # 轉回 Document 物件
    return [
        Document(page_content=d["page_content"], metadata=d["metadata"])
        for d in documents
    ]