from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router

app = FastAPI()

# ✅ CORS CONFIGURATION (CRITICAL)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],   # allows OPTIONS, POST, GET, etc.
    allow_headers=["*"],
)

app.include_router(router)
