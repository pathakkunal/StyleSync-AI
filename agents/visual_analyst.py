import google.generativeai as genai
import os
import json
import asyncio
from dotenv import load_dotenv

load_dotenv()

class VisualAnalyst:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        genai.configure(api_key=self.api_key)
        # UPDATED: Using the stable model version
        self.model = genai.GenerativeModel('gemini-1.5-flash')

    async def analyze_image(self, image_path: str):
        # Read file as bytes to match the user's logic requirements
        try:
            with open(image_path, "rb") as f:
                image_bytes = f.read()
        except Exception as e:
             return {
                "main_color": "Error",
                "product_type": "File Read Error",
                "design_style": "Error",
                "visual_features": [f"Could not read file: {str(e)}"]
            }

        prompt = (
            "Analyze this product image for an e-commerce listing. "
            "detailed visual attributes including: Main Color, Material/Texture, Style/Vibe, "
            "and 3 distinct Visual Features. Return the result strictly as a JSON object "
            "with keys: main_color, product_type, design_style, visual_features."
        )
        
        try:
            # Run blocking call in thread
            response = await asyncio.to_thread(
                self.model.generate_content,
                [
                    {'mime_type': 'image/jpeg', 'data': image_bytes},
                    prompt
                ]
            )
            
            text_response = response.text
            
            # Clean up markdown code blocks if present
            if text_response.startswith('```json'):
                text_response = text_response[7:]
            if text_response.startswith('```'):
                text_response = text_response[3:]
            if text_response.endswith('```'):
                text_response = text_response[:-3]
                
            return json.loads(text_response.strip())
        except Exception as e:
            print(f"⚠️ API Error: {e}")
            # Return a clearer error for debugging
            return {
                "main_color": "Unknown",
                "product_type": "Unidentified Item",
                "design_style": "Standard",
                "visual_features": [f"Error: {str(e)}"]
            }
