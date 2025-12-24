import os
from dotenv import load_dotenv
from openai import OpenAI

# Always load .env even if Streamlit didn't
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY", "").strip()

# Helpful error if missing
if not api_key:
    raise RuntimeError(
        "OPENAI_API_KEY is missing. Put it in the .env file as: OPENAI_API_KEY=your_key"
    )

client = OpenAI(api_key=api_key)

SYSTEM_PROMPT = """
You are an elite AI sales assistant.
You sell AI prompts, AI automation, AI toolkits, and AI SaaS.
You identify user needs and recommend the best product.
You upsell naturally and close sales confidently.
"""

def sales_chat(user_message: str) -> str:
    resp = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message},
        ],
        temperature=0.7,
    )
    return resp.choices[0].message.content