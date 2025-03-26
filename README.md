# AI Voice Agent

## Overview
This project implements an AI-powered voice agent capable of handling multi-turn sales conversations. The agent uses the following technologies:
- **Vocode** for voice interaction
- **Twilio** for telephony integration
- **Hugging Face** for dialogue generation
- **Deepgram** for real-time transcription
- **ElevenLabs** for text-to-speech (TTS) synthesis

## Features
1. **Call Handling**: Receives incoming calls and initiates outbound calls using Twilio.
2. **Speech-to-Text Processing**: Uses Deepgram to transcribe user speech to text.
3. **Conversational AI**: Uses Hugging Face to generate contextually relevant responses.
4. **Text-to-Speech Synthesis**: Converts AI-generated text to speech using ElevenLabs.
5. **Conversation Logging**: Captures and stores the complete conversation with timestamps and call metadata.
6. **Sales-Oriented Dialogue Flow**: Engages customers with professional greetings, open-ended questions, and dynamic sales pitches.

## Architecture
The AI voice agent architecture consists of the following components:
1. **Flask Server**: Handles incoming Twilio calls and routes the requests to appropriate services.
2. **Deepgram**: Transcribes the caller's speech to text in real-time.
3. **Hugging Face**: Generates AI responses based on the transcribed text and conversation history.
4. **ElevenLabs**: Converts the AI-generated text to natural-sounding speech.
5. **Twilio**: Manages the telephony interactions, including receiving and initiating calls.
6. **Vocode**: Handles the voice interaction with the caller.

## APIs Used
1. **Twilio API**: For call handling and telephony integration.
2. **Deepgram API**: For real-time speech-to-text transcription.
3. **Hugging Face API**: For generating conversational AI responses.
4. **ElevenLabs API**: For text-to-speech synthesis.

## Setup Instructions

### Prerequisites
- Python 3.8 or higher
- Node.js and npm (for the React frontend)

### Step 1: Clone the Repository
```bash
git clone https://github.com/Divzdj/AI-Voice-Agent-Project.git
cd AI-Voice-Agent-Project
```

### Step 2: Create and Activate a Virtual Environment
For Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

For macOS/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Upgrade pip
```bash
python -m pip install --upgrade pip
```

### Step 4: Install Required Dependencies
```bash
pip install -r requirements.txt
```

### Step 5: Set Up Environment Variables
Create a `.env` file in the root directory and add the following environment variables:
```
TWILIO_ACCOUNT_SID=your_twilio_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
HUGGINGFACE_API_KEY=your_huggingface_key
DEEPGRAM_API_KEY=your_deepgram_key
ELEVENLABS_API_KEY=your_elevenlabs_key
```

### Step 6: Run the Flask Server
```bash
python app.py
```

### Step 7: Expose Your Local Server Using ngrok
```bash
ngrok http 5000
```
Copy the public URL provided by ngrok (e.g., `https://abcd1234.ngrok-free.app`) and update the Twilio webhook with this URL.

### Step 8: Install and Run the React Frontend
```bash
cd ai-voice-agent-dashboard
npm install
npm start
```

### Step 9: Access the Application
Open your browser and go to `http://localhost:5000` to access the dashboard.

### Usage
- Make calls using the provided Twilio number and interact with the AI voice agent.
- Monitor live conversations and view conversation logs on the dashboard.

## Deployment Instructions
1. **Deploy Flask Server**: You can deploy the Flask server on a cloud platform like AWS, Heroku, or DigitalOcean.
2. **Deploy React Frontend**: You can deploy the React frontend on platforms like Vercel, Netlify, or GitHub Pages.
3. **Update Environment Variables**: Ensure that environment variables are correctly set in the production environment.

## Evaluation Criteria
- **Functionality**: The AI agent's performance in multi-turn conversations.
- **Code Quality**: Structure and documentation of the code.

## Contact
For any questions, please contact divvyarosejoseph25@gmail.com