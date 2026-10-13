# RAG Knowledge Base

A production-style Retrieval-Augmented Generation (RAG) system that answers questions about a set of documents with source citations.

## Goal

Build a real AI-powered question-answering system that:
- Ingests documents (PDF, text)
- Chunks and embeds them
- Stores embeddings in a real vector database
- Retrieves relevant chunks for a user query
- Generates answers with source citations
- Evaluates answer quality on a test set

## Architecture

(User question)
    |
    v
[FastAPI /query endpoint]
    |
    v
[Embed question] -> [Qdrant vector search] -> top N chunks
    |
    v
[Build prompt with context + question]
    |
    v
[LLM via OpenRouter]
    |
    v
(Answer + citations)

## Tech stack

- **Python** — language
- **FastAPI** — HTTP API layer
- **Qdrant Cloud** — vector database (free tier)
- **OpenRouter** — LLM access (free models)
- **Pydantic** — validation and settings
- **Logging** — structured logs via Python's `logging` module

## Why Qdrant (and not pgvector)

- Dedicated vector database with strong filtering and hybrid search
- Free cloud tier with ~1M vectors at 768 dimensions
- Production-ready performance (used by real companies)
- Clean Python client and simple API
- Matches what real AI engineering job postings list

## Project structure
rag_project/
├── data/
│ └── documents/ # source PDFs and text files
├── ingestion/ # load, chunk, embed documents
├── retrieval/ # Qdrant search logic
├── generation/ # RAG prompt and LLM call
├── api/ # FastAPI endpoints
└── README.md # this file


## How to run

(will fill in as the project is built)

## Evaluation

(will fill in — accuracy on a 50-question test set)

## Known limitations

(will fill in as I discover them)

## Status

- [x] Day 6 — project skeleton and vector DB setup
- [ ] Day 7 — document ingestion and chunking
- [ ] Day 8 — embedding and Qdrant indexing
- [ ] Day 9 — retrieval
- [ ] Day 10 — generation with citations
- [ ] Day 11 — FastAPI endpoints
- [ ] Day 12 — evaluation set