import google.generativeai as genai
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from models import Thread, Message
from database import SessionLocal
import uuid
import os

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

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

            # Build history from DB messages with valid roles for Gemini
            messages = db.query(Message).filter(Message.thread_id == thread_id).order_by(Message.created_at).all()
            history = [
                {
                    "role": "user" if m.sender == "user" else "model",
                    "parts": [m.text]
                }
                for m in messages
            ]

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
                            yield delta  # stream chunk to frontend

                # Save bot response after streaming finishes
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
    async def get_chat_history(thread_id: str):
        db: Session = SessionLocal()
        try:
            messages = db.query(Message).filter(Message.thread_id == thread_id).order_by(Message.created_at).all()
            history = [{"sender": m.sender, "text": m.text} for m in messages]
            return history
        finally:
            db.close()
