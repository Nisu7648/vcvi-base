# Handles AI calls and workspace operations
import os, re, openai, json
from datetime import datetime

openai.api_key = os.getenv("OPENAI_API_KEY", "sk-dummy")

def clean_code_blocks(text: str) -> str:
    match = re.search(r"```(?:\w+)?\n([\s\S]*?)```", text)
    return match.group(1) if match else text

async def thinker_ai(prompt: str) -> str:
    messages = [
        {"role": "system", "content": "You are GPT-5, an expert architect."},
        {"role": "user", "content": f"Break this idea into steps:\n{prompt}"}
    ]
    res = openai.ChatCompletion.create(model="gpt-4o-mini", messages=messages, max_tokens=600)
    return res.choices[0].message["content"].strip()

async def coder_ai(plan: str) -> str:
    messages = [
        {"role": "system", "content": "You are Cursor, an autonomous coder."},
        {"role": "user", "content": f"Generate full code for this plan:\n{plan}"}
    ]
    res = openai.ChatCompletion.create(model="gpt-4o-mini", messages=messages, max_tokens=1500)
    return res.choices[0].message["content"].strip()

def save_code(project: str, code: str):
    """Creates project folder and saves the code."""
    workspace = os.path.join(os.path.dirname(__file__), "..", "workspace")
    os.makedirs(workspace, exist_ok=True)

    project_path = os.path.join(workspace, project)
    os.makedirs(project_path, exist_ok=True)

    file_path = os.path.join(project_path, f"build_{datetime.now().strftime('%Y%m%d_%H%M%S')}.py")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(code)
    return file_path
