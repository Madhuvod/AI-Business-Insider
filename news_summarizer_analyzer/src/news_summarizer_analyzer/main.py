import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from crew import NewsSummarizerAnalyzerCrew

load_dotenv()

app = FastAPI()

crew = NewsSummarizerAnalyzerCrew()

class TopicRequest(BaseModel):
    topic: str

@app.post("/analyze")
async def analyze_topic(request: TopicRequest) -> dict:
    """
    Analyzes a given topic using the NewsSummarizerAnalyzerCrew.
    
    Args:
        request (TopicRequest): The request containing the topic to analyze
        
    Returns:
        dict: Analysis results for the given topic
        
    Raises:
        HTTPException: If analysis fails
    """
    try:
        crew_output = crew.kickoff(request.topic)
        
    
        result = {
            "summary": crew_output.raw,
            "tasks": [
                {
                    "description": task.description,
                    "output": task.raw
                }
                for task in crew_output.tasks_output
            ]
        }
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
