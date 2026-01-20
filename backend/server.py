import os
from dotenv import load_dotenv

# 1. CRITICAL: Load the API Key FIRST
load_dotenv() 

# Check if key is loaded
if not os.getenv("GOOGLE_API_KEY"):
    print("❌ ERROR: GOOGLE_API_KEY not found. Make sure .env is in the root folder.")

from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

# 2. NOW import the agents (Environment variables are ready)
from core.graph import app as workflow_app
from agents.legacy import legacy_analysis_agent

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class StoryInput(BaseModel):
    user_story: str

class LegacyInput(BaseModel):
    code_snippet: str

@app.post("/generate")
async def generate_app(data: StoryInput):
    print(f"Received Story: {data.user_story}")
    try:
        result = workflow_app.invoke({"user_story": data.user_story})
        return {
            "status": "success",
            # NEW KEYS
            "html_code": result.get("html_code"),
            "css_code": result.get("css_code"),
            "js_code": result.get("js_code"),
            # OLD KEYS
            "backend_code": result.get("backend_code"),
            "database_schema": result.get("database_schema"),
            "test_results": result.get("test_results")
        }
    except Exception as e:
        print(f"Error processing request: {e}")
        return {"status": "error", "message": str(e)}

@app.post("/analyze_legacy")
async def analyze_legacy(data: LegacyInput):
    print("Received Legacy Code for Analysis")
    # This will now use the MOCK logic or Real AI safely
    analysis = legacy_analysis_agent(data.code_snippet)
    return {"status": "success", "analysis": analysis}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)