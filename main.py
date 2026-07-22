from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

from agent import run_agent

app = FastAPI(
    title="AutoResearcher API",
    description="An AI Agent that researches topics on the web and returns comprehensive markdown reports.",
    version="1.0.0"
)

class ResearchRequest(BaseModel):
    topic: str

class ResearchResponse(BaseModel):
    topic: str
    report: str

@app.post("/api/research", response_model=ResearchResponse)
def research_topic(request: ResearchRequest):
    """
    Given a topic, the agent will search the web and write a comprehensive markdown report.
    Note: This is a synchronous endpoint. The request will hang until the agent finishes.
    """
    if not request.topic.strip():
        raise HTTPException(status_code=400, detail="Topic cannot be empty.")
        
    try:
        # Run the ReAct agent loop
        report = run_agent(request.topic)
        
        if report.startswith("Error"):
            raise HTTPException(status_code=500, detail=report)
            
        return ResearchResponse(
            topic=request.topic,
            report=report
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    # To run locally: python main.py
    # Or: uvicorn main:app --reload
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
