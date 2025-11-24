from fastapi import HTTPException
from schemas.chat_schema import ChatRequest
from services.chat_service import ChatService

class ChatController:
    @staticmethod
    async def process_message(data: ChatRequest):
        try:
            reply = await ChatService.generate_response(data.message, data.thread_id)
            return {"reply": reply}

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

