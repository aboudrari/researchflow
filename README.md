# ResearchFlow 🔬
### Multi-Agent AI Research Assistant — Kaggle AI Agents Capstone 2026

> Type a topic. Four specialized AI agents plan, search, synthesize, and deliver a full research report to your inbox.

---

## What is ResearchFlow?

ResearchFlow is a multi-agent AI system that automates deep research on any topic. Instead of one large model doing everything, it uses four specialized agents that collaborate in sequence — each with a focused role, passing results to the next.

**Track:** Freestyle  
**Course Concepts Applied:** Multi-agent system (ADK), SequentialAgent orchestration, Google Search tool, MCP delivery, agent streaming

---

## Agent Architecture

```
User Input (topic)
        │
        ▼
┌─────────────────┐
│  Planner Agent  │  → Breaks topic into 3-5 focused sub-questions
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Search Agent   │  → Searches the web for each sub-question (google_search tool)
└────────┬────────┘
         │
         ▼
┌──────────────────────┐
│  Synthesizer Agent   │  → Writes a structured research report from findings
└──────────┬───────────┘
           │
           ▼
┌──────────────────┐
│  Delivery Agent  │  → Formats report as email, sends via Gmail MCP
└──────────────────┘
```

Each agent is an `LlmAgent` powered by `gemini-2.0-flash`. The orchestrator is a `SequentialAgent` from Google ADK that coordinates the pipeline, passing conversation context between steps.

---

## Key Course Concepts Used

| Concept | Where |
|---|---|
| Multi-agent system (ADK) | `agent/orchestrator.py` — `SequentialAgent` with 4 sub-agents |
| Agent / LlmAgent | `agent/planner.py`, `searcher.py`, `synthesizer.py`, `delivery.py` |
| Tool use (google_search) | `agent/searcher.py` |
| MCP Server (Gmail) | `agent/delivery.py` — Gmail MCP for report delivery |
| Streaming / SSE | `app.py` — FastAPI Server-Sent Events for live progress |
| Deployability | FastAPI backend + static HTML frontend, Docker-ready |

---

## Tech Stack

- **Google ADK 2.x** — Agent orchestration (`SequentialAgent`, `LlmAgent`)
- **Gemini 2.0 Flash** — LLM powering all 4 agents
- **FastAPI** — REST API backend with SSE streaming
- **Google Search Tool** — Built-in ADK tool for web search
- **Gmail MCP** — Email delivery of final report
- **Vanilla HTML/CSS/JS** — Zero-dependency frontend

---

## Setup Instructions

### 1. Clone the repo
```bash
git clone https://github.com/aboudrari/researchflow
cd researchflow
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure environment
```bash
cp .env.example .env
# Edit .env and add your GOOGLE_API_KEY
```

Get your API key from [Google AI Studio](https://aistudio.google.com).

### 4. Run the backend
```bash
python app.py
# Server starts at http://localhost:8000
```

### 5. Open the frontend
Open `index.html` in your browser (or serve it):
```bash
python -m http.server 3000
# Visit http://localhost:3000
```

### 6. Research something
- Type any topic in the search box
- Optionally enter your email for report delivery
- Watch the four agents work in real time
- Get your report

---

## Project Structure

```
researchflow/
├── agent/
│   ├── __init__.py
│   ├── planner.py        # Planner Agent — breaks topic into sub-questions
│   ├── searcher.py       # Search Agent — web search via google_search tool
│   ├── synthesizer.py    # Synthesis Agent — writes the research report
│   ├── delivery.py       # Delivery Agent — formats & sends via Gmail
│   └── orchestrator.py   # Root SequentialAgent orchestrating the pipeline
├── app.py                # FastAPI backend with SSE streaming
├── index.html            # Frontend UI
├── requirements.txt
├── .env.example
└── README.md
```

---

## Security Notes

- API keys are loaded from `.env` (never committed to git)
- `.env` is in `.gitignore`
- No hardcoded credentials anywhere in the codebase
- Gmail delivery uses OAuth via MCP — no password storage

---

## About the Author

Built by **Abdallah Aboudrari** — AI Engineering student at Cyprus International University, Kaggle AI Agents Intensive Course participant (June 2026).

- GitHub: [@aboudrari](https://github.com/aboudrari)
- Project: [github.com/aboudrari/researchflow](https://github.com/aboudrari/researchflow)

---

*ResearchFlow — Kaggle AI Agents: Intensive Vibe Coding Capstone Project, 2026*
