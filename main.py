from flask import Flask, request, jsonify, Response
from flask_cors import CORS
from google import genai
from google.genai import types
import os
import re

app = Flask(__name__)
CORS(app)

API_KEY = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=API_KEY)

SYSTEM_PROMPT = """You are AIOmetre, a warm witty AI companion fighting digital loneliness. Talk like a cool best friend texting. Short. Real. Funny. Never robotic, never corporate, never therapy-voice.

LANGUAGE: Mirror the user. They switch, you switch.
NICKNAME: Use actual name if told. Otherwise say "friend". NEVER write literal [nickname].
CRITICAL: If you receive "skip intro and start questions directly with Q1" jump IMMEDIATELY to Q1. No greeting. No preamble.
CRITICAL: If user says "continue", "let's continue", "back", "I want to continue", or similar — skip ALL questions and say exactly: "Hold on! To unlock your mission, you need to hear this story first, deal?" Do NOT add OPTIONS.

STEP 1 - Q1: When you are with your closest friends, are you the listener, the leader, or the funny one?
OPTIONS: The listener | The leader | The funny one | A mix of all

STEP 2 - SCREEN TIME: Ask exactly: "Real talk — how many hours on screens today?"
OPTIONS: Less than 2h | 3-4h | 5-6h | 7+ hours
After answer, give ONE short reaction sentence. Then set SCORE:
Less than 2h: SCORE:2 | 3-4h: SCORE:5 | 5-6h: SCORE:7 | 7+h: SCORE:9

STEP 3 - PAIRING: Pick ONE pairing based on Q1 answer. AIOmetre = companion. User = protagonist. MAX 2 short sentences. STOP. Ask: Does this resonate?
OPTIONS: Yes, I love it! | Tell me more | Suggest another
CRITICAL: Output NOTHING after OPTIONS. Wait for user.
CRITICAL: Once confirmed — NEVER repeat. Move to STEP 4.
CRITICAL: Tell me more or Suggest another — ONE different pairing, 2 sentences max.

PAIRINGS: Frodo & Sam | Gandalf & Bilbo | Joey & Chandler | Monica & Rachel | Lorelai & Rory | Turk & JD | Thelma & Louise | Sherlock & Watson | Luke & Yoda | Daniel & Mr. Miyagi | Harry & Dumbledore | Neo & Morpheus | Don Quijote & Sancho | Elphaba & Glinda | Willow & Tara | Crowley & Aziraphale | Korra & Asami | Adora & Catra | Eric & Otis | Nick & Tao | Magnus & Alec | Blanca & Elektra | David & Stevie

STEP 4 - VIBE CHECK: Ask exactly: "One last thing — which song feels more like you lately?"
OPTIONS: Unstoppable by Sia 🔥 | Numb by U2 🌫️ | Hurt by Johnny Cash 🪨
After answer, give ONE warm sentence reaction. Then say exactly: "Want me to take you out of the matrix? Ha, I am joking! Am I though?"
Do NOT add OPTIONS — frontend handles pill buttons.

STEP 5 - PILLS:
If RED PILL: say "Congrats, you are a real NEO!" then say exactly: "Hold on! To unlock your mission, you need to hear this story first, deal?"
If BLUE PILL: say "Sorry buddy, the journey is not over yet... and I know you are gonna love this." then say exactly: "Hold on! To unlock your mission, you need to hear this story first, deal?"
Do NOT add OPTIONS after story line — frontend handles button.

STEP 6 - GOLDEN COINS after story:
Say: "Now your real mission: share what you just discovered about yourself with 2 real humans. Each one = a Golden Coin."
OPTIONS: I did it! First coin 💜 | Not ready yet

If first coin: celebrate in 1 sentence. STOP. Then:
OPTIONS: I did it! Second coin 💜 | Need more time
CRITICAL: Output NOTHING after OPTIONS.

If second coin: say exactly "YOU DID IT! You are officially the most connected human I know today!" then say "Ready for your next mission?"
OPTIONS: Hell yes 🔥 | Give me a sec | Hasta la vista, Baby!

STEP 7 - INFINITE LOOP after Hell yes:
Say exactly: "Hold on! To unlock your mission, you need to hear this story first, deal?"
Do NOT add OPTIONS — frontend handles button.

If Give me a sec: say "Fair enough! Come back whenever. I will be here."
OPTIONS: Hell yes 🔥 | Hasta la vista, Baby!

If Hasta la vista Baby: say "Hasta la vista, Baby!" + ONE funny callback. SCORE:0

GOODBYE: Only say "Hasta la vista, Baby!" when user picks that option.
Always end every response with SCORE:X"""

chat_sessions = {}

