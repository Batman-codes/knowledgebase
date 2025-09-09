import json
import re
from pathlib import Path



# Default input/output locations
input_file = "chat_history.txt"
output_file = "chat_history.jsonl"

# Regex pattern to parse each message line
line_pattern = re.compile(r'^\[(.*?)\]\s+(\w+)\s+\((.*?)\):\s+(.*)$')

# Read input file
with open(input_file, "r", encoding="utf-8") as f:
    content = f.read().strip()

# Split threads by blank line
threads = [t.strip() for t in content.split("\n\n") if t.strip()]

jsonl_lines = []
thread_id = 1

for thread in threads:
    lines = thread.split("\n")
    message_id = 1
    for line in lines:
        match = line_pattern.match(line)
        if match:
            timestamp, role, author, text = match.groups()
            json_obj = {
                "channel": "product-support",
                "thread_id": f"T{thread_id}",
                "message_id": f"m{message_id}",
                "timestamp": timestamp,
                "role": role,
                "author": author,
                "text": text
            }
            jsonl_lines.append(json_obj)
            message_id += 1
    thread_id += 1

# Write to JSONL file
with open(output_file, "w", encoding="utf-8") as f:
    for obj in jsonl_lines:
        f.write(json.dumps(obj) + "\n")

print(f"✅ Converted {len(jsonl_lines)} messages into {output_file}")