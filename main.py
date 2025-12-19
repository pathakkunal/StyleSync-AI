import os
import httpx
import asyncio
import json
import traceback
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from dotenv import load_dotenv

# Import Agents
from agents.visual_analyst import VisualAnalyst
from agents.memory_agent import MemoryAgent
from agents.writer_agent import WriterAgent

load_dotenv()

app = FastAPI()

# Initialize Agents
try:
    visual_agent = VisualAnalyst()
    memory_agent = MemoryAgent()
    writer_agent = WriterAgent()
    
    # Try seeding database, but don't crash if it fails (optional robustness)
    try:
        memory_agent.seed_database()
    except Exception as e:
        print(f"⚠️ Memory Agent Seed Warning: {e}")
        
    print("✅ All Agents Online")
except Exception as e:
    print(f"❌ Agent Startup Failed: {e}")
    # We continue, but endpoints might fail if agents aren't ready.

@app.get("/", response_class=HTMLResponse)
async def read_root():
    try:
        with open("dashboard.html", "r") as f:
            return f.read()
    except FileNotFoundError:
        return "<h1>Error: dashboard.html not found</h1>"

@app.post("/generate-catalog")
async def generate_catalog(file: UploadFile = File(...)):
    file_path = None
    try:
        # 1. Save Temp File
        os.makedirs("uploads", exist_ok=True)
        file_path = f"uploads/{file.filename}"
        with open(file_path, "wb") as f:
            f.write(await file.read())
        
        # 2. Run AI Pipeline (Sequential)
        print("▶️ Starting Visual Analysis...")
        visual_data = await visual_agent.analyze_image(file_path)
        
        print("▶️ Retrieving Keywords...")
        query = f"{visual_data.get('main_color', '')} {visual_data.get('product_type', 'product')}"
        seo_keywords = memory_agent.retrieve_keywords(query)
        
        print("▶️ Writing Listing...")
        listing = writer_agent.write_listing(visual_data, seo_keywords)
        
        # 3. Construct Final Payload
        final_data = {
            "visual_data": visual_data,
            "seo_keywords": seo_keywords,
            "listing": listing
        }
        
        # 4. Async N8n Trigger (Before Return)
        # Constraint: "Must happen after agents finish but before returning"
        n8n_url = os.getenv("N8N_WEBHOOK_URL")
        if n8n_url:
            print(f"🚀 Triggering N8N Webhook: {n8n_url}")
            await trigger_n8n_webhook(n8n_url, final_data)
        else:
            print("ℹ️ N8N_WEBHOOK_URL not set, skipping webhook.")
            
        return JSONResponse(content=final_data)

    except Exception as e:
        error_details = traceback.format_exc()
        print(f"❌ Error in generate-catalog: {e}")
        print(error_details)
        return JSONResponse(
            content={
                "error": str(e),
                "type": type(e).__name__,
                "details": error_details
            },
            status_code=500
        )
        
    finally:
        # Cleanup
        if file_path and os.path.exists(file_path):
            try:
                os.remove(file_path)
            except Exception as cleanup_error:
                print(f"⚠️ Cleanup Warning: {cleanup_error}")

async def trigger_n8n_webhook(url: str, data: dict):
    """
    Sends data to n8n webhook asynchronously using httpx.
    """
    async with httpx.AsyncClient() as client:
        try:
            # We await the post to ensure it's sent before returning, 
            # fulfilling the user constraint.
            response = await client.post(url, json=data, timeout=10.0)
            response.raise_for_status()
            print(f"✅ N8N Webhook Success: {response.status_code}")
        except httpx.HTTPStatusError as e:
             print(f"❌ N8N Webhook HTTP Error: {e.response.status_code} - {e.response.text}")
        except Exception as e:
            print(f"❌ N8N Webhook Connection Failed: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)
