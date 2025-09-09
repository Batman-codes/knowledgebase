# kb_prompts.py

SYSTEM_KB = """You turn grounded Q&A into concise Knowledge Base (KB) articles.
Rules:
- Use ONLY provided Q&A content; do not invent facts.
- Be crisp and actionable. Prefer bullet points for Steps/Resolution.
- If info missing, omit that section.
- Output Markdown only, no backticks.
Sections in order: Title, Problem, Environment, Steps, Expected, Actual, Resolution, Notes."""

USER_KB_TEMPLATE = """Thread: {thread_id}

Q&A items (each has grounded content and sources):
{qa_block}

Create ONE KB article in Markdown with sections:
# <Title>
**Problem**
**Environment**
**Steps**
**Expected**
**Actual**
**Resolution**
**Notes**"""

def render_user_kb(thread_id: str, qa_items: list[dict]) -> str:
    # qa_items: [{"question","answer","sources","confidence"}]
    lines = []
    for i, it in enumerate(qa_items, 1):
        sources = ", ".join(it.get("sources", []))
        lines.append(f"{i}. Q: {it.get('question','').strip()}\n   A: {it.get('answer','').strip()}\n   sources: [{sources}]  conf={it.get('confidence',0)}")
    qa_block = "\n".join(lines) if lines else "(none)"
    return USER_KB_TEMPLATE.format(thread_id=thread_id, qa_block=qa_block)