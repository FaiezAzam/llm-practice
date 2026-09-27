import os
from dotenv import load_dotenv
from openai import OpenAI

# Load the API key from the .env file
load_dotenv()

# Create the client pointing to OpenRouter
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

# Send a message to the LLM
response = client.chat.completions.create(
    model="openrouter/free",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Explain what an API is in one sentence."}
    ]
)

# Print the answer
print(response.choices[0].message.content)

# Print token usage
print(f"Tokens used: {response.usage.total_tokens}")