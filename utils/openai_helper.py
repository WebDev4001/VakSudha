import os
from openai import OpenAI

# the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
# do not change this unless explicitly requested by the user
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
openai = OpenAI(api_key=OPENAI_API_KEY)

def analyze_speech_content(text):
    try:
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": "Analyze the following speech text for clarity, "
                    "pronunciation patterns, and provide constructive feedback. "
                    "Return JSON with format: "
                    "{'score': float, 'feedback': string, 'improvements': array}"
                },
                {"role": "user", "content": text}
            ],
            response_format={"type": "json_object"}
        )
        return response.choices[0].message.content
    except Exception as e:
        raise Exception(f"Speech analysis failed: {str(e)}")
