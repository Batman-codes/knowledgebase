from pathlib import Path

KB_DIR = Path("kb_drafts")
MERGED_MD = Path("approved_kb_articles.md")

def merge_approved():
    articles = []
    for md_file in sorted(KB_DIR.glob("*.md")):
        content = md_file.read_text(encoding="utf-8").strip()
        if "**status:approved**" in content:
            articles.append(content)

    if not articles:
        print("❌ No approved KB articles found.")
        return

    MERGED_MD.write_text("\n\n---\n\n".join(articles), encoding="utf-8")
    print(f"✅ Merged {len(articles)} approved articles → {MERGED_MD}")

if __name__ == "__main__":
    merge_approved()
