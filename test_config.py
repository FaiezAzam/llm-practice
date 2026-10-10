from src.config import settings

print("API key present",bool(settings.openrouter_api_key))
print("Default model:", settings.default_model)
print("Max retries:", settings.max_retries)
print("Fallback models:", settings.fallback_models)
