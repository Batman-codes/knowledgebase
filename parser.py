import re
from typing import Iterable, Dict, List

# Slack-style line: [timestamp] Role (Name): message
LINE_RE = re.compile(r'^\[(.*?)\]\s+(\w+)\s+\((.*?)\):\s+(.*)$')

def split_threads(raw_text: str) -> List[str]:
    """Split threads by one-or-more blank lines."""
    blocks = [b.strip() for b in re.split(r'\n\s*\n', raw_text) if b.strip()]
    return blocks

def parse_thread(thread_text: str, thread_idx: int, channel: str) -> Iterable[Dict]:
    """
    Yield per-message dicts for a thread.
    thread_idx is 1-based; message_id is 1-based within a thread.
    """
    msg_id = 1
    for line in thread_text.splitlines():
        m = LINE_RE.match(line)
        if not m:
            # skip non-matching lines silently; could log if needed
            continue
        timestamp, role, author, text = m.groups()
        yield {
            "channel": channel,
            "thread_id": f"T{thread_idx}",
            "message_id": f"m{msg_id}",
            "timestamp": timestamp,
            "role": role,
            "author": author,
            "text": text
        }
        msg_id += 1
