import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.document_loaders import PyPDFLoader, TextLoader, Docx2txtLoader

# 1️⃣ Path to uploaded file
UPLOAD_DIR = "uploads"
file_name = "About_Dogs.pdf"  # Replace with your uploaded file
file_path = os.path.join(UPLOAD_DIR, file_name)

# 2️⃣ Load file based on type
def load_file(file_path: str):
    ext = file_path.split(".")[-1].lower()
    if ext == "pdf":
        loader = PyPDFLoader(file_path)
    elif ext == "txt":
        loader = TextLoader(file_path)
    elif ext == "docx":
        loader = Docx2txtLoader(file_path)
    else:
        raise ValueError("Unsupported file type")
    
    return loader.load()  # Returns list of documents

documents = load_file(file_path)

# 3️⃣ Split into smaller chunks for better retrieval
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
    length_function=len
)
docs = text_splitter.split_documents(documents)

# 4️⃣ Create embeddings using Hugging Face model
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# 5️⃣ Store vectors in FAISS
vector_store = FAISS.from_documents(docs, embeddings)

# 6️⃣ Save FAISS index locally
VECTOR_STORE_PATH = "vector_store/faiss_index"
os.makedirs("vector_store", exist_ok=True)
vector_store.save_local(VECTOR_STORE_PATH)

print(f"File '{file_name}' processed and embeddings stored in '{VECTOR_STORE_PATH}'")
