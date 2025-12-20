import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

class VisualAnalyst:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found")
        
        genai.configure(api_key=self.api_key)
        self.model_name = "models/gemini-flash-latest"
        self.model = genai.GenerativeModel(self.model_name)
        print(f"✅ VisualAnalyst stored Gemini model: {self.model_name}")

    def analyze_image(self, image_path: str):
        try:
            # Upload the file to Gemini
            # Note: For efficiency in production, files should be managed (uploads/deletes)
            # but for this agentic flow, we'll upload per request or assume local path usage helper if needed.
            # However, the standard `model.generate_content` can take PIL images or file objects directly for some sdk versions,
            # but using the File API is cleaner for 1.5 Flash multi-modal.
            # Let's use the simpler PIL integration if available, or just path if the SDK supports it.
            # actually, standard genai usage for images usually involves PIL or uploading.
            # Let's try the PIL approach first as it's often more direct for local scripts.
            import PIL.Image
            img = PIL.Image.open(image_path)
            
            user_prompt = (
                "Analyze this product image. "
                "Return ONLY valid JSON with keys: main_color, product_type, design_style, visual_features."
            )
            
            # Gemini 1.5 Flash supports JSON response schema, but simple prompting often works well too.
            # We'll stick to prompt engineering for now to match the "Return ONLY valid JSON" instruction.
            response = self.model.generate_content([user_prompt, img])
            
            response_text = response.text
            
            # Clean up potential markdown code fences
            cleaned_content = response_text
            if "```json" in cleaned_content:
                cleaned_content = cleaned_content.replace("```json", "").replace("```", "")
            elif "```" in cleaned_content:
                 cleaned_content = cleaned_content.replace("```", "")
            
            return json.loads(cleaned_content.strip())

        except Exception as e:
            print(f"❌ Analysis Failed: {e}")
            return {
                "main_color": "Unknown",
                "product_type": "Unknown", 
                "design_style": "Unknown",
                "visual_features": [f"Error: {str(e)}"]
            }
