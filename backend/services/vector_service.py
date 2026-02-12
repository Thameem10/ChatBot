import time
from pathlib import Path
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from PyPDF2 import PdfReader
import docx
import threading

BASE_DIR = Path(__file__).resolve().parent.parent
VECTOR_STORE_PATH = BASE_DIR / "vector_store"
FAISS_INDEX_PATH = VECTOR_STORE_PATH / "faiss_index"

VECTOR_STORE_PATH.mkdir(exist_ok=True)

embeddings_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

class VectorService:

    progress = 0
    status = "idle"
    time_taken = 0
    cancelled = False
    cancel_event = threading.Event()

    @staticmethod
    def read_file(file_path: Path):
        text = ""

        if file_path.suffix.lower() == ".txt":
            text = file_path.read_text(encoding="utf-8", errors="ignore")

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

    @classmethod
    def build_index(cls, file_path: str):
        start_time = time.time()

        cls.status = "processing"
        cls.progress = 0
        cls.time_taken = 0
        cls.cancel_event.clear()

        file_path = Path(file_path)

        if not file_path.exists():
            cls.status = "error"
            return

        text = cls.read_file(file_path)

        if not text.strip():
            cls.status = "error"
            return

        chunks = text_splitter.split_text(text)
        total = len(chunks)

        if total == 0:
            cls.status = "error"
            return

        if (FAISS_INDEX_PATH / "index.faiss").exists():
            vector_store = FAISS.load_local(
                str(FAISS_INDEX_PATH),
                embeddings_model,
                allow_dangerous_deserialization=True
            )
        else:
            vector_store = None

        batch_size = 8

        for i in range(0, total, batch_size):

            # 🔴 Cancel check
            if cls.cancel_event.is_set():
                cls.status = "cancelled"
                cls.progress = 0
                return


            batch = chunks[i:i + batch_size]

            if vector_store is None:
                vector_store = FAISS.from_texts(batch, embeddings_model)
            else:
                vector_store.add_texts(batch)

            processed = min(i + batch_size, total)
            cls.progress = int((processed / total) * 100)

        if vector_store:
            vector_store.save_local(str(FAISS_INDEX_PATH))

        cls.time_taken = round(time.time() - start_time, 2)
        cls.status = "ready"
        cls.progress = 100

    @classmethod
    def cancel(cls):
        print("Cancel called!")
        cls.cancel_event.set()
