import json
from typing import Any
from src.llm_client import LLMClient


class StructuredLLM:
    """Wraps LLMClient to return validated JSON instead of text."""

    def __init__(self):
        self.client = LLMClient()

    def extract(
        self,
        user_message: str,
        schema_description: str,
        system_message: str = "You extract structured data. Reply with JSON only.",
    ) -> dict[str, Any]:
        """
        Ask the LLM for JSON matching the schema_description.
        Retries once with a stricter prompt if JSON parsing fails.
        """
        prompt = (
            f"{user_message}\n\n"
            f"Return ONLY valid JSON matching this schema:\n{schema_description}\n"
            f"Do not include any explanation, markdown, or code fences."
        )

        result = self._call_and_parse(prompt, system_message)

        if not result["success"]:
            # Retry once with a stricter instruction
            strict_prompt = (
                f"Your previous reply was not valid JSON. Try again.\n\n"
                f"{prompt}\n\n"
                f"Output must start with {{ and end with }}. Nothing else."
            )
            result = self._call_and_parse(strict_prompt, system_message)

        return result

    def _call_and_parse(self, prompt: str, system_message: str) -> dict[str, Any]:
        response = self.client.chat(
            user_message=prompt,
            system_message=system_message,
        )

        if not response["success"]:
            return {
                "success": False,
                "error": response.get("error", "LLM call failed"),
                "data": None,
            }

        raw = response["answer"].strip()

        # Remove markdown code fences if the LLM added them anyway
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
            raw = raw.strip()

        try:
            data = json.loads(raw)
            return {
                "success": True,
                "data": data,
                "tokens": response["tokens"],
                "raw": raw,
            }
        except json.JSONDecodeError as e:
            return {
                "success": False,
                "error": f"Invalid JSON: {e}",
                "raw": raw,
                "data": None,
            }