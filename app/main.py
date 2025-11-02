from fastapi import FastAPI
from app.routes.ocr_routes import routes

app = FastAPI(title="My FastAPI Application")

app.include_router(routes)