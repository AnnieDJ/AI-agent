from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.inference.models import SystemMessage, UserMessage, AssistantMessage
import os

# Load .env config
load_dotenv()
project_connection = os.getenv("AZURE_PROJECT_CONNECTION")
model_deployment = os.getenv("AZURE_MODEL_DEPLOYMENT")

# Initialize the project client
projectClient = AIProjectClient.from_connection_string(
    conn_str=project_connection,
    credential=DefaultAzureCredential()
)

# Get a chat client
chat = projectClient.inference.get_chat_completions_client()

# Initialize prompt with system message
prompt = [
    SystemMessage("You are a helpful AI assistant that answers questions.")
]

# Start chat loop
print("👋 Chat started. Type 'quit' to exit.")
while True:
    input_text = input("You: ")
    if input_text.lower() == "quit":
        break

    # Get a chat completion
    prompt.append(UserMessage(input_text))
    response = chat.complete(
        model=model_deployment,
        messages=prompt
    )
    completion = response.choices[0].message.content
    print("AI:", completion)
    prompt.append(AssistantMessage(completion))
