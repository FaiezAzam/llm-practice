# LLM Practice — Backend to AI Engineering

My transition from backend engineering (5 years PHP/Node.js) to production AI engineering.

This repository contains the practice projects, tools, and portfolio work I am building during my transition.

## Repository structure

```
llm-practice/
├── api/                    # FastAPI HTTP service (Day 4)
├── src/
│   ├── config.py           # Pydantic settings and logging setup (Day 5)
│   ├── llm_client.py       # Production-style LLM client (Day 2)
│   └── structured.py       # Structured JSON output (Day 3)
├── rag_project/            # RAG knowledge base project (Day 6+)
│   ├── ingestion/
│   ├── retrieval/
│   ├── generation/
│   └── README.md
├── hello_llm.py            # First raw API call (Day 1)
└── README.md
```

## Day 1 — First LLM API call

`hello_llm.py` makes a raw call to OpenRouter and prints the response.

**What it demonstrates:** understanding of the chat completion API shape — system message, user message, model, response structure, token usage.

## Day 2 — Reusable LLM client

`src/llm_client.py` is a production-style client with:

- Retries with exponential backoff for rate limits
- Timeout handling with fixed retry delay
- Automatic fallback to alternative models on API errors
- Token usage tracking

**Why this matters:** LLM APIs fail often. Production AI systems need retry logic, fallback models, and clean error reporting. This client is the foundation for every AI project in this repository.

## Day 3 — Structured output

`src/structured.py` wraps the LLM client to return validated JSON.

**Key features:**

- Asks the LLM for JSON matching a schema
- Strips markdown code fences if the LLM adds them
- Retries once with a stricter prompt if parsing fails
- Returns a dict with `success`, `data`, or `error`

**Why this matters:** Backend systems cannot use free-form text. Structured output turns the LLM into a real data source that your application code can consume.

## Day 4 — FastAPI service

`api/main.py` exposes LLM extraction as a real HTTP API.

### Endpoints

- `GET /health` — service health check
- `POST /extract` — extract structured JSON from text

### Run it

```bash
uvicorn api.main:app --reload
```

Interactive docs available at `http://localhost:8000/docs`.

**What it demonstrates:** Pydantic validation, typed request/response models, proper HTTP status codes (422 for bad input, 502 for upstream failures), auto-generated OpenAPI docs.

## Day 5 — Configuration and logging

- All configuration loaded from `.env` via `pydantic-settings` (`src/config.py`)
- Structured logging with timestamps, levels, and module names
- No hardcoded secrets or configuration values in code

**Why this matters:** Production services do not hardcode API keys or retry counts. Everything comes from the environment. Logging gives you a real diagnostic trail.

## Day 6–8 — RAG knowledge base

See `rag_project/README.md` for the full RAG project.

**Summary so far:**

- PDF ingestion with `pypdf`
- Character-based chunking with overlap and small-tail merging
- Embeddings with `sentence-transformers/all-MiniLM-L6-v2` (384 dimensions)
- Vector storage in Qdrant Cloud
- Retrieval working: natural language queries return correct chunks

## What is coming next

- Day 9 — RAG generation with citations
- Day 10 — FastAPI endpoint for the RAG system
- Day 11 — Evaluation set and accuracy measurement
- Day 12+ — Retrieval improvements, hybrid search, deployment

## Tech stack

- **Python 3.13**
- **FastAPI** — HTTP API
- **Pydantic / pydantic-settings** — validation and configuration
- **OpenAI SDK** (pointing at OpenRouter) — LLM calls
- **sentence-transformers** — local embeddings
- **Qdrant Cloud** — vector database
- **pypdf** — PDF text extraction

## Why this repository exists

I am a backend engineer transitioning into AI engineering. Instead of taking courses and hoping for the best, I am building real, production-style systems that:

- Use my existing backend strengths (APIs, config, logging, error handling)
- Add real AI capabilities (LLM clients, RAG, embeddings, vector search)
- Come with tests, evaluations, and honest limitations

The goal is not a portfolio of demos. The goal is a portfolio of systems I can defend in an interview.