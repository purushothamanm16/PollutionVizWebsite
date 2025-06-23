from openai import OpenAI
import json
from dotenv import load_dotenv
import os

load_dotenv()
key = os.getenv("OPENAI_API_KEY")

client = OpenAI(
    api_key=key,
    base_url="https://api.groq.com/openai/v1"
)

def ask_groq(prompt: str) -> dict:
    response = client.chat.completions.create(
        model="llama3-70b-8192",  
        messages=[
            {
                "role": "system",
                "content": (
                    "You are Clarity, an AI that returns pollution-related explanations "
                    "in strict JSON format with keys: object, causes, effects. "
                    "Always use less words, and use simpler and understandable words"
                    "Always assume pollutant units as:\n"
                    "- CO: ppb\n"
                    "- NO2: ppb\n"
                    "- O3: µg/m³\n"
                    "- PM10: µg/m³\n"
                    "- PM2.5: µg/m³"
                )
            },
            {"role": "user", "content": prompt}
        ]
    )
    content = response.choices[0].message.content
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        return {"error": "Failed to parse AI response as JSON", "raw_output": content}