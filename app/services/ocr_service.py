import requests, os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OCR_SPACE_API_KEY")
OCR_API_URL = os.getenv("OCR_SPACE_API_URL")

async def process_image(file):
    try:
        image_bytes = await file.read()
        if not API_KEY:
            return {"error": "API key not set. Check your .env file."}
        
        payload = { "apikey": API_KEY, "language": "spa" }
        
        response = requests.post(
            OCR_API_URL,
            files={"file": (file.filename, image_bytes)},
            data=payload )
        
        try:
            result = response.json()
        except Exception:
            return {"error": "Invalid JSON response", "response": response.text}
        if "ParsedResults" in result and result["ParsedResults"]:
            return result["ParsedResults"][0].get("ParsedText", "No text found")
        return {"error": "No ParsedResults", "response": result}
    except Exception as e:
        return {"error": str(e)}
