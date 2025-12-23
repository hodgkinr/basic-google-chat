from google import genai
import os

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

print("Checking available models for your API key...")
for m in client.models.list():
    # Only show models that support generating content
    if 'generateContent' in m.supported_actions:
        print(f"- {m.name}")