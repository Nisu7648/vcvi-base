import openai, os

openai.api_key = os.getenv("OPENAI_API_KEY", "sk-dummy")

async def review_and_fix(code: str):
    """
    Reviewer AI inspects code for syntax or logic issues
    and returns fixed version + review notes.
    """
    review_msgs = [
        {"role": "system", "content": "You are a senior code reviewer."},
        {"role": "user", "content": f"Find and correct bugs in this code:\n{code}"}
    ]
    review = openai.ChatCompletion.create(model="gpt-4o-mini", messages=review_msgs, max_tokens=1200)
    fixed = review.choices[0].message["content"].strip()

    # Separate note section if provided
    notes = "Auto-review completed. Adjustments applied."
    if "```" in fixed:
        notes = "Code fixed and cleaned."
        fixed = fixed.split("```")[-2] if len(fixed.split("```")) >= 2 else fixed

    return fixed, notes
