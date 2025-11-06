from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from .utils.ai_agents import thinker_ai, coder_ai, clean_code_blocks, save_code

app = FastAPI(title="VCVI Builder", version="0.3")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class BuildRequest(BaseModel):
    project: str
    prompt: str

@app.get("/")
def root():
    return {"vcvi": "AI Builder online", "phase": "2-A", "status": "ready"}

@app.post("/build")
async def build(req: BuildRequest):
    try:
        plan = await thinker_ai(req.prompt)
        raw_code = await coder_ai(plan)
        code = clean_code_blocks(raw_code)
        path = save_code(req.project, code)
        return {
            "project": req.project,
            "plan": plan,
            "file": path,
            "status": "saved"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
