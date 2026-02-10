import os
import sys

def main():
    print("\n🔐 StyleSync AI - Security Setup")
    print("---------------------------------")
    print("Please enter your API keys. They will be saved locally to .env")
    print("(Get free keys at: console.groq.com | aistudio.google.com | pinecone.io)\n")

    groq_key = input("👉 Enter GROQ_API_KEY: ").strip()
    gemini_key = input("👉 Enter GEMINI_API_KEY: ").strip()
    pinecone_key = input("👉 Enter PINECONE_API_KEY (Optional for Phase 2): ").strip()

    env_content = f"GROQ_API_KEY={groq_key}\nGEMINI_API_KEY={gemini_key}\nPINECONE_API_KEY={pinecone_key}\n"

    try:
        with open(".env", "w", encoding="utf-8") as f:
            f.write(env_content)
        print("\n✅ .env file created successfully!")
    except Exception as e:
        print(f"\n❌ Failed to write .env: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
