# LLM Practice

My transition from backend engineering to AI engineering.

## Structure
- `hello_llm.py` — first raw API call (Day 1)
- `src/llm_client.py` — reusable client with retries, fallback models, error handling (Day 2)
- `test_client.py` — usage example

## What the client handles
- Rate limits with exponential backoff
- Timeouts
- API errors with automatic fallback to a different model
- Token usage tracking

## Why this matters
LLM APIs fail often. Production AI systems need retry logic and fallback models.
This client is the foundation for every AI project I will build.