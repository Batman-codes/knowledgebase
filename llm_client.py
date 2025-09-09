from typing import Any, Dict, List

# Minimal abstraction. Implement ONE of the clients below.

# ---------- Option A: OpenAI (sdk >= 1.0) ----------
import os, json, re
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()  # loads variables from .env file
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

_CODE_FENCE_RE = re.compile(r"^```(?:json)?\s*([\s\S]*?)\s*```$", re.IGNORECASE)

def _strip_code_fences(s: str) -> str:
    m = _CODE_FENCE_RE.match(s.strip())
    return m.group(1) if m else s

def _normalize_jsonish(obj):
    """
    Accepts list/dict/string and returns a list of dicts for items.
    Supports: list, {"items":[...]}, {"data":[...]}, stringified JSON.
    """
    if obj is None:
        return []
    if isinstance(obj, list):
        return obj
    if isinstance(obj, dict):
        for k in ("items", "data", "qa", "pairs"):
            if k in obj and isinstance(obj[k], list):
                return obj[k]
        # single object -> wrap
        return [obj]
    if isinstance(obj, str):
        s = _strip_code_fences(obj)
        try:
            j = json.loads(s)
            return _normalize_jsonish(j)
        except Exception:
            # Not JSON; return empty so caller won’t crash
            return []
    # Unknown -> empty
    return []

def call_llm_json(system: str, user: str, model: str = "gpt-4o-mini"):
    try:
        resp = client.chat.completions.create(
            model=model,
            temperature=0.2,
            messages=[{"role":"system","content":system},{"role":"user","content":user}],
            response_format={"type":"json_object"}  # model should return JSON
        )
        content = resp.choices[0].message.content or ""
        # Try primary parse
        try:
            data = json.loads(content)
        except Exception:
            # content might itself be a JSON-looking string or fenced
            data = _strip_code_fences(content)
            try:
                data = json.loads(data)
            except Exception:
                # As a last resort, normalize directly (may return [])
                return _normalize_jsonish(content)
        return _normalize_jsonish(data)
    except Exception as e:
        print("❌ LLM call failed:", e)
        return []