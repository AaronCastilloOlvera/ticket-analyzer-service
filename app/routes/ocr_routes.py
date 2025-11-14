from fastapi import APIRouter, UploadFile, File
from app.services.ocr_service import process_image
from google import genai
from google.genai import types
import json

routes = APIRouter(prefix="/orc", tags=["ORC"])

@routes.post("/analyze-image")
async def analyze_image(file: UploadFile = File(...)):
    """
    Analyze an image file for ORC (Optical Character Recognition) processing.

    - **file**: The image file to be analyzed.
    """
    try:
        # Extract text from image using OCR
        ocr_result = await process_image(file)

        # Gemini AI Integration
        client = genai.Client()

        json_example = {
            "ticket_id": "1234567890",
            "odds": 2.5,
            "stake": 100.0,
            "payout": 250.0,
            "status": "won",
            "bet_description": "Team A to win against Team B",
            "match_datetime": "2025-11-02T13:39:00",
            "device_type": "movil",
            "league": "Liga MX"
        }

        request_description = (
            "I will provide you a text extracted from an image using OCR. "
            "If the odds is american format (e.g., +150, -200), convert it to decimal format. "
            "Remove any special characters and extra spaces. "
            "Infer the league from the bet description or teams if possible (e.g., Liga MX, MLS, Copa Oro) and return it in the 'league' field. "
            "Status value should be 'pending' if there is no result mentioned in the text. Another values are 'won' or 'lost'. "
            "If includad, 'incl. Prorroga' remove it from the bet description. "
            "Add 'CA - ' at the start of the bet description if it is a 'crear apuesta' (a single match with 2 or more selections). "
            "Add 'Parley' at the start of the bet description if it is a parley bet. "
            "Device type should only be 'movil' or 'desktop' based on the layout of the ticket. "
            "Add a column call studied with boolean false value. "
            "Add a column called comments with empty string value. "
            "Return a compact JSON with this structure: "
            f"{json.dumps(json_example)} "
            "Do not use markdown, code blocks, or line breaks. "
            "No explanation, just the JSON."
        )

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=request_description + "\n Extracted Text: " + str(ocr_result),
            config=types.GenerateContentConfig(
                thinking_config=types.ThinkingConfig(thinking_budget=0) # Disables thinking
            ),
        )
        
        gemini_text = ""
        try:
            gemini_text = response.candidates[0].content.parts[0].text
        except Exception:
            gemini_text = str(response)

        # Attempt to parse Gemini response as JSON
        try:
            gemini_json = json.loads(gemini_text)
        except Exception:
            gemini_json = gemini_text

        return gemini_json

    except Exception as e:
        return {"error": str(e)}