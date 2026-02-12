import os
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from PyPDF2 import PdfReader
import docx

# Directories
UPLOAD_DIR = "uploads"
VECTOR_STORE_PATH = "vector_store/faiss_index"
CHUNK_OUTPUT_FILE = "vector_store/chunks.txt"

os.makedirs(VECTOR_STORE_PATH, exist_ok=True)

# Load embedding model
print("Loading embedding model...")
embeddings_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Text splitter
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

# Open chunk file for writing
chunk_file = open(CHUNK_OUTPUT_FILE, "w", encoding="utf-8")

INDEX_FILE = os.path.join(VECTOR_STORE_PATH, "index.faiss")

# Initialize FAISS index
if os.path.exists(INDEX_FILE):
    print("Loading existing FAISS index...")
    vector_store = FAISS.load_local(
        VECTOR_STORE_PATH,
        embeddings_model,
        allow_dangerous_deserialization=True
    )
else:
    print("Creating new FAISS index...")
    vector_store = FAISS(embedding_function=embeddings_model)

def read_file(file_path, filename):
    """Extract text from txt, pdf, docx."""
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

    return text


print("Processing files...")

# STREAM chunks → FAISS
for filename in os.listdir(UPLOAD_DIR):
    file_path = os.path.join(UPLOAD_DIR, filename)

    print(f"Processing: {filename}")
    text = read_file(file_path, filename)

    if not text.strip():
        print(f"Skipped empty/unreadable file: {filename}")
        continue

    # Split into chunks
    chunks = text_splitter.split_text(text)

    # Save chunks into text file (viewable)
    for chunk in chunks:
        chunk_file.write(chunk + "\n---CHUNK-END---\n")

    # Stream chunks into FAISS
    vector_store.add_texts(chunks)

chunk_file.close()
print(f"Chunks saved to {CHUNK_OUTPUT_FILE}")

# Save FAISS index
print("Saving FAISS index...")
vector_store.save_local(VECTOR_STORE_PATH)

print("FAISS vector store generated successfully!")
