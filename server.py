from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uuid
from dotenv import load_dotenv
load_dotenv()
from repo_rector.orchestrator import Orchestrator

app = FastAPI(title="CodeNova API", description="API for the CodeNova AI Agent")

# In-memory store for orchestrators (in a real app, use a DB or redis)
sessions = {}

class AgentRequest(BaseModel):
    instruction: str
    session_id: str = None

class AgentResponse(BaseModel):
    session_id: str
    response: str
    status: str

@app.post("/api/v1/agent/run", response_model=AgentResponse)
async def run_agent(req: AgentRequest):
    try:
        session_id = req.session_id or str(uuid.uuid4())
        
        if session_id not in sessions:
            sessions[session_id] = Orchestrator(session_id=session_id)
            
        orchestrator = sessions[session_id]
        response_text = orchestrator.run(req.instruction)
        
        return AgentResponse(
            session_id=session_id,
            response=response_text,
            status=orchestrator.session.state.status.value
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/agent/status/{session_id}")
async def get_status(session_id: str):
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
        
    orchestrator = sessions[session_id]
    return {
        "session_id": session_id,
        "status": orchestrator.session.state.status.value,
        "completed_steps": len(orchestrator.session.state.completed_steps),
        "errors": orchestrator.session.state.errors
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
