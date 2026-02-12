from fastapi import HTTPException , Query  , Depends
from sqlalchemy.orm import Session
from schemas.chat_schema import ChatRequest
from services.chat_service import ChatService
from typing import Optional
from database import get_db

class ChatController:
    @staticmethod
    async def process_stream(data: ChatRequest):
        try:
            return await ChatService.generate_stream(data.message, data.thread_id)
        except Exception as e:
            print("Error:", str(e))
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    async def fetch_chat_history(thread_id: str, limit: Optional[int] = Query(50, gt=0), offset: Optional[int] = Query(0, ge=0)):
       
        try:
            return await ChatService.get_chat_history(thread_id, limit=limit, offset=offset)
        except Exception as e:
            print("Error:", str(e))
            raise HTTPException(status_code=500, detail=str(e))
    
    @staticmethod
    def fetch_threads(db: Session = Depends(get_db)):
        try:
            return ChatService.get_all_threads(db)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    