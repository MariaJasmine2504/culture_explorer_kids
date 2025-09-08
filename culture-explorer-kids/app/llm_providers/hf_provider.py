import httpx
from llm_providers.base import LLMProvider
from utils import get_env

HF_URL = "https://api-inference.huggingface.co/models/{model}"

class HuggingFaceProvider(LLMProvider):
    async def generate(self, prompt: str) -> str:
        token = get_env("HF_API_TOKEN")
        if not token:
            return "Hugging Face API token missing. Set HF_API_TOKEN to use this provider."
        headers = {"Authorization": f"Bearer {token}"}
        payload = {"inputs": prompt, "parameters": {"max_new_tokens": 350, "temperature": 0.7}}
        async with httpx.AsyncClient(timeout=60) as client:
            r = await client.post(HF_URL.format(model=self.model), headers=headers, json=payload)
            r.raise_for_status()
            data = r.json()
        if isinstance(data, list) and data and "generated_text" in data[0]:
            return data[0]["generated_text"]
        return str(data)
