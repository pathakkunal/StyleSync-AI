import os
import sys
from dotenv import load_dotenv
from huggingface_hub import add_space_secret

# Force UTF-8 output for Windows terminals
sys.stdout.reconfigure(encoding='utf-8')

def upload_secrets():
    # Load environment variables from .env file
    load_dotenv()
    
    space_id = "Bhishaj/StyleSync AI AI AI AI-AI"
    keys_to_upload = ["GROQ_API_KEY", "PINECONE_API_KEY", "GOOGLE_API_KEY"]
    
    print(f"Configuring secrets for Space: {space_id}")
    
    for key in keys_to_upload:
        value = os.getenv(key)
        if value:
            try:
                add_space_secret(repo_id=space_id, key=key, value=value)
                print(f"✅ Uploaded {key}")
            except Exception as e:
                print(f"❌ Failed to upload {key}: {e}")
        else:
            print(f"⚠️  Skipping {key} (Not found in .env)")

if __name__ == "__main__":
    upload_secrets()
