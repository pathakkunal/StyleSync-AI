import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

class WriterAgent:
    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")
        if not self.api_key:
            print("⚠️ GROQ_API_KEY missing. Writer Agent will not function.")
            self.client = None
        else:
            self.client = Groq(api_key=self.api_key)
            self.model = "llama-3.3-70b-versatile"

    def write_listing(self, visual_data: dict, seo_keywords: list) -> dict:
        if not self.client:
            return {"error": "No API Key"}

        system_prompt = """You are a elite e-commerce copywriter for high-end fashion brands. 
        Your goal is to write a product listing that converts.
        
        RULES:
        1. Tone: Sophisticated, confident, and sensory.
        2. Focus on BENEFITS, not just features.
        3. Integrate SEO keywords naturally, do not stuff them.
        4. Return ONLY valid JSON.
        
        JSON STRUCTURE:
        {
            "title": "SEO Optimized Title (50-60 chars)",
            "description": "2-3 persuasive paragraphs telling a story about the product.",
            "features": ["Bullet 1 (benefit)", "Bullet 2 (material)", "Bullet 3 (fit)"],
            "price_estimate": "Estimated price range in USD based on perceived value"
        }
        """

        user_content = f"""
        PRODUCT DATA:
        {json.dumps(visual_data, indent=2)}
        
        TARGET KEYWORDS:
        {', '.join(seo_keywords)}
        """

        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_content}
                ],
                temperature=0.7,
                response_format={"type": "json_object"}
            )

            return json.loads(completion.choices[0].message.content)

        except Exception as e:
            print(f"❌ Writer Error: {e}")
            return {"error": str(e)}