@app.route('/')
def index():
    with open('AIOMetre.html', 'r') as f:
        return Response(f.read(), mimetype='text/html')

@app.route('/fondo.png')
def fondo():
    return open('fondo.png', 'rb').read(), 200, {'Content-Type': 'image/png'}

@app.route('/eloisa_flores_foto.png')
def foto():
    return open('eloisa_flores_foto.png', 'rb').read(), 200, {'Content-Type': 'image/png'}

@app.route('/chat', methods=['POST'])
def chat_endpoint():
    data = request.json
    user_message = data.get('message', '')
    session_id = data.get('session_id', 'default')
    if session_id not in chat_sessions:
        chat_sessions[session_id] = []
    chat_sessions[session_id].append({"role": "user", "parts": [{"text": user_message}]})
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=chat_sessions[session_id],
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                max_output_tokens=450
            )
        )
        full_text = response.text if response.text else "I got a little lost there — say that again? 😄"
        chat_sessions[session_id].append({"role": "model", "parts": [{"text": full_text}]})
        score = 5
        score_match = re.search(r'SCORE:(\d+)', full_text)
        if score_match:
            score = int(score_match.group(1))
        clean_text = re.sub(r'\nSCORE:\d+', '', full_text).strip()
        clean_text = re.sub(r'SCORE:\d+', '', clean_text).strip()
        clean_text = re.sub(r'[\U0001F300-\U0001FFFE\U00002700-\U000027BF\U0001F900-\U0001F9FF\U00002600-\U000026FF]', '', clean_text).strip()
        options = []
        options_match = re.search(r'OPTIONS:\s*(.+?)(?:\n|$)', clean_text)
        if options_match:
            options = [o.strip() for o in options_match.group(1).split('|')]
            clean_text = re.sub(r'\nOPTIONS:.+', '', clean_text).strip()
            clean_text = re.sub(r'OPTIONS:.+', '', clean_text).strip()
        return jsonify({'reply': clean_text, 'score': score, 'options': options})
    except Exception as e:
        return jsonify({'reply': f'Error: {str(e)}', 'score': 5, 'options': []})

STORY_PROMPTS = [
    "Send this to that person who had your back when everything was falling apart.",
    "Share this with someone who taught you something good about yourself.",
    "Think of that person who always makes you laugh without trying — send it to them.",
    "Who was there for you during a tough time without asking anything in return? That is your person today.",
    "Send this to someone you think about more than you admit.",
    "That friend who knows your worst day and never judged you — this one is for them.",
    "Someone out there misses you right now. Send this and find out who.",
    "Think of that person who believed in you before you believed in yourself.",
    "Who would you call at 3am if you really needed to? Send them this first.",
    "That family member you keep meaning to check on — today is the day."
]

import random
import base64


@app.route('/story', methods=['POST'])
def story_endpoint():
    data = request.json
    session_id = data.get('session_id', 'default')
    vibe = data.get('vibe', 'searching')
    pairing = data.get('pairing', 'two companions')
    try:
        import json
        story_prompt = f"""Create a short story for someone who feels {vibe} and relates to {pairing}.
Respond with ONLY these two lines, nothing else:
STORY: [2-3 warm human sentences: a conflict, a resolution, and a moral]
IMAGE: [detailed scene for one illustration, anime european style, warm amber tones, two people connecting]"""
        story_response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[{"role": "user", "parts": [{"text": story_prompt}]}],
            config=types.GenerateContentConfig(max_output_tokens=400)
        )
        raw = story_response.text.strip()
        story_line = ""
        image_line = ""
        for line in raw.split("\n"):
            if line.startswith("STORY:"):
                story_line = line[6:].strip()
            elif line.startswith("IMAGE:"):
                image_line = line[6:].strip()
        if not story_line:
            story_line = "Sometimes the best connections happen when we least expect them."
        if not image_line:
            image_line = "two friends reuniting after a long time, warm embrace, golden light"
        story = {"story_text": story_line, "image_prompt": image_line}
        img_prompt = story['image_prompt'] + ", anime european style illustration, warm golden amber colors, soft shadows, clean lines, emotional, cinematic, no text, no watermark"
        img_response = client.models.generate_images(
            model="imagen-4.0-fast-generate-001",
            prompt=img_prompt,
            config={"number_of_images": 1, "aspect_ratio": "1:1"}
        )
        img_data = img_response.generated_images[0].image.image_bytes
        img_b64 = base64.b64encode(img_data).decode('utf-8')
        share_prompt = random.choice(STORY_PROMPTS)
        return jsonify({'story': story['story_text'], 'image': img_b64, 'share_prompt': share_prompt})
    except Exception as e:
        return jsonify({'error': str(e), 'story': '', 'image': '', 'share_prompt': ''})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
