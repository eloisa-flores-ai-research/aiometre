# AIOmetre 🍂
### Your Human Connection Companion

People expose their lives on social media but at the end of the day most of them feel alone, because they never really had a human-to-human experience. So I thought — what if technology could help them realize when they've spent too much time in the digital world? I created AIOmetre: not a nagging mom, but a caring friend and advisor that helps you fight loneliness and screen overuse, gently pushing you back into the real world.

AIOmetre is a Live Agent built with Gemini's voice capabilities. The AI companion talks to you (or stays quiet if you prefer), gets to know your personality, and gives you fun "human connection missions" to complete.

## Features
- 4 personality questions to assign you a fictional character companion
- Real-time CONNECTION INDEX that tracks your screen time and loneliness score
- Human connection missions — achievable in 5 minutes
- Voice input and output (can be disabled)
- Supports any language — mirrors the user automatically

## Tech Stack
- **Gemini 2.5 Flash** — conversational AI
- **Google Cloud Run** — backend hosting
- **Flask** — Python backend
- **Web Speech API** — voice input/output
- **HTML/CSS/JS** — frontend

## Live Demo
https://aiometre-446670956067.us-central1.run.app

## How to Run Locally
```bash
git clone https://github.com/eloisa-flores-ai-research/aiometre.git
cd aiometre
pip install -r requirements.txt
export GEMINI_API_KEY=your_key_here
python main.py
```

## Deploy to Cloud Run
```bash
gcloud run deploy aiometre --source . --region us-central1 --allow-unauthenticated --set-env-vars GEMINI_API_KEY=your_key_here
```

## Architecture
User speaks or types → Flask backend → Gemini 2.5 Flash → CONNECTION INDEX score extracted → Response read aloud via Web Speech API → Human connection mission proposed when score is high

## Created by
Eloisa Flores — Gemini Live Agent Challenge 2026
#GeminiLiveAgentChallenge
