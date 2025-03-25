import os
import requests
import time
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")

if not HUGGINGFACE_API_KEY:
    raise ValueError("Hugging Face API key not found. Set it in the .env file.")

# Hugging Face API URL for BlenderBot model
HF_MODEL = "facebook/blenderbot-400M-distill"
HF_API_URL = f"https://api-inference.huggingface.co/models/{HF_MODEL}"
HEADERS = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}

# Conversation history
conversation_history = [
    {"role": "system", "content": "You are an AI voice assistant helping users with general queries."}
]

def format_conversation(history):
    """Format the conversation history into a single string."""
    formatted_history = ""
    for message in history:
        role = message["role"]
        content = message["content"]
        formatted_history += f"{role}: {content}\n"
    return formatted_history.strip()

def chat_with_ai(user_input, max_retries=3, backoff_factor=2):
    """Generate AI response while maintaining conversation history."""
    conversation_history.append({"role": "user", "content": user_input})

    try:
        formatted_history = format_conversation(conversation_history)
        payload = {"inputs": formatted_history}
        retries = 0

        while retries < max_retries:
            response = requests.post(HF_API_URL, headers=HEADERS, json=payload)

            if response.status_code == 200:
                ai_response = response.json()
                if isinstance(ai_response, list) and len(ai_response) > 0 and 'generated_text' in ai_response[0]:
                    ai_text = ai_response[0]['generated_text']
                else:
                    ai_text = "Sorry, I couldn't generate a response."
                conversation_history.append({"role": "assistant", "content": ai_text})
                return ai_text
            else:
                print(f"❌ API Error: {response.text}")
                retries += 1
                wait_time = backoff_factor ** retries
                print(f"Retrying in {wait_time} seconds...")
                time.sleep(wait_time)

        return "❌ API Error: Maximum retry limit reached."

    except Exception as e:
        return f"❌ Error: {e}"

# Chat loop
if __name__ == "__main__":
    print("🗨️ AI Chatbot (Hugging Face) is ready! Type 'exit' to stop.")
    while True:
        user_message = input("You: ")
        if user_message.lower() == "exit":
            print("👋 Goodbye!")
            break

        response = chat_with_ai(user_message)
        print(f"AI: {response}")