import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("❌ API Key not found")
else:
    genai.configure(api_key=api_key)
    print("Listing available models:")
    for m in genai.list_models():
        if 'embedContent' in m.supported_generation_methods:
            print(f"- {m.name}")
