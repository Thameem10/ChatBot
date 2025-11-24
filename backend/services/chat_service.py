import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

threads = {}

class ChatService:
    @staticmethod
    async def generate_response(message: str, thread_id: str):
        if thread_id not in threads:
            threads[thread_id] = [
                {"role": "user", "content": "You are an intelligent AI assistant."}
            ]

        threads[thread_id].append({"role": "user", "content": message})

        history = [{"role": m["role"], "parts": [m["content"]]} for m in threads[thread_id]]

        model = genai.GenerativeModel("models/gemini-2.5-flash")

        response = model.generate_content(history)
        reply = response.text

        threads[thread_id].append({"role": "model", "content": reply})

        return reply
