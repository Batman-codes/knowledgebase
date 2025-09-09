KnowledgeBase Builder — README

Turn daily chat transcripts into reviewed Knowledge Base (KB) articles (Markdown + HTML) with a simple, local, LLM-powered pipeline.

Features:
- Parse Slack/Teams-style chats → JSONL
- Extract grounded Q&A pairs per thread using OpenAI
- Generate Markdown KB drafts (status: draft)
- Manual review → set **status:approved**
- Merge approved drafts → single HTML for easy sharing

Prerequisites:
- Python 3.10+
- OpenAI API key
- VS Code (optional)

Set up:
1) Clone & enter
git clone <your-repo-url> KnowledgeBase
cd KnowledgeBase

2) Python env (optional but recommanded)
python -m venv venv
# Windows PowerShell
.\venv\Scripts\Activate
# macOS/Linux
source venv/bin/activate

3) Install Dependency:
pip install markdown python-dotenv openai

4) Config OpenAI
Create .env in the project roo and add the API key:
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxx

Make sure .gitignore is in the root and contains:
.env
venv/
__pycache__/
*.pyc
.DS_Store

Input Format (chat_history.txt)
[2025-09-08 09:12:10] QA (Rahul): Export for Client A failing with 500.
[2025-09-08 09:13:02] Developer (Amit): I deployed a change; checking logs.

[2025-09-08 10:05:30] QA (Priya): Client B submit hangs; 400 on /submitForm.
[2025-09-08 10:08:40] Architect (Vikram): Missing 'participantType' in payload.

Typical Workflow:
Step 1 - Convert TXT -> JSONL
python main.py            # reads ./chat_history.txt, writes ./chat_history.jsonl

Step 2 - Extract Q&A Pairs
python qa_extract.py      # reads ./chat_history.jsonl, writes ./qa_pairs.jsonl

Step 3 - Generate Markdown drafts
python kb_summarize.py    # reads ./qa_pairs.jsonl, writes ./kb_drafts/*.md

Step 4 - Review & Approve 
Manually review the draft, update any error or information needed.
Once done, Set the second line
**status:approved**

Step 5 - Merge Approved -> Single Markdown
python merge_approved_kb.py    # writes ./approved_kb_articles.md

Step 6 - Convert merged Markdown -> HTML
python convert_md_to_html.py   # writes ./approved_kb_articles.html

Step 7 - Open HTML file in browser
# macOS
open approved_kb_articles.html
# Windows
start approved_kb_articles.html
# Linux
xdg-open approved_kb_articles.html

Notes:
To check OPENAI Key is loaded, run test.py file
python test.py     #It will print the key

Next steps:
- Create a python script to pipeline first 3 steps
- Create a python script to pipeline last 3 steps
- Create a diectory outside project to store .txt files and html files
- Change script to delete draft markdown files aftr step 7
- Change scripts to give options to use any otehr LLM tools
