from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class BuildRequest(BaseModel):
    description: str

@app.get("/")
def root():
    return {"vcvi": "AI Builder online", "status": "ready"}

@app.post("/build")
def build(req: BuildRequest):
    return {"status": "success", "message": f"AI received: {req.description}"}
