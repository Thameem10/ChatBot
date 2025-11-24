from fastapi import APIRouter
from controllers.chat_controller import ChatController
from schemas.chat_schema import ChatRequest

router = APIRouter(prefix="/chat", tags=["Chat"])

@router.post("/send")
async def send_message(data: ChatRequest):
    return await ChatController.process_message(data)
