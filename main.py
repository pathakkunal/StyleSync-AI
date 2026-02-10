import os
import httpx
import asyncio
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv

# Import Phase 2 & 3 Agents
from agents.visual_analyst import VisualAnalyst
from agents.memory_agent import MemoryAgent
from agents.writer_agent import WriterAgent

load_dotenv()
app = FastAPI()

# --- Global Agent Initialization ---
print("🚀 StyleSync AI: Initializing Agents...")
try:
    visual_agent = VisualAnalyst()
    memory_agent = MemoryAgent() # Connects to 'stylesync-index-v2'
    writer_agent = WriterAgent()
    print("✅ All Agents Online & Ready.")
except Exception as e:
    print(f"❌ Critical Startup Error: {e}")

@app.get("/", response_class=HTMLResponse)
async def read_root():
    try:
        with open("dashboard.html", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "<h1>Error: dashboard.html not found. Run setup scripts first.</h1>"

@app.post("/generate-catalog")
async def generate_catalog(file: UploadFile = File(...)):
    file_path = f"temp_{file.filename}"
    try:
        # 1. Save File Temporarily
        with open(file_path, "wb") as f:
            f.write(await file.read())
        
        # 2. Vision (The Eyes)
        print(f"👁️ Analyzing: {file.filename}")
        visual_data = await visual_agent.analyze_image(file_path)
        
        # 3. Memory (The Context)
        # Create a search query from visual tags
        search_query = f"{visual_data.get('design_style', '')} {visual_data.get('product_type', '')}"
        print(f"🧠 Recalling trends for: {search_query}")
        seo_keywords = memory_agent.retrieve_keywords(search_query)
        
        # 4. Writer (The Brain)
        print("✍️ Drafting copy...")
        listing = writer_agent.write_listing(visual_data, seo_keywords)
        
        # 5. Construct Payload
        response_data = {
            "status": "success",
            "visual_analysis": visual_data,
            "market_trends": seo_keywords,
            "final_listing": listing
        }
        
        # 6. Automation Trigger (n8n)
        n8n_url = os.getenv("N8N_WEBHOOK_URL")
        if n8n_url:
            asyncio.create_task(trigger_webhook(n8n_url, response_data))
            
        return JSONResponse(content=response_data)

    except Exception as e:
        print(f"❌ Pipeline Error: {e}")
        return JSONResponse(content={"error": str(e)}, status_code=500)
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)

async def trigger_webhook(url, data):
    """Fire-and-forget webhook to n8n"""
    try:
        async with httpx.AsyncClient() as client:
            await client.post(url, json=data, timeout=5.0)
            print(f"🚀 Webhook sent to n8n")
    except Exception as e:
        print(f"⚠️ Webhook failed: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)
