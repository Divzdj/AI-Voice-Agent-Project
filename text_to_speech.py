import requests
import os
from dotenv import load_dotenv

# Load API Key from .env
load_dotenv(dotenv_path="D:/DataScience/Assignment/ai_voice_agent/AI_Voice_Agent/.env")
# Print all environment variables to debug
print("Environment Variables:", os.environ)

# Fetch the API key from the environment
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
print(f"Using API Key: {ELEVENLABS_API_KEY}")

if not ELEVENLABS_API_KEY:
    raise ValueError("❌ ERROR: ElevenLabs API key is missing!")

# Use the Voice ID you obtained from ElevenLabs
VOICE_ID = "9BWtsMINqrJLrRacOk9x"  # This is your actual Voice ID

# Correct API URL for ElevenLabs
API_URL = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"

def text_to_speech(text):
    headers = {
        "xi-api-key": ELEVENLABS_API_KEY,  # Correct header for ElevenLabs API
        "Content-Type": "application/json"
    }

    # Prepare the request body with the text
    data = {
        "text": text,
        "voice_settings": {
            "voice": VOICE_ID,
            "format": "mp3"
        }
    }

    # Send the request to ElevenLabs API
    response = requests.post(API_URL, json=data, headers=headers)

    if response.status_code == 200:
        # Save the generated speech to output.mp3
        with open("output.mp3", "wb") as audio_file:
            audio_file.write(response.content)
        print("✅ Speech generated and saved as output.mp3")
    else:
        print(f"❌ Error: {response.status_code}, {response.text}")

# Example usage: Convert a sample text to speech
text_to_speech("Hello, this is a test of the ElevenLabs Text-to-Speech API!")