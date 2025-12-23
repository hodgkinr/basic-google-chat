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
    limit = MODEL_LIMITS.get(model_id, MODEL_LIMITS["default"])
    
    # Save current user message
    conn = sqlite3.connect('chat_history.db')
    c = conn.cursor()
    c.execute("INSERT INTO messages (role, content, session_id) VALUES (?, ?, ?)", 
              ("user", user_message, session_id))
    conn.commit()
    
    # Pull ONLY this session's history for context
    c.execute("SELECT role, content FROM messages WHERE session_id = ?", (session_id,))
    past_messages = c.fetchall()
    conn.close()

    history_for_gemini = []
    for role, content in past_messages:
        history_for_gemini.append({"role": "user" if role == "user" else "model", "parts": [{"text": content}]})

    def generate():
        full_response = []
        last_chunk = None
        
        stream = client.models.generate_content_stream(
            model=model_id,
            contents=history_for_gemini,
            config=types.GenerateContentConfig(
                system_instruction=get_system_instruction(),
                temperature=0.7
            )
        )
        
        # Stream the text chunks
        for chunk in stream:
            last_chunk = chunk # Keep track of the most recent chunk to get metadata at the end
            if chunk.text:
                full_response.append(chunk.text)
                yield f"data: {json.dumps({'text': chunk.text})}\n\n"
        
        # --- THE FIX: Capture actual usage from the LAST chunk ---
        if last_chunk and last_chunk.usage_metadata:
            meta = last_chunk.usage_metadata
            yield f"data: {json.dumps({
                'usage': round((meta.total_token_count / limit) * 100, 4), 
                'count': meta.total_token_count, 
                'limit': limit
            })}\n\n"
        
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
    # Order by session_id so we can group them easily
    c.execute("SELECT * FROM messages ORDER BY session_id DESC, id ASC")
    rows = [dict(row) for row in c.fetchall()]
    conn.close()

    # Group messages by session_id
    grouped_chats = {}
    for msg in rows:
        s_id = msg['session_id']
        if s_id not in grouped_chats:
            grouped_chats[s_id] = []
        grouped_chats[s_id].append(msg)
        
    return jsonify(grouped_chats)

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