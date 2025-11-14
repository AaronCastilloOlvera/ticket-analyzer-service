from fastapi import FastAPI
from app.routes.ocr_routes import routes as ocr_routes
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Tycket Analyzer API", version="1.0.0")

allowed_origins = [o.strip() for o in os.getenv("ALLOWED_ORIGINS", "").split(",") if o.strip()]
if not allowed_origins:
    print("Warning: No allowed origins set in ALLOWED_ORIGINS environment variable.")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ocr_routes)