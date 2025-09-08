import os, random
from typing import List,Optional
from config import DEFAULT_BG_KEYWORDS

def get_env(key: str, default: str = "") -> str:
    return os.environ.get(key, default)

def choose_background_url(keywords: Optional[List[str]]) -> str:
    """Return an Unsplash image URL using a keyword. Rotates through keywords."""
    pool = keywords or DEFAULT_BG_KEYWORDS
    query = random.choice(pool).replace(" ", ",")
    # Unsplash random image with query
    return f"https://source.unsplash.com/1600x900/?{query}"

def apply_bg_css(url: str):
    import streamlit as st
    css = f'''
    <style>
      .stApp {{
        background: url("{url}") no-repeat center center fixed;
        background-size: cover;
      }}
      .block-container {{
        backdrop-filter: blur(2px);
        background: rgba(255,255,255,0.65);
        border-radius: 18px;
        padding: 1.2rem 1.2rem 2rem 1.2rem;
      }}
    </style>
    '''
    st.markdown(css, unsafe_allow_html=True)
