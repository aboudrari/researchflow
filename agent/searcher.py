from google.adk.agents import LlmAgent
from google.adk.tools import google_search

SEARCHER_PROMPT = '''You are a web research specialist. You will receive a numbered list of research sub-questions.

For each question:
1. Use the google_search tool to search for current, relevant information
2. Collect the most useful facts, data points, and insights from results
3. Label each section clearly with the question number

Output format:
## Question 1: [question text]
[Key findings from search - bullet points, facts, quotes, data]

## Question 2: [question text]
[Key findings from search]

Be thorough but focused. Prioritize recent sources (2025-2026).
'''

searcher_agent = LlmAgent(
    name='searcher_agent',
    model='groq/llama-3.3-70b-versatile',
    description='Searches the web for each research sub-question and collects raw findings.',
    instruction=SEARCHER_PROMPT,
    tools=[google_search],
)
