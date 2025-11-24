from fastapi import APIRouter
from controllers.chat_controller import ChatController
from schemas.chat_schema import ChatRequest
from fastapi.responses import StreamingResponse

router = APIRouter(prefix="/chat", tags=["Chat"])

@router.post("/send")
async def send_message(data: ChatRequest):
    # Return streaming response from controller
    return await ChatController.process_stream(data)
