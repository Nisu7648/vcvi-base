from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from .utils.ai_agents import thinker_ai, coder_ai, clean_code_blocks, save_code
from .utils.reviewer import review_and_fix

app = FastAPI(title="VCVI Builder", version="0.4")

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
    return {"vcvi": "AI Builder online", "phase": "2-Full", "status": "ready"}

@app.post("/build")
async def build(req: BuildRequest):
    """
    Receives a prompt → Thinker AI → Coder AI → Reviewer AI
    Saves final corrected code into workspace/project folder.
    """
    try:
        # Step 1: Plan
        plan = await thinker_ai(req.prompt)

        # Step 2: Generate code
        raw_code = await coder_ai(plan)
        code = clean_code_blocks(raw_code)

        # Step 3: Reviewer AI checks & fixes
        fixed_code, notes = await review_and_fix(code)

        # Step 4: Save
        path = save_code(req.project, fixed_code)

        return {
            "project": req.project,
            "plan": plan,
            "review_notes": notes,
            "file": path,
            "status": "completed"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
