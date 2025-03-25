import os
import json
import datetime
import asyncio
import cProfile
import pstats
from dotenv import load_dotenv
from flask import Flask, request, jsonify, send_from_directory
from twilio.twiml.voice_response import VoiceResponse
from aiohttp import ClientSession
import logging
import openai
from deepgram import Deepgram
import vocode

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__, static_folder='./frontend/build', static_url_path='/')

# Load environment variables from .env file
load_dotenv()

# Initialize APIs
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
DEEPGRAM_API_KEY = os.getenv('DEEPGRAM_API_KEY')
HUGGINGFACE_API_KEY = os.getenv('HUGGINGFACE_API_KEY')
ELEVENLABS_API_KEY = os.getenv('ELEVENLABS_API_KEY')

huggingface_api_key = HUGGINGFACE_API_KEY
elevenlabs_api_key = ELEVENLABS_API_KEY

# Initialize Deepgram
deepgram = Deepgram(DEEPGRAM_API_KEY)

# In-memory conversation log
conversation_log = []

# Hugging Face API details
HF_MODEL = "facebook/blenderbot-400M-distill"
HF_API_URL = f"https://api-inference.huggingface.co/models/{HF_MODEL}"
HEADERS = {"Authorization": f"Bearer {huggingface_api_key}"}

# Initialize ClientSession within async function
session = None

async def init_session():
    global session
    session = ClientSession()
    logger.info("ClientSession initialized")

async def close_session():
    await session.close()
    logger.info("ClientSession closed")

async def format_conversation(history):
    """Format the conversation history into a single string."""
    formatted_history = ""
    for message in history:
        role = message["role"]
        content = message["content"]
        formatted_history += f"{role}: {content}\n"
    return formatted_history.strip()

async def chat_with_ai(user_input, max_retries=3, backoff_factor=1.5):
    """Generate AI response while maintaining conversation history."""
    formatted_history = await format_conversation(conversation_log)
    payload = {"inputs": formatted_history}
    retries = 0

    while retries < max_retries:
        async with session.post(HF_API_URL, headers=HEADERS, json=payload) as response:
            if response.status == 200:
                try:
                    ai_response = await response.json()
                    if isinstance(ai_response, dict) and 'generated_text' in ai_response:
                        ai_text = ai_response['generated_text']
                    elif isinstance(ai_response, list) and len(ai_response) > 0 and 'generated_text' in ai_response[0]:
                        ai_text = ai_response[0]['generated_text']
                    else:
                        ai_text = "Thank you for your interest in our products! How can I assist you further?"

                    return ai_text
                except json.JSONDecodeError:
                    logger.error("Error: Could not parse JSON response from Hugging Face.")
                    return "Thank you for your interest in our products! How can I assist you further?"

        logger.error(f"❌ API Error: {response.status} - {await response.text()}")
        retries += 1
        wait_time = backoff_factor ** retries
        logger.info(f"Retrying in {wait_time} seconds...")
        await asyncio.sleep(wait_time)  # Use asynchronous sleep

    return "❌ API Error: Maximum retry limit reached."

async def text_to_speech(text):
    """Convert text to speech using ElevenLabs."""
    headers = {
        "xi-api-key": elevenlabs_api_key,
        "Content-Type": "application/json"
    }
    data = {
        "text": text,
        "voice_settings": {
            "voice": "9BWtsMINqrJLrRacOk9x",  # Replace with a valid voice ID
            "format": "mp3"
        }
    }
    async with session.post(f"https://api.elevenlabs.io/v1/text-to-speech/{data['voice_settings']['voice']}",
                            json=data, headers=headers) as response:
        if response.status == 200:
            response_json = await response.json()
            return response_json.get('audio_url', 'http://example.com/ai_response_audio.mp3')
    return 'http://example.com/ai_response_audio.mp3'

@app.route("/voice", methods=['POST'])
async def voice():
    """Endpoint to start a voice call interaction."""
    response = VoiceResponse()
    response.say("Hello, please start speaking after the beep.", voice='alice', language='en-US')
    response.record(timeout=5, transcribe=True, transcribe_callback="/transcription")
    return str(response)

@app.route("/transcription", methods=['POST'])
async def transcription_endpoint():
    """Handles transcription results from Twilio."""
    try:
        transcription_text = request.form.get('TranscriptionText', '')
        timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
        call_sid = request.form.get('CallSid', 'UNKNOWN')
        caller_number = request.form.get('From', 'UNKNOWN')

        # Log user input
        user_log_entry = {
            "timestamp": timestamp,
            "call_sid": call_sid,
            "caller_number": caller_number,
            "user_input": transcription_text.strip('"'),
            "role": "user",
            "content": transcription_text.strip('"')
        }
        conversation_log.append(user_log_entry)

        # Run tasks concurrently
        ai_response, audio_url = await asyncio.gather(
            chat_with_ai(transcription_text),
            text_to_speech(transcription_text)
        )

        # Log AI response
        ai_log_entry = {
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "call_sid": call_sid,
            "caller_number": caller_number,
            "ai_response": ai_response.strip(),
            "audio_url": audio_url,
            "role": "assistant",
            "content": ai_response.strip()
        }
        conversation_log.append(ai_log_entry)

        # Save conversation log
        try:
            with open("conversation_log.json", "w") as log_file:
                json.dump(conversation_log, log_file, indent=4)
        except Exception as e:
            logger.error(f"Error writing to conversation_log.json: {e}")

        # Play AI response
        response = VoiceResponse()
        if audio_url:
            response.play(audio_url)
        else:
            response.say("Sorry, something went wrong and I could not generate the audio.")

        return str(response)

    except Exception as e:
        logger.error(f"Error in transcription processing: {e}")
        return jsonify({"error": "Error processing transcription."}), 500

@app.route("/conversation-log", methods=['GET'])
async def get_conversation_log():
    """Retrieve the stored conversation log."""
    try:
        with open("conversation_log.json", "r") as log_file:
            data = json.load(log_file)
        return jsonify(data)
    except Exception as e:
        logger.error(f"Could not load conversation log: {e}")
        return jsonify({"error": f"Could not load conversation log: {e}"}), 500

# Serve React App
@app.route('/')
@app.route('/<path:path>')
def serve_react_app(path=None):
    return send_from_directory(app.static_folder, 'index.html')

async def main():
    await init_session()
    try:
        app.run(debug=True, use_reloader=False)  # Disable reloader for performance
    finally:
        await close_session()

if __name__ == "__main__":
    logger.info("Starting the Flask app...")
    cProfile.run('asyncio.run(main())', filename='profile_output.prof')
    p = pstats.Stats('profile_output.prof')
    p.sort_stats('cumulative').print_stats(10)