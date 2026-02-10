import os
import shutil

# --- Configuration ---
OLD_NAMES = ["MerchFlow", "TrendForge", "MerchFlow-AI", "TrendForge-AI"]
NEW_NAME = "StyleSync"
NEW_TITLE = "StyleSync AI"
ROOT_DIR = os.getcwd()

def replace_text_in_file(file_path):
    # CRITICAL: Skip this script itself to prevent self-corruption
    if os.path.basename(file_path) == "setup_rebrand.py" or os.path.abspath(file_path) == os.path.abspath(__file__):
        print(f"Skipping self: {file_path}")
        return

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        new_content = content
        for old in OLD_NAMES:
            new_content = new_content.replace(old, NEW_NAME)
            new_content = new_content.replace(old.upper(), NEW_NAME.upper())
            # Handle space variations like "Merch Flow"
            new_content = new_content.replace(old.replace("Flow", " Flow"), NEW_TITLE)
        
        # Specific Brand Color Update (Switch to Emerald/Teal for StyleSync)
        new_content = new_content.replace("blue-600", "emerald-600")
        new_content = new_content.replace("primary", "emerald-500") # Tailwind heuristic
        
        if content != new_content:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(new_content)
            print(f"✏️ Updated content in: {file_path}")
    except Exception as e:
        print(f"⚠️ Could not process {file_path}: {e}")

def main():
    print(f"🚀 Initializing {NEW_TITLE} Setup in Antigravity...")

    # 1. Rename Directories
    print("\n--- Renaming Directories ---")
    for item in os.listdir(ROOT_DIR):
        if os.path.isdir(item) and any(old in item for old in OLD_NAMES):
            new_dir_name = item.replace("MerchFlow", NEW_NAME).replace("TrendForge", NEW_NAME)
            # Ensure we don't overwrite existing
            if not os.path.exists(new_dir_name):
                os.rename(item, new_dir_name)
                print(f"📂 Renamed folder: {item} -> {new_dir_name}")
            else:
                print(f"⚠️ Folder {new_dir_name} already exists. Merging content...")
    
    # 2. Update File Content (Recursively)
    print("\n--- Updating File Branding ---")
    for root, dirs, files in os.walk(ROOT_DIR):
        if "venv" in root or ".git" in root or "__pycache__" in root:
            continue
            
        for file in files:
            file_path = os.path.join(root, file)
            # Skip if it's the current script
            if os.path.abspath(file_path) == os.path.abspath(__file__) or file == "setup_rebrand.py":
                continue
                
            if file.endswith((".py", ".html", ".md", ".txt", ".json")):
                replace_text_in_file(file_path)

    # 3. Create Standard requirements.txt
    print("\n--- Generating Standard requirements.txt ---")
    reqs = """fastapi==0.109.0
uvicorn==0.27.0
python-multipart
python-dotenv
google-generativeai>=0.8.3
groq
pinecone-client>=3.0.0
langchain
langchain-community
langchain-google-genai
langchain-groq
pillow
huggingface_hub
httpx
"""
    with open("requirements.txt", "w", encoding="utf-8") as f:
        f.write(reqs)
    print("✅ Created requirements.txt")

    # 4. Create README
    readme_content = f"""---
title: {NEW_TITLE}
emoji: 🛍️
colorFrom: green
colorTo: indigo
sdk: docker
pinned: false
---

# {NEW_TITLE}

**{NEW_TITLE}** is an autonomous design & merchandising agent built for the Antigravity IDE. 

## ⚡ Stack
* **Core:** FastAPI & Python 3.9
* **Vision:** Gemini 1.5 Flash
* **Copy:** Llama 3 (Groq)
* **Memory:** Pinecone

## 🚀 Local Run
```bash
pip install -r requirements.txt
python main.py
"""
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(readme_content)
    print("✅ Created README.md")

    print(f"\n🎉 {NEW_TITLE} is ready! Run 'python main.py' to start.")

if __name__ == "__main__":
    main()
