from dataclasses import dataclass
from typing import Dict, List
import hashlib

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()

USERS = {
    "kiddo": hash_password("play123"),   # username: hashed_password
    "maria": hash_password("secret123")
}
# Choose your provider: "ollama", "gemini", "huggingface"
LLM_PROVIDER: str = "ollama"

# Model names per provider
PROVIDER_MODELS = {
    "ollama": "llama3.1:8b",
    "gemini": "gemini-1.5-flash",
    "huggingface": "meta-llama/Llama-3.1-8B-Instruct",
    "groq":"llama-3.3-70b-versatile"
}

GROQ_API_KEY = "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"
GROQ_MODEL = "llama-3.3-70b-versatile"
# Mapping topic -> background keyword (Unsplash search term)
TOPIC_BACKGROUNDS: Dict[str, List[str]] = {
    "Japan": ["japan festival children", "anime kids", "japanese food kids"],
    "India": ["india festival children", "indian cartoons", "indian street food"],
    "Mexico": ["mexico festival kids", "mexican food", "mexican folk art"],
}

# Fallback background search terms
DEFAULT_BG_KEYWORDS = ["world map kids", "children learning", "colorful pattern kids"]

# Prompting style
CHILD_TONE_GUIDELINES = [
    "Use simple, friendly language for a 7–10 year-old.",
    "Keep sentences short and cheerful.",
    "Explain festivals, foods, cartoons, and folktales with examples.",
    "Avoid stereotypes; be respectful and factual.",
]

@dataclass(frozen=True)
class UISettings:
    app_title_v1: str = "🌍 Culture Explorer for Kids"
    app_title: str = "CurioQuest 🧭✨"
    footer_text: str = "Made with ❤️ for curious kids"
    sidebar_title: str = "Explore"
    compare_tab_label: str = "Compare with my culture"

UI = UISettings()
