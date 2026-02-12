from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.chat_models import ChatOllama
from pathlib import Path
import google.generativeai as genai
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from sqlalchemy import func
from models import Thread, Message
from database import SessionLocal
from typing import List, Optional
import uuid
import os

# Embedding model
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Vector store path
VECTOR_STORE_PATH = Path("vector_store/faiss_index")


def get_vector_store():
    index_path = VECTOR_STORE_PATH / "index.faiss"

    # Check if index file exists
    if not index_path.exists():
        return None

    return FAISS.load_local(
        str(VECTOR_STORE_PATH),
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

            # Retrieve relevant chunks
            
            vector_store = get_vector_store()
            if not vector_store:
                return "Knowledge base not built yet. Please upload a document first."
            relevant_docs = vector_store.similarity_search(message, k=3)

            retrieved_text = "\n".join(
                [doc.page_content for doc in relevant_docs]
            )

            # STRICT RAG PROMPT
            prompt = f"""
                        You are a document-based assistant.
                        Use ONLY the information provided in the context.
                        If the answer is not found in the context,
                        reply strictly: "I don't know based on the provided document."

                        Context:
                        {retrieved_text}

                        Question:
                        {message}
                        """

            # Initialize Ollama
            llm = ChatOllama(
                model="llama3",  # or mistral
                temperature=0.2,
                streaming=True
            )

            async def event_stream():
                full_reply = ""

                for chunk in llm.stream(prompt):
                    if chunk.content:
                        full_reply += chunk.content
                        yield chunk.content

                # Save bot response
                bot_msg = Message(
                    id=str(uuid.uuid4()),
                    thread_id=thread_id,
                    sender="bot",
                    text=full_reply
                )
                db.add(bot_msg)
                db.commit()

            return StreamingResponse(
                event_stream(),
                media_type="text/event-stream"
            )

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