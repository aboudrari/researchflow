import os
import asyncio
import json
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai.types import Content, Part

load_dotenv()

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
if not GOOGLE_API_KEY:
    raise RuntimeError('GOOGLE_API_KEY not set in .env')

app = FastAPI(title='ResearchFlow API')

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*'],
    allow_headers=['*'],
)

session_service = InMemorySessionService()
APP_NAME = 'researchflow'
USER_ID = 'user_1'

class ResearchRequest(BaseModel):
    topic: str
    email: str | None = None

@app.get('/health')
async def health():
    return {'status': 'ok', 'version': '1.0.0'}

@app.post('/research')
async def research(req: ResearchRequest):
    if not req.topic or len(req.topic.strip()) < 3:
        raise HTTPException(status_code=400, detail='Topic must be at least 3 characters.')

    from agent.orchestrator import root_agent

    async def stream_pipeline():
        def emit(stage, status, content=''):
            payload = json.dumps({'stage': stage, 'status': status, 'content': content})
            return f'data: {payload}\n\n'

        try:
            session_id = f'session_{asyncio.get_event_loop().time()}'
            await session_service.create_session(
                app_name=APP_NAME,
                user_id=USER_ID,
                session_id=session_id,
            )

            runner = Runner(
                agent=root_agent,
                app_name=APP_NAME,
                session_service=session_service,
            )

            topic_msg = req.topic
            if req.email:
                topic_msg += f'\n\nDeliver the final report to: {req.email}'

            user_message = Content(
                role='user',
                parts=[Part(text=topic_msg)],
            )

            stage_labels = {
                'planner_agent': ('Planning', 'Breaking your topic into research questions...'),
                'searcher_agent': ('Searching', 'Searching the web for each question...'),
                'synthesizer_agent': ('Synthesizing', 'Writing your research report...'),
                'delivery_agent': ('Delivering', 'Preparing your email report...'),
            }

            yield emit('start', 'running', f'Starting ResearchFlow for: {req.topic}')

            final_report = ''
            current_stage = None

            async for event in runner.run_async(
                user_id=USER_ID,
                session_id=session_id,
                new_message=user_message,
            ):
                agent_name = getattr(event, 'author', None)

                if agent_name and agent_name in stage_labels:
                    label, description = stage_labels[agent_name]
                    if agent_name != current_stage:
                        current_stage = agent_name
                        yield emit(label, 'running', description)

                if hasattr(event, 'content') and event.content:
                    for part in event.content.parts:
                        if hasattr(part, 'text') and part.text:
                            yield emit(
                                stage_labels.get(agent_name, ('Processing', ''))[0] if agent_name else 'Processing',
                                'streaming',
                                part.text,
                            )
                            final_report = part.text

            yield emit('complete', 'done', final_report)

        except Exception as e:
            yield emit('error', 'failed', str(e))

    return StreamingResponse(
        stream_pipeline(),
        media_type='text/event-stream',
        headers={'Cache-Control': 'no-cache', 'X-Accel-Buffering': 'no'},
    )

if __name__ == '__main__':
    import uvicorn
    uvicorn.run('app:app', host='0.0.0.0', port=8000, reload=True)
