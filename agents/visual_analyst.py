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
            raise ValueError("GEMINI_API_KEY not found")
        
        genai.configure(api_key=self.api_key)
        
        print("🔍 Checking available Gemini models...")
        try:
            my_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
            print(f"📋 Available Models: {my_models}")
            
            # UPDATED PRIORITY: GEMINI 2.0 FIRST
            preferred_order = [
                'models/gemini-2.0-flash-exp',  # <--- Newest & Smartest (Available in logs)
                'models/gemini-1.5-pro',
                'models/gemini-1.5-pro-001',
                'models/gemini-1.5-flash',
                'models/gemini-1.5-flash-001',
                'models/gemini-pro-vision'
            ]
            
            selected_model = "models/gemini-2.0-flash-exp" # Default to the new one
            
            for model_name in preferred_order:
                if model_name in my_models:
                    selected_model = model_name
                    break
            
            print(f"✅ Selected Vision Model: {selected_model}")
            self.model = genai.GenerativeModel(selected_model)
            
        except Exception as e:
            print(f"⚠️ Model list failed ({e}), defaulting to gemini-2.0-flash-exp")
            self.model = genai.GenerativeModel('models/gemini-2.0-flash-exp')

    async def analyze_image(self, image_path: str):
        # Adaptation: Read file path to bytes, as main.py passes a path
        try:
            with open(image_path, "rb") as f:
                image_bytes = f.read()
        except Exception as e:
            print(f"❌ File Read Error: {e}")
            return {
                "main_color": "Unknown",
                "visual_features": [f"Error reading file: {str(e)}"]
            }

        prompt = (
            "Analyze this product image for an e-commerce listing. "
            "Return a JSON object with keys: main_color, product_type, design_style, visual_features."
        )
        try:
            # Adaptation: Run in thread to allow async await
            response = await asyncio.to_thread(
                self.model.generate_content,
                [
                    {'mime_type': 'image/jpeg', 'data': image_bytes},
                    prompt
                ]
            )
            
            text = response.text
            if text.startswith('```json'): text = text[7:]
            if text.endswith('```'): text = text[:-3]
            
            return json.loads(text.strip())
        except Exception as e:
            print(f"❌ Analysis Failed: {e}")
            return {
                "main_color": "Unknown",
                "visual_features": [f"Error: {str(e)}"]
            }
