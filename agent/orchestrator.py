from google.adk.agents import SequentialAgent
from agent.planner import planner_agent
from agent.searcher import searcher_agent
from agent.synthesizer import synthesizer_agent
from agent.delivery import delivery_agent

root_agent = SequentialAgent(
    name='researchflow_orchestrator',
    description=(
        'ResearchFlow: A multi-agent research assistant. '
        'Given a topic, it plans sub-questions, searches the web, '
        'synthesizes findings into a report, and prepares email delivery.'
    ),
    sub_agents=[
        planner_agent,
        searcher_agent,
        synthesizer_agent,
        delivery_agent,
    ],
)
