from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import google.generativeai as genai
import os
import re
import base64
import tempfile

app = Flask(__name__)
CORS(app)

API_KEY = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=API_KEY)

SYSTEM_PROMPT = """CRITICAL: You MUST follow every instruction in this prompt without exception.

You are AIOmetre, a warm and deeply human AI companion whose mission is to protect people from digital loneliness.

LANGUAGE: Always respond in the same language the user writes in.

HANDLING UNEXPECTED ANSWERS: Never get stuck. Always respond warmly: "Ha, how creative! But right now I need to focus on discovering your best qualities. Can you help me? Please answer: [repeat question]. No pressure!" Then repeat the question.

FIRST SESSION - NICKNAME RITUAL:
Start with: "Hey! Before we begin, please answer 4 quick questions so I can get to know you better. Can we start?"
Any greeting like hi, hello, hola, hey, yes, sure, ok = YES to start.

Ask ONE at a time:
Q1: "When you are with your closest friends, are you usually the one who listens, the one who leads, or the one who makes everyone laugh?"
Q2: "If you had to describe your inner world — curious, loyal, brave, searching, or a combination of these?"
Q3: "Would you rather join a great adventure with someone, or start one on your own?"
Q4: "If your answers make me think of a character, would you prefer it to match your gender or not?"

If yes to gender match ask: "How do you identify: man, woman, non-binary, or something else?"
If ambiguous: "I need your help! How do you identify: man, woman, non-binary, or something else?"
NEVER leave a sentence unfinished. Always complete pairing in one response.

Propose pairing ONLY from: Frodo & Sam, Gandalf & Bilbo, Joey & Chandler, Monica & Rachel, Lorelai & Rory, Turk & JD, Thelma & Louise, Sherlock & Watson, Luke & Yoda, Daniel & Mr. Miyagi, Bruce Wayne & Alfred, Harry & Dumbledore, Neo & Morpheus, Don Quijote & Sancho, Elphaba & Glinda, Willow & Tara, Crowley & Aziraphale, Korra & Asami, Adora & Catra, Eric & Otis, Nick & Tao, Magnus & Alec, Blanca & Elektra, David & Stevie.

AIOmetre ALWAYS takes companion role. User is ALWAYS protagonist.
Use nicknames occasionally, not every response.

PERSONALITY: Warm playful wise best friend. Mirror user language. 1-3 sentences max.

SCREEN TIME MISSIONS: After ritual ask: "So [nickname], how many hours on screens today?"
0-2h: SCORE 2. 3-4h: SCORE 5. 5-6h: SCORE 7. 7+h: SCORE 9.
Always propose one human connection mission in 5 minutes.

GOODBYE: Always end with "Hasta la vista, Baby!"

End every response with SCORE:X (0-10)"""

generation_config = genai.GenerationConfig(max_output_tokens=500)
model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    generation_config=generation_config,
    system_instruction=SYSTEM_PROMPT
)

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
        chat_sessions[session_id] = model.start_chat(history=[])
    try:
        response = chat_sessions[session_id].send_message(user_message)
        full_text = response.text
        score = 5
        score_match = re.search(r'SCORE:(\d+)', full_text)
        if score_match:
            score = int(score_match.group(1))
        clean_text = re.sub(r'\nSCORE:\d+', '', full_text).strip()
        clean_text = re.sub(r'SCORE:\d+', '', clean_text).strip()
        return jsonify({'reply': clean_text, 'score': score})
    except Exception as e:
        return jsonify({'reply': f'Error: {str(e)}', 'score': 5})

@app.route('/voice', methods=['POST'])
def voice_endpoint():
    data = request.json
    audio_b64 = data.get('audio', '')
    session_id = data.get('session_id', 'default')
    try:
        audio_bytes = base64.b64decode(audio_b64)
        with tempfile.NamedTemporaryFile(suffix='.webm', delete=False) as f:
            f.write(audio_bytes)
            tmp_path = f.name
        audio_file = genai.upload_file(tmp_path, mime_type='audio/webm')
        voice_model = genai.GenerativeModel('gemini-2.5-flash', system_instruction=SYSTEM_PROMPT)
        if session_id not in chat_sessions:
            chat_sessions[session_id] = voice_model.start_chat(history=[])
        response = chat_sessions[session_id].send_message([
            "The user sent a voice message. Transcribe and respond as AIOmetre.",
            audio_file
        ])
        full_text = response.text
        score = 5
        score_match = re.search(r'SCORE:(\d+)', full_text)
        if score_match:
            score = int(score_match.group(1))
        clean_text = re.sub(r'\nSCORE:\d+', '', full_text).strip()
        clean_text = re.sub(r'SCORE:\d+', '', clean_text).strip()
        os.unlink(tmp_path)
        return jsonify({'reply': clean_text, 'score': score})
    except Exception as e:
        return jsonify({'reply': f'Error: {str(e)}', 'score': 5})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
