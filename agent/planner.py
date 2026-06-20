import os
from groq import Groq

client = Groq(api_key=os.getenv('GROQ_API_KEY'))

def run_planner(topic: str) -> str
    response = client.chat.completions.create(
        model='llama-3.3-70b-versatile',
        messages=[
            {'role': 'system', 'content': '''You are a research planning expert. Take a broad research topic
and break it down into exactly 3 to 5 focused, specific sub-questions.

Rules:
- Each sub-question must be specific and searchable
- Cover different angles: overview, key players, recent developments, challenges, future
- Output ONLY a numbered list of questions, nothing else'''},
            {'role': 'user', 'content': f'Research topic: {topic}'}
        ]
    )
    return response.choices[0].message.content
