import os, re, openai
from datetime import datetime

openai.api_key = os.getenv("OPENAI_API_KEY", "sk-dummy")

def clean_code_blocks(text: str) -> str:
    match = re.search(r"```(?:\w+)?\n([\s\S]*?)```", text)
    return match.group(1) if match else text

async def thinker_ai(prompt: str) -> str:
    """Breaks the idea into clear architecture steps."""
    messages = [
        {"role": "system", "content": "You are GPT-5, an expert software architect."},
        {"role": "user", "content": f"Analyze and outline implementation plan:\n{prompt}"}
    ]
    res = openai.ChatCompletion.create(model="gpt-4o-mini", messages=messages, max_tokens=700)
    return res.choices[0].message["content"].strip()

async def coder_ai(plan: str) -> str:
    """Writes full code based on the plan."""
    messages = [
        {"role": "system", "content": "You are Cursor, an autonomous coder."},
        {"role": "user", "content": f"Write production-ready code for this plan:\n{plan}"}
    ]
    res = openai.ChatCompletion.create(model="gpt-4o-mini", messages=messages, max_tokens=1600)
    return res.choices[0].message["content"].strip()

def save_code(project: str, code: str):
    """Creates project folder & saves code."""
    base = os.path.join(os.path.dirname(__file__), "..", "workspace")
    os.makedirs(base, exist_ok=True)

    proj_path = os.path.join(base, project)
    os.makedirs(proj_path, exist_ok=True)

    fname = f"build_{datetime.now().strftime('%Y%m%d_%H%M%S')}.py"
    fpath = os.path.join(proj_path, fname)
    with open(fpath, "w", encoding="utf-8") as f:
        f.write(code)
    return fpath
