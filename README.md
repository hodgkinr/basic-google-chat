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

🔑 Step-by-Step: Adding your Gemini Key
Go to your Repository on GitHub.com: Make sure you are on the main page of your project (not inside the Codespace editor).

Click "Settings": This is the last tab in the top navigation bar (next to "Insights").

Find "Secrets and variables": On the left-hand sidebar, scroll down to the Security section. Click the arrow next to Secrets and variables to expand it.

Click "Codespaces": You will see three options (Actions, Codespaces, Dependabot). You must choose Codespaces for the key to work inside your editor.

New Repository Secret: Click the green button that says New repository secret.

Enter the Details:

Name: GEMINI_API_KEY (It must be exactly this for the app.py code to find it).

Secret: Paste your key from Google AI Studio here.

Add Secret: Click the Add secret button.

🔄 Important: Refreshing your Codespace
GitHub does not automatically "push" new secrets into an active Codespace for security reasons.

Go back to your open Codespace tab.

A notification might pop up in the bottom right saying "Secrets have changed. Reload to apply." Click Reload.

If you don't see the popup: Close the Codespace tab and reopen it from your GitHub repo. This "reboots" the environment with your new key.

🧪 How to verify it worked
To make sure the key is actually there, type this into your Codespace terminal:

echo $GEMINI_API_KEY
If it prints out your key (or a part of it), you are ready to run python app.py!

If that doesn't work you need to force a stop to codespaces. 

inside the Chrome/browser window where your Codespace is running.

Click anywhere inside the dark area of the code editor to make sure it's "focused."

Press the shortcut:

Windows/Linux: Ctrl + Shift + P

Mac: Cmd + Shift + P

Alternative (No Keyboard): If the shortcut isn't working, click the Gear Icon ⚙️ in the bottom-left corner of the Codespace and select Command Palette.

🔄 How to perform the "Full Stop"
Once that little search bar pops up at the top of your screen:

Type the word "Stop" into the bar.

Click on the option that says: Codespaces: Stop Codespace.

The screen will turn dark with a "Codespace stopped" message.

Now, Refresh your browser tab (the standard Chrome refresh button). This will force the machine to boot from scratch and pull in your new GEMINI_API_KEY.

### 3. Installation

```bash
python -m venv .venv
source .venv/bin/activate
```

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