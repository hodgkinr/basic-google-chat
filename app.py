import sqlite3
import json
import os
import uuid
from flask import Flask, render_template, request, Response, stream_with_context, jsonify
from google import genai
from google.genai import types

app = Flask(__name__)

# Configure Gemini Client
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

# Define Model Limits
MODEL_LIMITS = {
    "gemini-2.5-flash-lite": 1000000,
    "gemini-2.0-flash": 1000000,
    "default": 128000
}

def get_system_instruction():
    try:
        with open('system_prompt.txt', 'r') as f:
            return f.read()
    except FileNotFoundError:
        return "You are a helpful assistant."

def init_db():
    conn = sqlite3.connect('chat_history.db')
    c = conn.cursor()
    # Added session_id column
    c.execute('''CREATE TABLE IF NOT EXISTS messages 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  role TEXT, 
                  content TEXT, 
                  session_id TEXT)''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/history')
def history_page():
    return render_template('history.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get("message")
    session_id = data.get("session_id")
    model_id = "gemini-2.5-flash-lite"
    
    # 1. Pull ONLY this session's history for context and counting
    conn = sqlite3.connect('chat_history.db')
    c = conn.cursor()
    c.execute("SELECT role, content FROM messages WHERE session_id = ?", (session_id,))
    past_messages = c.fetchall()
    
    # Save current user message
    c.execute("INSERT INTO messages (role, content, session_id) VALUES (?, ?, ?)", 
              ("user", user_message, session_id))
    conn.commit()
    conn.close()

    # 2. Prepare context for token counting and Gemini
    history_for_gemini = []
    for role, content in past_messages:
        history_for_gemini.append({"role": "user" if role == "user" else "model", "parts": [{"text": content}]})
    
    # Current message
    current_contents = history_for_gemini + [{"role": "user", "parts": [{"text": user_message}]}]

    # 3. Count Tokens
    limit = MODEL_LIMITS.get(model_id, MODEL_LIMITS["default"])
    token_response = client.models.count_tokens(model=model_id, contents=current_contents)
    total_tokens = token_response.total_tokens
    usage_percent = round((total_tokens / limit) * 100, 4)

    def generate():
        # First packet: send the usage metadata
        yield f"data: {json.dumps({'usage': usage_percent, 'count': total_tokens, 'limit': limit})}\n\n"
        
        full_response = []
        stream = client.models.generate_content_stream(
            model=model_id,
            contents=current_contents,
            config=types.GenerateContentConfig(
                system_instruction=get_system_instruction(),
                temperature=0.7,
                safety_settings=[
                    types.SafetySetting(category="HARM_CATEGORY_HATE_SPEECH", threshold="BLOCK_LOW_AND_ABOVE"),
                    types.SafetySetting(category="HARM_CATEGORY_HARASSMENT", threshold="BLOCK_LOW_AND_ABOVE"),
                    types.SafetySetting(category="HARM_CATEGORY_SEXUALLY_EXPLICIT", threshold="BLOCK_LOW_AND_ABOVE"),
                    types.SafetySetting(category="HARM_CATEGORY_DANGEROUS_CONTENT", threshold="BLOCK_LOW_AND_ABOVE"),
                ]
            )
        )
        
        for chunk in stream:
            if chunk.text:
                full_response.append(chunk.text)
                yield f"data: {json.dumps({'text': chunk.text})}\n\n"
        
        # Save Bot Response to DB
        final_text = "".join(full_response)
        save_conn = sqlite3.connect('chat_history.db')
        save_c = save_conn.cursor()
        save_c.execute("INSERT INTO messages (role, content, session_id) VALUES (?, ?, ?)", 
                       ("bot", final_text, session_id))
        save_conn.commit()
        save_conn.close()

    return Response(stream_with_context(generate()), mimetype='text/event-stream')

@app.route('/api/messages', methods=['GET'])
def get_messages():
    conn = sqlite3.connect('chat_history.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM messages ORDER BY id DESC")
    messages = [dict(row) for row in c.fetchall()]
    conn.close()
    return jsonify(messages)

@app.route('/api/delete', methods=['POST'])
def delete_messages():
    ids = request.json.get("ids", [])
    conn = sqlite3.connect('chat_history.db')
    c = conn.cursor()
    c.execute(f'DELETE FROM messages WHERE id IN ({",".join(["?"]*len(ids))})', ids)
    conn.commit()
    conn.close()
    return jsonify({"status": "success"})

if __name__ == '__main__':
    app.run(debug=True, port=5000)