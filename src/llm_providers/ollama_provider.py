import httpx
from llm_providers.base import LLMProvider

OLLAMA_URL = "http://localhost:11434/api/generate"

class OllamaProvider(LLMProvider):
    async def generate(self, prompt: str) -> str:
        payload = {"model": self.model, "prompt": prompt, "stream": False}
        async with httpx.AsyncClient(timeout=120) as client:
            r = await client.post(OLLAMA_URL, json=payload)
            r.raise_for_status()
            data = r.json()
        # Ollama response shape may vary; check "response" key
        return data.get("response", data.get("text", "No response from Ollama."))
