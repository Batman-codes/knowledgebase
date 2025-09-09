# kb_summarize.py
from pathlib import Path
import json
from collections import defaultdict
import re
from typing import Dict, List

from kb_prompts import SYSTEM_KB, render_user_kb
from llm_client import call_llm_json  # we'll use the same client but ask for text

# ---- Config (flat layout) ----
INPUT_QA = Path("qa_pairs.jsonl")
OUT_DIR = Path("kb_drafts")
MODEL = "gpt-4o-mini"
CONF_MIN = 0.55  # drop low-confidence pairs

def _safe_filename(title: str) -> str:
    t = title.strip()[:120]
    t = re.sub(r"[^\w\-\. ]+", "", t)
    t = re.sub(r"\s+", "_", t)
    return t or "kb_article"

def _extract_title(md: str) -> str:
    # Get first markdown H1 if present
    m = re.search(r"^\s*#\s+(.+)$", md, flags=re.MULTILINE)
    return m.group(1).strip() if m else "KB_Article"

def _llm_markdown(system: str, user: str, model: str) -> str:
    """
    Reuse call_llm_json but allow plain text by wrapping result.
    If the model returns JSON by mistake, convert to markdown-ish string.
    """
    # Trick: ask for JSON, but if it's text the normalizer returns [].
    # So call model without forcing JSON: we’ll implement a lightweight text call.
    try:
        # Minimal text call via chat.completions returning content string
        from openai import OpenAI  # type: ignore
        import os
        from dotenv import load_dotenv
        load_dotenv()
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        resp = client.chat.completions.create(
            model=model,
            temperature=0.2,
            messages=[{"role":"system","content":system},{"role":"user","content":user}],
        )
        return (resp.choices[0].message.content or "").strip()
    except Exception as e:
        print("❌ LLM text call failed:", e)
        return ""

def load_qa(path: Path) -> Dict[str, List[dict]]:
    """
    Load qa_pairs.jsonl and group by thread_id.
    Each line: {"thread_id","question","answer","sources","confidence",...}
    """
    buckets: Dict[str, List[dict]] = defaultdict(list)
    with path.open("r", encoding="utf-8") as f:
        for i, line in enumerate(f, 1):
            s = line.strip()
            if not s:
                continue
            try:
                obj = json.loads(s)
            except json.JSONDecodeError as e:
                print(f"❌ Bad JSON in {path} line {i}: {e}")
                continue
            buckets[obj["thread_id"]].append(obj)
    return buckets

def render_fallback_md(thread_id: str, qa_items: List[dict]) -> str:
    # Simple, deterministic Markdown if LLM fails
    lines = [f"# Draft Article for {thread_id}", "", "**Problem**", "- See Q&A below"]
    lines += ["", "**Steps**"]
    for i, it in enumerate(qa_items, 1):
        lines.append(f"- Q{i}: {it.get('question','').strip()}")
        lines.append(f"  - A: {it.get('answer','').strip()}")
    lines += ["", "**Resolution**", "- See accepted answers above."]
    return "\n".join(lines)

def write_md(md: str, out_dir: Path) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    title = _extract_title(md)
    fname = _safe_filename(title) + ".md"
    path = out_dir / fname
    path.write_text(md, encoding="utf-8")
    return path

def summarize_thread(thread_id: str, qa_items: List[dict]) -> Path | None:
    # filter by confidence
    filt = [q for q in qa_items if float(q.get("confidence", 0)) >= CONF_MIN]
    if not filt:
        # if all low confidence, keep top 1 as seed
        filt = sorted(qa_items, key=lambda x: float(x.get("confidence", 0)), reverse=True)[:1]
        if not filt:
            return None

    user = render_user_kb(thread_id, filt)
    md = _llm_markdown(SYSTEM_KB, user, model=MODEL).strip()
    if not md:
        md = render_fallback_md(thread_id, filt)
    return write_md(md, OUT_DIR)

def run(input_path: Path = INPUT_QA, out_dir: Path = OUT_DIR) -> int:
    input_path = Path(input_path)
    out_dir = Path(out_dir)
    threads = load_qa(input_path)
    count = 0
    for tid, items in threads.items():
        p = summarize_thread(tid, items)
        if p:
            count += 1
            print(f"📝 Wrote: {p}")
    print(f"✅ Generated {count} Markdown drafts → {out_dir}")
    return count

if __name__ == "__main__":
    run()
