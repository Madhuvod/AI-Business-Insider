import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from crew import NewsSummarizerAnalyzerCrew
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

# Load environment variables from .env file
load_dotenv()

app = FastAPI()

# Get the absolute path to the static directory
current_dir = os.path.dirname(os.path.abspath(__file__))
static_dir = os.path.join(os.path.dirname(os.path.dirname(current_dir)), "static")

# Mount the static files directory
app.mount("/static", StaticFiles(directory=static_dir), name="static")

class TopicRequest(BaseModel):
    topic: str

@app.get("/", response_class=HTMLResponse)
async def read_index():
    with open(os.path.join(static_dir, "index.html")) as f:
        return HTMLResponse(f.read())

@app.post("/analyze")
async def analyze_topic(request: TopicRequest):
    crew = NewsSummarizerAnalyzerCrew()
    try:
        result = crew.kickoff(request.topic)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
