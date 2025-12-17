import os
import json
import asyncio
import google.generativeai as genai
from PIL import Image
from dotenv import load_dotenv

load_dotenv()

class VisualAnalyst:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            print("⚠️ GEMINI_API_KEY missing")

        genai.configure(api_key=api_key)
        # Use the modern, faster Flash model
        self.model = genai.GenerativeModel('gemini-1.5-flash')

    async def analyze_image(self, image_path: str):
        print(f"👁️ Analyzing image: {image_path}")
        
        try:
            # 1. Load image properly with Pillow (Fixes format issues)
            img = Image.open(image_path)
            
            # 2. Define the prompt
            prompt = """
            Analyze this product image for an e-commerce listing.
            Return ONLY a raw JSON object (no markdown formatting) with this structure:
            {
                "main_color": "string",
                "product_type": "string",
                "design_style": "string (minimalist, streetwear, vintage, etc)",
                "visual_features": ["list", "of", "visible", "features"],
                "suggested_title": "creative product title",
                "condition_guess": "new/used"
            }
            """
            
            # 3. Run in a thread to prevent blocking (Sync to Async wrapper)
            response = await asyncio.to_thread(
                self.model.generate_content,
                [prompt, img]
            )
            
            # 4. Clean and Parse JSON
            # 4. Clean and Parse JSON
            # Robust extraction of JSON content
            content = response.text
            if "```" in content:
                import re
                # Find content between ```json (or just ```) and ```
                match = re.search(r"```(?:json)?\s*(.*?)```", content, re.DOTALL)
                if match:
                    content = match.group(1)
            
            cleaned_text = content.strip()
            return json.loads(cleaned_text)
        except Exception as e:
            print(f"❌ Vision Error: {e}")
            # Return a Safe Fallback (Simulation)
            return {
                "main_color": "Unknown",
                "product_type": "Unidentified Item",
                "design_style": "Standard",
                "visual_features": ["Error analyzing image"],
                "suggested_title": "Manual Review Needed",
                "condition_guess": "New"
            }
