import os
import pickle
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from PyPDF2 import PdfReader
import docx

# Directories
UPLOAD_DIR = "uploads"
VECTOR_STORE_PATH = "vector_store/faiss_index"
EMBEDDINGS_CACHE = "vector_store/embeddings_cache.pkl"

os.makedirs(VECTOR_STORE_PATH, exist_ok=True)

# Load embedding model
print("Loading embedding model...")
embeddings_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Text splitter
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

# Read files
print("Reading files...")
all_texts = []

for filename in os.listdir(UPLOAD_DIR):
    file_path = os.path.join(UPLOAD_DIR, filename)
    text = ""

    if filename.lower().endswith(".txt"):
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            text = f.read()
    elif filename.lower().endswith(".pdf"):
        try:
            reader = PdfReader(file_path)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        except Exception as e:
            print(f"Failed to read PDF {filename}: {e}")
    elif filename.lower().endswith(".docx"):
        try:
            doc = docx.Document(file_path)
            for para in doc.paragraphs:
                text += para.text + "\n"
        except Exception as e:
            print(f"Failed to read DOCX {filename}: {e}")
    else:
        print(f"Skipping unsupported file: {filename}")
        continue

    if text.strip():
        all_texts.append(text)

# Split text into chunks
print("Splitting text into chunks...")
docs = text_splitter.create_documents(all_texts)
print(f"Total chunks created: {len(docs)}")

INDEX_FILE = os.path.join(VECTOR_STORE_PATH, "index.faiss")

if os.path.exists(INDEX_FILE):
    print("FAISS index already exists. Loading index...")
    vector_store = FAISS.load_local(
        VECTOR_STORE_PATH,
        embeddings_model,
        allow_dangerous_deserialization=True
    )
else:
    print("Creating FAISS index from documents...")
    vector_store = FAISS.from_documents(docs, embeddings_model)

    # Save FAISS index
    print("Saving FAISS index...")
    vector_store.save_local(VECTOR_STORE_PATH)
    print("FAISS vector store generated successfully!")


