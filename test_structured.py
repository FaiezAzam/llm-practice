from src.structured import StructuredLLM


extractor = StructuredLLM()

schema = """
{
  "sentiment": "positive" | "negative" | "neutral",
  "confidence": number between 0 and 1,
  "key_phrases": list of strings
}
"""

result = extractor.extract(
    user_message="I'm not sure how I feel about the new API. It's fast but the docs are terrible and I spent 3 hours debugging CORS.",
    schema_description=schema,
)

if result["success"]:
    print("Parsed data:")
    print(result["data"])
    print("Tokens:", result["tokens"])
else:
    print("Failed:", result["error"])
    print("Raw output:", result.get("raw"))