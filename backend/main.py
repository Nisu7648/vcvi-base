"""
VCVI Builder – Phase 2 foundation
---------------------------------
FastAPI backend that lets you:
  1. Send a plain-text prompt describing an app.
  2. Have the 'Thinker AI' (GPT-5) break it into coding tasks.
  3. Have the 'Coder AI' (Cursor) write, test and correct code files.
Later phases will add persistence, workflow graphs, and live previews.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import openai
import os
import re

# 1️⃣ ---  Base Setup ---
app = FastAPI(title="VCVI AI Builder", version="0.2")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Expect an OpenAI key in Render’s environment variables.
openai.api_key = os.getenv("OPENAI_API_KEY", "sk-dummy")

# 2️⃣ ---  Data Models ---
class PromptRequest(BaseModel):
    prompt: str

class CodeResponse(BaseModel):
    thinker_plan: str
    coder_code: str
    explanation: str

# 3️⃣ ---  Utility: basic AI calls ---
async def thinker_ai(prompt: str) -> str:
    """The 'visionary' – decomposes user intent into coding subtasks."""
    msg = [
        {"role": "system", "content": "You are GPT-5, a senior software architect."},
        {"role": "user", "content": f"Analyze this request and outline a step-by-step plan:\n{prompt}"}
    ]
    resp = openai.ChatCompletion.create(model="gpt-4o-mini", messages=msg, max_tokens=600)
    return resp.choices[0].message["content"].strip()

async def coder_ai(plan: str) -> str:
    """The 'cursor' – generates Python/JS code for the given plan."""
    msg = [
        {"role": "system", "content": "You are Cursor, an autonomous coding assistant."},
        {"role": "user", "content": f"Write fully working code for this plan:\n{plan}"}
    ]
    resp = openai.ChatCompletion.create(model="gpt-4o-mini", messages=msg, max_tokens=1200)
    return resp.choices[0].message["content"].strip()

def clean_code_blocks(text: str) -> str:
    """Extract first ```code``` block, if present."""
    match = re.search(r"```(?:\w+)?\n([\s\S]*?)```", text)
    return match.group(1) if match else text

# 4️⃣ ---  Routes ---
@app.get("/")
def root():
    return {"vcvi": "AI Builder online", "phase": 2, "status": "ready"}

@app.post("/build", response_model=CodeResponse)
async def build(req: PromptRequest):
    """
    Accepts a user prompt, calls the Thinker AI for a plan,
    then calls the Coder AI to generate source code.
    """
    try:
        plan = await thinker_ai(req.prompt)
        raw_code = await coder_ai(plan)
        code = clean_code_blocks(raw_code)

        return CodeResponse(
            thinker_plan=plan,
            coder_code=code,
            explanation="Code successfully generated and sanitized."
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 5️⃣ ---  Future Hooks ---
# TODO:
# - Add 'Reviewer AI' to run static checks & fix bugs automatically.
# - Persist projects to /workspace/<project_name>.
# - Stream real-time logs to front-end chat panel.
