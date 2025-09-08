from typing import Optional
from config import CHILD_TONE_GUIDELINES, PROVIDER_MODELS
from llm_providers.ollama_provider import OllamaProvider
from llm_providers.gemini_provider import GeminiProvider
from llm_providers.hf_provider import HuggingFaceProvider
from llm_providers.groq_provider import GroqProvider

def make_provider(name: str):
    model = PROVIDER_MODELS.get(name, "")
    if name == "groq":
        return GroqProvider(model)
    if name == "gemini":
        return GeminiProvider(model)
    if name == "huggingface":
        return HuggingFaceProvider(model)
    return OllamaProvider(model)

async def build_kid_page(provider, country: str) -> str:
    return await provider.kid_friendly_guide(country, CHILD_TONE_GUIDELINES)

async def build_compare(provider, my: str, target: str) -> str:
    return await provider.compare_cultures(my, target, CHILD_TONE_GUIDELINES)
