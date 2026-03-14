# AIOmetre — Your Human Connection Companion
AI-Powered Human Connection Agent | Built by Eloisa Flores with Google Gemini + Imagen

Live Demo: https://aiometre-446670956067.us-central1.run.app

---

## Intellectual Property Notice
This project and all its constituent parts — including source code, architectural design, logic, and creative assets — are the exclusive intellectual property of Eloisa Flores. This repository is shared for evaluation purposes within the Gemini Live Agent Challenge. All rights reserved. Unauthorized copying, redistribution, or commercial use is strictly prohibited without explicit written consent from the author. Submission to the Gemini Live Agent Challenge grants Google and Devpost a non-exclusive license to evaluate and promote this project as described in the official hackathon rules.

---

## What It Does
AIOmetre is an AI companion designed to combat digital isolation by transforming screen time into meaningful human connection.

- 📱 **Digital Footprint Awareness:** Brings your screen habits into sharp focus — because most of us have no idea how many hours slip by without a single real human exchange. AIOmetre makes that invisible cost visible, and personal.
- 🎵 **Emotional Resonance:** Detects your current emotional state through iconic pop culture references — no therapy-speak, just honest self-reflection disguised as fun.
- 🧬 **Relational DNA:** Identifies your personality type and communication style through a quick interactive conversation, then pairs you with a fictional duo that mirrors who you are.
- 💜 **Active Reconnection:** Doesn't just suggest "be more social" — it tells you exactly who to reach out to, and why, right now.

AIOmetre gamifies the process: complete your Human Connection Missions, earn Golden Coins, and celebrate the moments that truly matter — off-screen.

---

## How It Works
```
User answers 2 quick questions
        ↓
Gemini 2.5 Flash builds your personality profile
        ↓
Pairs you with an iconic fictional duo
        ↓
Checks screen time + emotional vibe
        ↓
Matrix pill moment — Red or Blue?
        ↓
Imagen 4.0 generates a personalized image + iconic quote
        ↓
AIOmetre gives you a human connection mission
        ↓
User earns Golden Coins for completed missions
        ↓
Infinite mission loop — never runs out of reasons to connect
```

---

## Google Gemini Integration

| Service | Role |
|--------|------|
| Gemini 2.5 Flash | Conversation, personality profiling, story + quote generation |
| Imagen 4.0 Fast | Real-time personalized image generation |
| Web Speech API | Voice input and output |
| Google Cloud Run | Backend hosting |

---

## Why Gemini 2.5 Flash?
Gemini 2.5 Flash is one of Google's most capable and efficient models — and it shows. With its extended context window, it maintains full conversational memory across the entire user session, remembering personality answers, screen time data, emotional vibe, and chosen pairing without losing context. Its instruction-following precision allows AIOmetre to enforce complex behavioral rules — like never repeating a quote, always stopping after OPTIONS, and switching languages mid-conversation — with remarkable consistency. Its multimodal reasoning enables it to generate contextually relevant prompts for Imagen 4.0, creating images that feel genuinely personalized rather than generic. And its speed keeps the experience feeling live and responsive, not like a chatbot waiting to think.

---

## Features
- 🗣️ Voice narration — AIOmetre speaks every response out loud using Web Speech API
- 🎨 AI-generated images — personalized per user vibe using Imagen 4.0
- 💊 Matrix pill moment — Red or Blue, your choice
- 🐱 7 unique cat characters — animated reactions for key emotional moments
- 🏆 Golden Coin system — gamified human connection tracking
- 🔄 Infinite mission loop — always a new reason to reach out
- 🌍 Multilingual — mirrors the user's language automatically
- ⚡ Full session under 2 minutes

---

## Tech Stack
- **Backend:** Python + Flask
- **AI Conversation + Story:** Gemini 2.5 Flash via Google GenAI SDK
- **AI Image Generation:** Imagen 4.0 Fast via Google GenAI SDK
- **Voice:** Web Speech API (browser-native)
- **Hosting:** Google Cloud Run
- **Frontend:** Vanilla HTML/CSS/JavaScript

