import google.generativeai as genai
from fastapi.responses import StreamingResponse
import os

threads = {}  # store chat history per thread id

class ChatService:
    @staticmethod
    async def generate_stream(message: str, thread_id: str):
        global threads

        if thread_id not in threads:
            threads[thread_id] = [
                {"role": "user", "content": "You are an intelligent AI assistant."}
            ]

        threads[thread_id].append({"role": "user", "content": message})

        history = [{"role": m["role"], "parts": [m["content"]]} for m in threads[thread_id]]

        model = genai.GenerativeModel("gemini-2.0-flash")
        response = model.generate_content(history, stream=True)

        async def event_stream():
            full_reply = ""
            for chunk in response:
                if chunk.candidates and chunk.candidates[0].content.parts:
                    delta = chunk.candidates[0].content.parts[0].text
                    if delta:
                        full_reply += delta
                        yield delta

            threads[thread_id].append({"role": "model", "content": full_reply})

        return StreamingResponse(event_stream(), media_type="text/event-stream")
