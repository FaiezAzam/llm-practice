from src.llm_client import LLMClient

client = LLMClient()

result = client.chat(
    user_message="What is the difference between REST and GraphQL?",
    system_message="You are a backend engineering mentor. Answer in 3 sentences."
)

if result["success"]:
    print("Answer:", result["answer"])
    print("Model used:", result["model"])
    print("Tokens:", result["tokens"])
else:
    print("Failed:", result["error"])