from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.domains.chat.router import router as chat_router

app = FastAPI(
    title="Student Environment API",
    description="Backend for University Students App",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)





app.include_router(chat_router)

@app.get("/")
async def root():
    return {"message": "Welcome to Student Environment API. Chat system is ready!"}

