import os
import time
from pathlib import Path
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from PyPDF2 import PdfReader
import docx

# =====================================
# PROJECT ROOT (outside scripts folder)
# =====================================

BASE_DIR = Path(__file__).resolve().parent.parent  # project root

UPLOAD_DIR = BASE_DIR / "uploads"
VECTOR_STORE_PATH = BASE_DIR / "vector_store"
FAISS_INDEX_PATH = VECTOR_STORE_PATH / "faiss_index"

UPLOAD_DIR.mkdir(exist_ok=True)
VECTOR_STORE_PATH.mkdir(exist_ok=True)

# =====================================
# LOAD EMBEDDING MODEL
# =====================================

print("🔄 Loading embedding model...")
start_time = time.time()

embeddings_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

print(f"✅ Embedding model loaded in {round(time.time() - start_time, 2)} sec\n")

# =====================================
# TEXT SPLITTER
# =====================================

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

# =====================================
# LOAD EXISTING FAISS INDEX
# =====================================

vector_store = None

if (FAISS_INDEX_PATH / "index.faiss").exists():
    print("📦 Loading existing FAISS index...")
    vector_store = FAISS.load_local(
        str(FAISS_INDEX_PATH),
        embeddings_model,
        allow_dangerous_deserialization=True
    )
    print("✅ Existing index loaded\n")
else:
    print("🆕 No existing index found. A new one will be created.\n")

# =====================================
# GET LATEST FILE ONLY
# =====================================

files = [
    f for f in UPLOAD_DIR.iterdir()
    if f.is_file() and f.suffix.lower() in [".txt", ".pdf", ".docx"]
]

if not files:
    print("❌ No files found in uploads folder.")
    exit()

latest_file = max(files, key=lambda f: f.stat().st_mtime)

print(f"📄 Latest file detected: {latest_file.name}")

# =====================================
# FILE READER
# =====================================

def read_file(file_path):
    text = ""

    if file_path.suffix.lower() == ".txt":
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            text = f.read()

    elif file_path.suffix.lower() == ".pdf":
        reader = PdfReader(str(file_path))
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"

    elif file_path.suffix.lower() == ".docx":
        doc = docx.Document(str(file_path))
        for para in doc.paragraphs:
            text += para.text + "\n"

    return text


# =====================================
# PROCESS FILE
# =====================================

print("🔄 Reading file...")
text = read_file(latest_file)

if not text.strip():
    print("❌ File is empty or unreadable.")
    exit()

print("✂️ Splitting into chunks...")
chunks = text_splitter.split_text(text)
total_chunks = len(chunks)

print(f"📊 Total chunks generated: {total_chunks}\n")

if total_chunks == 0:
    print("❌ No chunks generated.")
    exit()

# =====================================
# ADD TO FAISS WITH PROGRESS
# =====================================

print("🧠 Generating embeddings & updating FAISS index...\n")
start_time = time.time()

BATCH_SIZE = 32  # Improve speed

for i in range(0, total_chunks, BATCH_SIZE):
    batch = chunks[i:i + BATCH_SIZE]

    if vector_store is None:
        vector_store = FAISS.from_texts(batch, embeddings_model)
    else:
        vector_store.add_texts(batch)

    processed = min(i + BATCH_SIZE, total_chunks)
    percent = round((processed / total_chunks) * 100, 2)

    print(f"Progress: {processed}/{total_chunks} chunks ({percent}%)")

# =====================================
# SAVE FAISS INDEX
# =====================================

print("\n💾 Saving FAISS index...")
vector_store.save_local(str(FAISS_INDEX_PATH))

print(f"\n✅ Done!")
print(f"⏱ Total processing time: {round(time.time() - start_time, 2)} sec")
print(f"📂 Index saved at: {FAISS_INDEX_PATH}")
