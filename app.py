import sqlite3
import json
import os
from flask import Flask, render_template, request, Response, stream_with_context, jsonify
from google import genai

app = Flask(__name__)

# Configure Gemini Client
# Make sure GEMINI_API_KEY is in your Codespaces Secrets!
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

def init_db():
    conn = sqlite3.connect('chat_history.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS messages 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, role TEXT, content TEXT)''')
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
    user_message = request.json.get("message")
    
    # Save User Message
    conn = sqlite3.connect('chat_history.db')
    c = conn.cursor()
    c.execute("INSERT INTO messages (role, content) VALUES (?, ?)", ("user", user_message))
    conn.commit()
    conn.close()

    def generate():
        full_response = []
        # Setup the streaming request to Gemini
        stream = client.models.generate_content_stream(
            model="gemini-2.5-flash-lite",
            contents=user_message
        )
        
        for chunk in stream:
            if chunk.text:
                full_response.append(chunk.text)
                yield f"data: {json.dumps({'text': chunk.text})}\n\n"
        
        # Save complete Bot Response after stream ends
        final_text = "".join(full_response)
        conn = sqlite3.connect('chat_history.db')
        c = conn.cursor()
        c.execute("INSERT INTO messages (role, content) VALUES (?, ?)", ("bot", final_text))
        conn.commit()
        conn.close()

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