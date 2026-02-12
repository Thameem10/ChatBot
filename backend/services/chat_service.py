import google.generativeai as genai
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from sqlalchemy import func
from models import Thread, Message
from database import SessionLocal
from typing import List, Optional
import uuid
import os
# Add these imports at the top of services/chat_service.py
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS


genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

VECTOR_STORE_PATH = "vector_store/faiss_index"
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vector_store = FAISS.load_local(
    VECTOR_STORE_PATH,
    embeddings,
    allow_dangerous_deserialization=True
)


class ChatService:
    @staticmethod
    async def generate_stream(message: str, thread_id: str):
        db: Session = SessionLocal()

        try:
            # Ensure thread exists
            thread = db.query(Thread).filter(Thread.id == thread_id).first()
            if not thread:
                thread = Thread(id=thread_id)
                db.add(thread)
                db.commit()
                db.refresh(thread)

            # Save user message
            user_msg = Message(
                id=str(uuid.uuid4()),
                thread_id=thread_id,
                sender="user",
                text=message
            )
            db.add(user_msg)
            db.commit()

            # Retrieve relevant chunks from FAISS vector store
            relevant_docs = vector_store.similarity_search(message, k=3)
            retrieved_text = "\n".join([doc.page_content for doc in relevant_docs])

            # ---------------------------
            # STRICT RAG: No hallucination
            # ---------------------------
            history = [
                {
                    "role": "user",
                    "parts": [
                        "You are a document-based assistant. "
                        "Use ONLY the information provided in the context. "
                        "If the answer is not found in the context, reply strictly: "
                        "'I don't know based on the provided document.'"
                    ]
                }
            ]

            # Add past messages (unchanged)
            messages = db.query(Message).filter(
                Message.thread_id == thread_id
            ).order_by(Message.created_at).all()

            for m in messages:
                history.append({
                    "role": "user" if m.sender == "user" else "model",
                    "parts": [m.text]
                })

            # Append retrieved document context and question
            history.append({
                "role": "user",
                "parts": [
                    f"Context:\n{retrieved_text}\n\n"
                    f"Question: {message}"
                ]
            })

            # Initialize Gemini model
            model = genai.GenerativeModel("gemini-2.0-flash")
            response = model.generate_content(history, stream=True)

            async def event_stream():
                full_reply = ""

                for chunk in response:
                    if chunk.candidates and chunk.candidates[0].content.parts:
                        delta = chunk.candidates[0].content.parts[0].text
                        if delta:
                            full_reply += delta
                            yield delta

                # Save bot response
                bot_msg = Message(
                    id=str(uuid.uuid4()),
                    thread_id=thread_id,
                    sender="bot",
                    text=full_reply
                )
                db.add(bot_msg)
                db.commit()

            return StreamingResponse(event_stream(), media_type="text/event-stream")

        finally:
            db.close()

    @staticmethod
    async def get_chat_history(thread_id: str, limit: int = 50, offset: int = 0) -> List[dict]:
        db: Session = SessionLocal()
        try:
            messages = (
                db.query(Message)
                .filter(Message.thread_id == thread_id)
                .order_by(Message.created_at)
                .offset(offset)
                .limit(limit)
                .all()
            )
            history = [{"sender": m.sender, "text": m.text} for m in messages]
            return history
        finally:
            db.close()

    @staticmethod
    def get_all_threads(db: Session):
        # Get latest message per thread to use as title
        subquery = (
            db.query(
                Message.thread_id,
                func.max(Message.created_at).label("last_msg_time")
            )
            .group_by(Message.thread_id)
            .subquery()
        )

        threads = (
            db.query(
                Message.thread_id,
                Message.text.label("title"),
                Message.created_at
            )
            .join(
                subquery,
                (Message.thread_id == subquery.c.thread_id) &
                (Message.created_at == subquery.c.last_msg_time)
            )
            .order_by(subquery.c.last_msg_time.desc())
            .all()
        )

        # Return list of dicts with id and title
        return [{"id": t.thread_id, "title": t.title} for t in threads]