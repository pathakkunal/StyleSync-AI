import os
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from agents.visual_analyst import VisualAnalyst
from dotenv import load_dotenv
# Load environment variables
load_dotenv()
app = FastAPI()
# Initialize Agent
visual_agent = VisualAnalyst()
# 1. READ THE DASHBOARD HTML FILE INTO MEMORY
try:
    with open("dashboard.html", "r") as f:
        dashboard_html = f.read()
except FileNotFoundError:
    dashboard_html = "<h1>Error: dashboard.html not found. Please ensure the file exists.</h1>"
# 2. SERVE DASHBOARD AT ROOT (Home Page)
@app.get("/", response_class=HTMLResponse)
async def read_root():
    return dashboard_html
# 3. KEEP /dashboard ROUTE AS BACKUP
@app.get("/dashboard", response_class=HTMLResponse)
async def read_dashboard():
    return dashboard_html
@app.post("/analyze")
async def analyze_merch(file: UploadFile = File(...)):
    try:
        os.makedirs("uploads", exist_ok=True)
        file_path = f"uploads/{file.filename}"
        with open(file_path, "wb") as f:
            f.write(await file.read())
        result = await visual_agent.analyze_image(file_path)
        
        if os.path.exists(file_path):
            os.remove(file_path)
            
        return JSONResponse(content=result)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)
