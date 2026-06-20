from google.adk.agents import LlmAgent

PLANNER_PROMPT = '''You are a research planning expert. Take a broad research topic
and break it down into exactly 3 to 5 focused, specific sub-questions that together
give a comprehensive understanding of the topic.

Rules:
- Each sub-question must be specific and searchable
- Questions should cover different angles (overview, key players, recent developments, challenges, future)
- Output ONLY a numbered list of questions, nothing else
- No preamble, no explanation, just the questions
'''

planner_agent = LlmAgent(
    name='planner_agent',
    model='gemini-2.0-flash',
    description='Breaks a research topic into 3-5 specific sub-questions for targeted research.',
    instruction=PLANNER_PROMPT,
)
