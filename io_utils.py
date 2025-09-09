from pathlib import Path
import json

def read_text(p: Path) -> str:
    return p.read_text(encoding="utf-8")

def ensure_parent_dir(p: Path) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)

def write_jsonl(records, out_path: Path) -> int:
    ensure_parent_dir(out_path)
    n = 0
    with out_path.open("w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
            n += 1
    return n
