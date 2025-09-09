SYSTEM_QA = """You extract Q&A pairs from chat threads. 
Rules:
- Use ONLY the provided messages.
- Prefer exact phrasing from messages; be concise.
- Include message_ids that support each question and answer.
- If no clear answer, set answer="" and confidence=0.3.
Return JSON as: [{"question":"","answer":"","sources":["m1","m2"],"confidence":0.0}]"""

USER_QA_TEMPLATE = """Thread: {thread_id}
Messages (ordered):
{messages}

Extract up to {max_pairs} Q&A pairs that reflect real issues and resolutions.
"""

def render_user_qa(thread_id: str, messages: list[dict], max_pairs: int = 5) -> str:
    msgs = []
    for m in messages:
        msgs.append(f'{m["timestamp"]} {m["role"]} ({m["author"]}) [{m["message_id"]}]: {m["text"]}')
    return USER_QA_TEMPLATE.format(thread_id=thread_id, messages="\n".join(msgs), max_pairs=max_pairs)