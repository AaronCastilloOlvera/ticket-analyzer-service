from fastapi import APIRouter, UploadFile, File
from app.services.ocr_service import process_image

routes = APIRouter(prefix="/orc", tags=["ORC"])

@routes.post("/analyze-image")
async def analyze_image(file: UploadFile = File(...)):
    """
    Analyze an image file for ORC (Optical Character Recognition) processing.

    - **file**: The image file to be analyzed.
    """
    result = await process_image(file)

    return {"result": result}