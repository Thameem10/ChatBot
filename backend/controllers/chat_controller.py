from fastapi import HTTPException
from schemas.chat_schema import ChatRequest
from services.chat_service import ChatService
from fastapi.responses import StreamingResponse

class ChatController:
    @staticmethod
    async def process_stream(data: ChatRequest):
        try:
            # Return streaming response directly
            return await ChatService.generate_stream(data.message, data.thread_id)

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
