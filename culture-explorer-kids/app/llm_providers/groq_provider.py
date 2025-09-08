# app/llm_providers/groq_provider.py
import os
from groq import Groq  # pip install groq
from llm_providers.base import LLMProvider
from config import GROQ_API_KEY, GROQ_MODEL


class GroqProvider(LLMProvider):
    def __init__(self, model: str = None):
        super().__init__(model or GROQ_MODEL)

    async def generate(self, prompt: str) -> str:
        """
        Generate a response from Groq LLM using chat completion API.
        Streams the response and accumulates text.
        """
        token = GROQ_API_KEY or os.getenv("GROQ_API_KEY")
        if not token:
            return "❌ Groq API key missing. Set GROQ_API_KEY in config.py or as environment variable."

        try:
            client = Groq(api_key=token)

            completion = client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a friendly cultural guide for kids. "
                            "Explain in simple words with fun examples."
                            
                        )
                    },
                    {"role": "user", "content": prompt}
                ],
                temperature=0.6,
                max_completion_tokens=600,
                top_p=1,
                stream=True,  # streaming mode
                stop=None
            )

            # Accumulate streamed chunks
            full_response = ""
            for chunk in completion:
                delta = chunk.choices[0].delta.content or ""
                full_response += delta

            return full_response or "⚠️ Groq API returned an empty response."

        except Exception as e:
            return f"⚠️ Error calling Groq API: {e}"
