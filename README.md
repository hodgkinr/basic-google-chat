# basic-google-chat
A google based chatbot that runs in codespace
# Gemini Flask Chatbot 🚀

A full-stack AI chatbot built with Python, Flask, and the Google Gemini 3 Flash API. This project features real-time streaming, Markdown support, and a local SQLite database to manage chat transcripts.

## ✨ Features
- **Real-time Streaming**: Response chunks appear as they are generated.
- **Markdown Rendering**: Beautifully formatted code blocks and text.
- **Transcript Dashboard**: View, delete, and export your chat history.
- **CSV Export**: Download selected chats for offline use.

## 🛠️ Setup Instructions

### 1. Prerequisites
- A [Google AI Studio API Key](https://aistudio.google.com/).
- GitHub Codespaces or a local Python environment.

### 2. Environment Variables
In GitHub Codespaces, go to **Settings > Secrets and variables > Codespaces** and add:
- `GEMINI_API_KEY`: Your Google API Key.

### 3. Installation
```bash
pip install -r requirements.txt
```
### 4. Running the App

```bash
python app.py
```
The app will run on http://127.0.0.1:5000.

📂 Project Structure

app.py: Flask backend & SQLite logic.

templates/index.html: Main chat UI.

templates/history.html: Data management dashboard.

chat_history.db: (Auto-generated) Local database.