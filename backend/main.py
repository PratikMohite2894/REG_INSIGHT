from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from backend.chatbot.creeChat import router as cree_router

# ✅ Import your router
from backend.chatbot.chat import router as chat_router

app = FastAPI()

# ✅ CORS setup (allow frontend or Spring Boot to call this)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can replace * with specific frontend IP if needed
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Attach router for chat functionality
app.include_router(chat_router, prefix="/api")
app.include_router(cree_router, prefix="/api")
