import os
import time
from typing import Optional
from dotenv import load_dotenv
from openai import OpenAI, APIError, APITimeoutError, RateLimitError

load_dotenv()


class LLMClient:
    """A production-style client for calling LLMs via OpenRouter."""

    # Fallback models — tried in order if the primary fails
    FALLBACK_MODELS = [
        "openrouter/free",
        "nvidia/nemotron-3.5-lightning:free",
        "google/gemma-4-26b-a4b-it:free",
    ]

    def __init__(self, model: Optional[str] = None):
        api_key = os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            raise ValueError("OPENROUTER_API_KEY is missing from .env")

        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
        )
        self.model = model or self.FALLBACK_MODELS[0]

    def chat(
        self,
        user_message: str,
        system_message: str = "You are a helpful assistant.",
        max_retries: int = 3,
        retry_delay: float = 2.0,
    ) -> dict:
        """
        Send a chat request with retries and fallback models.
        Returns a dict with the answer, model used, and token usage.
        """
        last_error = None

        for attempt in range(max_retries):
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": system_message},
                        {"role": "user", "content": user_message},
                    ],
                    timeout=30,
                )

                return {
                    "answer": response.choices[0].message.content,
                    "model": response.model,
                    "tokens": response.usage.total_tokens,
                    "success": True,
                }

            except RateLimitError as e:
                last_error = e
                print(f"[Attempt {attempt + 1}] Rate limited. Waiting {retry_delay}s...")
                time.sleep(retry_delay)
                retry_delay *= 2  # exponential backoff

            except APITimeoutError as e:
                last_error = e
                print(f"[Attempt {attempt + 1}] Timeout. Retrying...")
                time.sleep(retry_delay)

            except APIError as e:
                last_error = e
                print(f"[Attempt {attempt + 1}] API error: {e}")

                # Try the next fallback model
                if attempt < len(self.FALLBACK_MODELS) - 1:
                    self.model = self.FALLBACK_MODELS[attempt + 1]
                    print(f"Switching to fallback model: {self.model}")
                else:
                    break

        return {
            "answer": None,
            "model": self.model,
            "tokens": 0,
            "success": False,
            "error": str(last_error),
        }