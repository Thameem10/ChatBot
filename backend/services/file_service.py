import os
import uuid
from fastapi import UploadFile
from sqlalchemy.orm import Session
from models import ChatbotFile
from database import SessionLocal

UPLOAD_DIR = "uploads"  # create this folder in your project root
os.makedirs(UPLOAD_DIR, exist_ok=True)

class FileService:
    @staticmethod
    def upload_file(file: UploadFile):
        db: Session = SessionLocal()
        try:
            # Only allow one file: delete previous file record if exists
            existing_file = db.query(ChatbotFile).first()
            if existing_file:
                if os.path.exists(existing_file.filepath):
                    os.remove(existing_file.filepath)
                db.delete(existing_file)
                db.commit()

            # Save new file
            file_id = str(uuid.uuid4())
            file_path = os.path.join(UPLOAD_DIR, f"{file_id}_{file.filename}")

            with open(file_path, "wb") as f:
                f.write(file.file.read())

            chatbot_file = ChatbotFile(
                id=file_id,
                filename=file.filename,
                filepath=file_path
            )
            db.add(chatbot_file)
            db.commit()
            db.refresh(chatbot_file)
            return chatbot_file
        finally:
            db.close()
    