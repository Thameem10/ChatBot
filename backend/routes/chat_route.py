from fastapi import APIRouter , Query , Depends
from controllers.chat_controller import ChatController
from schemas.chat_schema import ChatRequest
from fastapi.responses import StreamingResponse
from typing import Optional
from sqlalchemy.orm import Session
from database import SessionLocal


router = APIRouter(prefix="/chat", tags=["Chat"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/send")
async def send_message(data: ChatRequest):
    # Return streaming response from controller
    return await ChatController.process_stream(data)

@router.get("/history/{thread_id}")
async def get_chat_history(
    thread_id: str,
    limit: Optional[int] = Query(50, gt=0),   # default 50 messages per page
    offset: Optional[int] = Query(0, ge=0)    # default start from 0
):
   
    return await ChatController.fetch_chat_history(thread_id, limit=limit, offset=offset)  

@router.get("/threads")
def get_threads(db: Session = Depends(get_db)):
    
    return ChatController.fetch_threads(db)