import os
import re

def fix_dashboard_branding():
    print("🎨 Correcting Dashboard Title...")
    path = "dashboard.html"
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()

        # Brutal replace: Fix the repeating "AI AI AI" issue
        # We replace any variation of "StyleSync AI AI..." with just "StyleSync AI"
        new_content = re.sub(r"StyleSync AI( AI)+", "StyleSync AI", content)

        # Ensure the Title tag is clean
        new_content = new_content.replace("<title>StyleSync AI AI AI AI AI Dashboard</title>", "<title>StyleSync AI Dashboard</title>")

        # Ensure the H2 header is clean
        new_content = new_content.replace("Enterprise Edition", "Enterprise Edition 1.0")

        with open(path, "w", encoding="utf-8") as f:
            f.write(new_content)
        print("✅ Dashboard branding sanitized.")

def fix_writer_prompt():
    print("✍️  Reinforcing Writer Agent...")
    path = "agents/writer_agent.py"
    # Overwrite with robust version
    robust_code = """import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

class WriterAgent:
    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")
        self.client = Groq(api_key=self.api_key) if self.api_key else None
        self.model = "llama-3.3-70b-versatile"

    def write_listing(self, visual_data: dict, seo_keywords: list) -> dict:
        if not self.client:
            return {"error": "No API Key"}

        system_prompt = \"\"\"You are a professional copywriter.
        Write a JSON product listing.

        RULES:
        1. Output strictly valid JSON.
        2. "description": Single paragraph, plain text, no newlines.
        3. "title": Concise SEO title.
        4. "features": List of 3 distinct features.

        Example Output:
        {
            "title": "Classic Leather Jacket",
            "description": "A timeless piece crafted from premium leather.",
            "features": ["Genuine Leather", "Slim Fit", "Zip Closure"],
            "price_estimate": "$100-$150"
        }
        \"\"\"

        user_content = f\"\"\"
        DATA: {json.dumps(visual_data)}
        KEYWORDS: {', '.join(seo_keywords)}
        \"\"\"

        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_content}
                ],
                temperature=0.1,
                response_format={"type": "json_object"}
            )
            return json.loads(completion.choices[0].message.content)
        except Exception as e:
            print(f"❌ Writer Error: {e}")
            return {
                "title": visual_data.get('product_type', 'Product Name'),
                "description": "High-quality fashion item matching your style.",
                "features": visual_data.get('visual_features', []),
                "price_estimate": "$50-$100"
            }
"""
    with open(path, "w", encoding="utf-8") as f:
        f.write(robust_code)
    print("✅ Writer Agent logic updated to 'Robust Mode'.")

def force_docker_rebuild():
    print("🐳 Touching Dockerfile to force rebuild...")
    path = "Dockerfile"
    if os.path.exists(path):
        with open(path, "a") as f:
            f.write("\n# Force Rebuild: Final Polish v1.0\n")
    print("✅ Dockerfile updated.")

if __name__ == "__main__":
    fix_dashboard_branding()
    fix_writer_prompt()
    force_docker_rebuild()