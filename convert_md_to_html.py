from pathlib import Path
import markdown

MD_FILE = Path("approved_kb_articles.md")
HTML_FILE = Path("approved_kb_articles.html")

def md_to_html():
    if not MD_FILE.exists():
        print(f"❌ {MD_FILE} not found. Run merge_approved_kb.py first.")
        return

    md_text = MD_FILE.read_text(encoding="utf-8")
    html_content = markdown.markdown(md_text, extensions=["extra", "tables", "fenced_code"])

    # Simple HTML wrapper for styling
    full_html = f"""
    <html>
    <head>
        <meta charset="utf-8">
        <title>Knowledge Base Articles</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; }}
            h1, h2, h3 {{ color: #2c3e50; }}
            pre {{ background: #f4f4f4; padding: 10px; }}
            code {{ background: #f4f4f4; padding: 2px 5px; }}
            hr {{ margin: 40px 0; }}
        </style>
    </head>
    <body>
    {html_content}
    </body>
    </html>
    """

    HTML_FILE.write_text(full_html, encoding="utf-8")
    print(f"✅ HTML generated → {HTML_FILE}")

if __name__ == "__main__":
    md_to_html()
