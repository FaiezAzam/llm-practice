from src.llm_client2 import LLMClient

client = LLMClient()

result = client.chat(
    user_message = "what is difference between rest and grapL",
    system_message = "you are a backend mentor. answer in 2 sentences"
)


print(result)