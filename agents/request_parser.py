import json
from openai import OpenAI

import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

class RequestParserAgent:

    def run(self, user_request):

        prompt = f"""
Extract the travel information from the user's request.

Return ONLY valid JSON.

Example:
{{
    "city": "Madinah",
    "days": 3,
}}

User Request:
{user_request}
"""

        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            response_format={"type": "json_object"},
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        result = response.choices[0].message.content
        print("===== LLM Response =====")
        print(repr(result))
        print("========================")

        return json.loads(result)