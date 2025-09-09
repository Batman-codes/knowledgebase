import os
from dotenv import load_dotenv

# Only needed if you use a .env file
load_dotenv()

key = os.getenv("OPENAI_API_KEY")
if key:
    print("✅ OpenAI API key detected. Length:", len(key))
else:
    print("❌ No OpenAI API key found. Check your environment or .env file.")