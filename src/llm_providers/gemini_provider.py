import httpx, os
from llm_providers.base import LLMProvider
from utils import get_env

GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"

class GeminiProvider(LLMProvider):
    async def generate(self, prompt: str) -> str:
        api_key = get_env("GEMINI_API_KEY")
        if not api_key:
            return "Gemini API key missing. Set GEMINI_API_KEY to use this provider."
        url = GEMINI_URL.format(model=self.model)
        payload = {"contents": [{"parts": [{"text": prompt}]}]}
        async with httpx.AsyncClient(timeout=30) as client:
            r = await client.post(url, params={"key": api_key}, json=payload)
            r.raise_for_status()
            data = r.json()
        try:
            return data["candidates"][0]["content"]["parts"][0]["text"]
        except Exception:
            return str(data)
