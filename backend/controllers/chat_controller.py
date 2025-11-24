from fastapi import HTTPException
from schemas.chat_schema import ChatRequest
from services.chat_service import ChatService


class ChatController:
    @staticmethod
    async def process_stream(data: ChatRequest):
        try:
            return await ChatService.generate_stream(data.message, data.thread_id)
        except Exception as e:
            print("Error:", str(e))
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    async def fetch_chat_history(thread_id: str):
        try:
            return await ChatService.get_chat_history(thread_id)
        except Exception as e:
            print("Error:", str(e))
            raise HTTPException(status_code=500, detail=str(e))