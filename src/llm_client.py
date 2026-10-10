import logging

import time
from typing import Optional
from openai import OpenAI, APIError, APITimeoutError, RateLimitError
from src.config import settings

logger = logging.getLogger(__name__)


class LLMClient:
    """A production-style client for calling LLMs via OpenRouter."""

    def __init__(self, model: Optional[str] = None):

        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=settings.openrouter_api_key,
        )
        self.fallback_models = settings.fallback_models.split(",")
        self.model = model or settings.default_model
        self.max_retries = settings.max_retries
        self.retry_delay = settings.retry_delay

    def chat(
        self,
        user_message: str,
        system_message: str = "You are a helpful assistant.",
        max_retries: Optional[int] = None,
        retry_delay: Optional[float] = None,
    ) -> dict:
        """
        Send a chat request with retries and fallback models.
        Returns a dict with the answer, model used, and token usage.
        """

        if max_retries is None:
            max_retries = self.max_retries
        if retry_delay is None:
            retry_delay = self.retry_delay


        last_error = None

        for attempt in range(max_retries):
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": system_message},
                        {"role": "user", "content": user_message},
                    ],
                    timeout=settings.request_timeout,
                )

                return {
                    "answer": response.choices[0].message.content,
                    "model": response.model,
                    "tokens": response.usage.total_tokens,
                    "success": True,
                }

            except RateLimitError as e:
                last_error = e
                logger.warning(f"[Attempt {attempt + 1}] Rate limited. Waiting {retry_delay}s...")
                time.sleep(retry_delay)
                retry_delay *= 2  # exponential backoff

            except APITimeoutError as e:
                last_error = e
                logger.warning(f"[Attempt {attempt + 1}] Timeout. Retrying...")
                time.sleep(retry_delay)

            except APIError as e:
                last_error = e
                logger.error(f"[Attempt {attempt + 1}] API error: {e}")

                # Try the next fallback model
                if attempt < len(self.fallback_models) - 1:
                    self.model = self.fallback_models[attempt + 1]
                    logger.info(f"Switching to fallback model: {self.model}")
                else:
                    break

        return {
            "answer": None,
            "model": self.model,
            "tokens": 0,
            "success": False,
            "error": str(last_error),
        }