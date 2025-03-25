import os
import asyncio
from dotenv import load_dotenv
from deepgram import Deepgram

# Load environment variables
load_dotenv()

# Get API Key from environment variables
DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")
print(f"Loaded API Key: {DEEPGRAM_API_KEY}")

# Ensure API Key is set
if not DEEPGRAM_API_KEY:
    raise ValueError("Deepgram API key not found. Please set it in the .env file.")

# Path to the audio file
AUDIO_FILE_PATH = "sample.wav"  # Ensure this file exists

async def transcribe_audio():
    """Transcribes audio using Deepgram API v3."""
    try:
        # Correct initialization of Deepgram Client
        deepgram = Deepgram(DEEPGRAM_API_KEY)

        # Read the audio file
        with open(AUDIO_FILE_PATH, "rb") as audio_file:
            audio_bytes = audio_file.read()

        # Use the new method for transcription
        response = await deepgram.transcription.prerecorded(
            source={"buffer": audio_bytes, "mimetype": "audio/wav"},
            options={"model": "nova"}  # Correct syntax, no 'PrerecordedOptions'
        )

        # Extract transcription text
        transcript = response["results"]["channels"][0]["alternatives"][0]["transcript"]
        print("\n📝 Transcription: ", transcript)

    except Exception as e:
        print(f"\n❌ Error: {e}")

# Run the async function
if __name__ == "__main__":
    asyncio.run(transcribe_audio())