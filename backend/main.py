from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import Base, engine
from routes.contact_route import router as ContactRouter
from routes.admin_routes import router as AdminRouter
from routes.chat_route import router as ChatRouter
from routes.file_routes import router as FileRouter

import uvicorn

# Create DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Register Routes
app.include_router(ContactRouter)
app.include_router(AdminRouter)
app.include_router(ChatRouter)
app.include_router(FileRouter)


