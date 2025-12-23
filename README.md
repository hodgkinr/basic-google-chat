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

## 🔑 Step-by-Step: Adding your Gemini Key

1. **Go to your Repository on GitHub.com**: Navigate to the main page of your project (outside of the Codespace editor).
2. **Click "Settings"**: This is the last tab in the top navigation bar (next to "Insights").
3. **Find "Secrets and variables"**: On the left-hand sidebar, scroll down to the **Security** section. Click the arrow next to **Secrets and variables** to expand it.
4. **Click "Codespaces"**: You will see three options (Actions, Codespaces, Dependabot). **You must choose Codespaces** for the key to work inside your editor.
5. **New Repository Secret**: Click the green button that says `New repository secret`.
6. **Enter the Details**:
   - **Name**: `GEMINI_API_KEY` (It must be exactly this for the `app.py` code to find it).
   - **Secret**: Paste your key from Google AI Studio here.
7. **Add Secret**: Click the `Add secret` button.

---

## 🔄 Important: Refreshing your Codespace
GitHub does not automatically "push" new secrets into an active Codespace for security reasons.

1. Go back to your open **Codespace tab**.
2. A notification might pop up in the bottom right saying *"Secrets have changed. Reload to apply."* Click **Reload**.
3. **If you don't see the popup**, you must perform a **Full Stop** to force the environment to pull in your new key.

### How to perform a "Full Stop"
1. **Focus the Editor**: Click anywhere inside the dark area of the code editor.
2. **Open the Command Palette**:
   - **Windows/Linux**: `Ctrl + Shift + P`
   - **Mac**: `Cmd + Shift + P`
   - *Alternative*: Click the **Gear Icon** ⚙️ (bottom-left) and select **Command Palette**.
3. **Run the Stop Command**: Type `Stop` into the bar and select `Codespaces: Stop Codespace`.
4. **Restart**: Once the screen goes dark, **Refresh your browser tab**. This forces the machine to boot from scratch with the new `GEMINI_API_KEY`.

---

## 🧪 How to verify it worked
To make sure the key is actually there, type this into your Codespace terminal:

```bash
echo $GEMINI_API_KEY
```
[!TIP] If it prints out your key (or stars ***), you are ready! If it prints a blank line, the secret hasn't loaded yet—repeat the "Full Stop" steps above.
---

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

### 5. Gotchas
If you dont get a response from the chat, it's likely that the model name isn't exactly correct in app.py. The line is model="gemini-2.5-flash-lite". You can see what available models your api key has access to by running

```bash
python list_models.py
```
Then find the one you want, copy and paste it, and you're good to go. 

📂 Project Structure

app.py: Flask backend & SQLite logic.

templates/index.html: Main chat UI.

templates/history.html: Data management dashboard.

chat_history.db: (Auto-generated) Local database.