from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import Base, engine
from routes.contact_route import router as ContactRouter
from routes.admin_routes import router as AdminRouter
from routes.chat_route import router as ChatRouter

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

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5000, reload=True)
