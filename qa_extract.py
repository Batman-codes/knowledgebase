# qa_extract.py
from pathlib import Path
import json
from collections import defaultdict
from typing import Dict, List

# These modules should also be in the project root now
from qa_prompts import SYSTEM_QA, render_user_qa
from llm_client import call_llm_json

# === Defaults for flat project layout ===
DEFAULT_INPUT = Path("chat_history.jsonl")   # <- root-level input
DEFAULT_OUTPUT = Path("qa_pairs.jsonl")      # <- root-level output


def load_threads(jsonl_path) -> Dict[str, List[dict]]:
    """Load messages from JSONL (one JSON object per line) and group by thread_id."""
    jsonl_path = Path(jsonl_path)
    threads: Dict[str, List[dict]] = defaultdict(list)

    with jsonl_path.open("r", encoding="utf-8") as f:
        for i, line in enumerate(f, start=1):
            s = line.strip()
            if not s:
                continue
            try:
                msg = json.loads(s)
            except json.JSONDecodeError as e:
                print(f"❌ JSON error in {jsonl_path} at line {i}: {e.msg} (pos {e.pos})")
                print(f"   Offending line: {s[:160]}...")
                continue  # skip bad lines rather than fail hard
            threads[msg["thread_id"]].append(msg)

    # Ensure per-thread message order
    for tid in threads:
        try:
            threads[tid].sort(key=lambda m: int(m["message_id"].lstrip("m")))
        except Exception:
            threads[tid].sort(key=lambda m: m.get("timestamp", ""))

    return threads


def validate_items(items) -> List[dict]:
    """
    Normalize and validate model output into a list of dicts:
    [{"question":"","answer":"","sources":["m1","m2"],"confidence":0.0}, ...]
    Accepts list/dict/string (including code-fenced JSON).
    """
    # If it's a raw string, try to parse JSON (strip fences if needed)
    if isinstance(items, str):
        s = items.strip()
        if s.startswith("```"):
            # strip code fences
            s = s.strip("`").strip()
            # after stripping, it might still include 'json' header
            if s.lower().startswith("json"):
                s = s[4:].strip()
        try:
            items = json.loads(s)
        except Exception:
            return []

    # If it's a dict, look for common containers
    if isinstance(items, dict):
        for k in ("items", "data", "qa", "pairs"):
            if k in items and isinstance(items[k], list):
                items = items[k]
                break
        else:
            # single-object -> wrap
            items = [items]

    if not isinstance(items, list):
        return []

    out = []
    for it in items:
        if isinstance(it, str):
            try:
                it = json.loads(it)
            except Exception:
                continue
        if not isinstance(it, dict):
            continue
        q = (it.get("question") or "").strip()
        a = (it.get("answer") or "").strip()
        sources = it.get("sources") or []
        try:
            conf = float(it.get("confidence", 0.0))
        except Exception:
            conf = 0.0
        if not q:
            continue
        conf = max(0.0, min(conf, 1.0))
        sources = [s.strip() for s in sources if isinstance(s, str) and s.strip()]
        out.append({"question": q, "answer": a, "sources": sources, "confidence": conf})
    return out


def extract_qa_for_thread(tid: str, messages: List[dict], max_pairs: int = 5, model: str = "gpt-4o-mini") -> List[dict]:
    user_prompt = render_user_qa(tid, messages, max_pairs=max_pairs)
    raw = call_llm_json(SYSTEM_QA, user_prompt, model=model)
    return validate_items(raw)


def run(input_path=DEFAULT_INPUT, output_path=DEFAULT_OUTPUT, model: str = "gpt-4o-mini", max_pairs: int = 5) -> int:
    input_path = Path(input_path)
    output_path = Path(output_path)

    threads = load_threads(input_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    total = 0
    with output_path.open("w", encoding="utf-8") as out:
        for tid, msgs in threads.items():
            items = extract_qa_for_thread(tid, msgs, max_pairs=max_pairs, model=model)
            for it in items:
                rec = {
                    "thread_id": tid,
                    "channel": msgs[0].get("channel", "product-support"),
                    "question": it["question"],
                    "answer": it["answer"],
                    "sources": it["sources"],
                    "confidence": it["confidence"]
                }
                out.write(json.dumps(rec, ensure_ascii=False) + "\n")
                total += 1

    print(f"✅ Wrote {total} Q&A pairs → {output_path}")
    return total


if __name__ == "__main__":
    # Simple defaults; customize via kwargs or edit the constants above.
    run()