---

## Deploy to Cloud Run
```bash
gcloud run deploy aiometre \
  --source . \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars GEMINI_API_KEY=YOUR_KEY_HERE
```

## Run Locally
```bash
pip install -r requirements.txt
GEMINI_API_KEY=your_key python3 main.py
```

---

## Architecture
```
[User Browser]
     |
     | Voice + Text Input
     ↓
[Web Speech API] → [AIOmetre Frontend HTML/JS]
     |
     | HTTP POST /chat or /story
     ↓
[Flask Backend — Google Cloud Run]
     |
     ├── /chat → Gemini 2.5 Flash (conversation + profiling)
     └── /story → Gemini 2.5 Flash (quote + image prompt generation)
                → Imagen 4.0 Fast (image generation)
     |
     | JSON response (text + image + options)
     ↓
[Frontend renders text + image + speaks via Web Speech API]
```

---

## Use Cases
- Young adults struggling with screen addiction and social isolation
- Anyone who feels disconnected despite being always online
- People who want to reconnect with friends and family but don't know where to start
- Organizations and HR teams promoting mental wellness and real human connection
- Therapists and coaches looking for engaging tools to encourage social behavior

---

## Technical Challenges & Solutions

**1. Gemini response truncation** — Gemini would cut off mid-sentence with low token limits. Solved by progressively tuning max_output_tokens and restructuring prompts to prioritize completion over length.

**2. Image generation timeout** — Generating multiple images per session caused Cloud Run request timeouts. Solved by reducing to 1 image per mission and increasing Cloud Run timeout to 300 seconds via gcloud services update.

**3. Base64 image inflation** — Embedding cat images as base64 strings inflated the HTML file to 6MB, crashing browsers with JavaScript heap errors. Solved by serving all static images as PNG files through dedicated Flask routes, reducing HTML size by 95%.

**4. Web Speech API emoji pronunciation** — Emojis like 👀 and 😉 were being read aloud as "eyes" and "winking face". Solved by stripping emoji characters from the speech synthesis text client-side while keeping them visible in the chat UI.

**5. Duplicate JavaScript functions** — Iterative HTML edits introduced duplicate function declarations (sendMessageToAPI, loadStory) causing Uncaught SyntaxError in the browser. Solved by rewriting the entire HTML file from scratch with a clean, single-source architecture.

**6. Gemini ignoring system prompt rules** — Gemini occasionally ignored instructions like "never write the word PAIRING" or "stop after OPTIONS". Solved by restructuring the system prompt with explicit CRITICAL labels and reducing competing instructions that caused rule conflicts.

**7. Cloud Run cold start blank screen** — First load after inactivity showed a blank page for 2-3 seconds due to Cloud Run cold start. Mitigated by optimizing the Flask startup sequence and keeping the initial HTML response lightweight.

**8. JSON parsing failure for image prompts** — Gemini occasionally returned malformed JSON for story generation, breaking the image pipeline. Solved by switching from JSON to a simple line-based format (QUOTE: / IMAGE:) that is far more robust to parse.

**9. Session context loss on reconnect** — Cloud Shell disconnections during development would wipe /tmp storage, losing generated assets. Solved by moving all persistent assets (cat images) to the project directory and serving them as static files committed to the repository.

**10. Gemini repeating quotes across missions** — The same iconic quote would appear on multiple missions within a session. Solved by providing a curated list of 30+ distinct quotes directly in the prompt with explicit instructions to vary selection based on the user's emotional vibe.

---

## Category
**Creative Storyteller** — multimodal output: text + AI-generated images + voice narration, interleaved in a single fluid user experience.

Built for the **Gemini Live Agent Challenge** — March 2026
\#GeminiLiveAgentChallenge

Created by Eloisa Flores — because in a world full of screens, the most revolutionary act is a real human conversation. 💜
