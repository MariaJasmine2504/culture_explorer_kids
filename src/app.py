import asyncio
import streamlit as st
import styles
from config import UI, TOPIC_BACKGROUNDS, LLM_PROVIDER
from validators import CultureQuery
from utils import choose_background_url, apply_bg_css
from culture_logic import make_provider
from auth import login_form, logout_button

st.set_page_config(page_title=UI.app_title, page_icon="🌍", layout="centered")
styles.base_theme()

# 🎨 Inject playful Google Font (Comic Neue as example)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/share?selection.family=Patrick+Hand');

    html, body, [class*="css"]  {
        font-family: 'Patrick Hand', cursive !important;
    }

    /* Optional: style buttons a bit rounder */
    .stButton button {
        border-radius: 12px;
        font-size: 1.1rem;
        padding: 0.5em 1.2em;
    }
    </style>
""", unsafe_allow_html=True)



st.markdown(f"# {UI.app_title}")
st.markdown(
            f"""
            Hey **little explorer**! 🌟  
            Get ready to **travel the world** right from your screen! 🌍  
            Discover **lit festivals 🎉, delish foods 🍲, cute animals 🐼,  
            and epic stories 📖**.  
            Every click = a new adventure — **learn, laugh, and vibe with curiosity** 🚀✨
 
            """
        )
# --- Auth ---
user = st.session_state.get("auth_user") or login_form()
if not user:
    st.stop()
logout_button()

# ---------- Form (persist into session_state) ----------
with st.form("culture_form", clear_on_submit=False):
    col1, col2 = st.columns([2,2])
    with col1:
        country_input = st.text_input(
            "Enter a country or culture",
            placeholder="e.g., Japan",
            value=st.session_state.get("country", "")
        )
    with col2:
        my_culture_input = st.text_input(
            "(Optional) Your culture for comparison",
            placeholder="e.g., India",
            value=st.session_state.get("my_culture", "")
        )

    providers = ["groq"] #"ollama", "gemini", "huggingface", 
    default_provider = st.session_state.get("provider_name", LLM_PROVIDER)
    provider_index = providers.index(default_provider) if default_provider in providers else providers.index(LLM_PROVIDER)
    provider_input = st.selectbox("LLM Provider", providers, index=provider_index)

    submitted = st.form_submit_button("Explore ✨")
    if submitted:
        # persist values so reruns don't lose them
        st.session_state["explored"] = True
        st.session_state["country"] = country_input.strip()
        st.session_state["my_culture"] = my_culture_input.strip()
        st.session_state["provider_name"] = provider_input

# If user hasn't explored yet, show tip and stop
if not st.session_state.get("explored", False):
    st.info("Tip: Try 'Japan', 'India', or 'Mexico' to get started!")
    st.stop()

# ---------- Use persisted values ----------
country = st.session_state["country"]
my_culture = st.session_state.get("my_culture")
provider_name = st.session_state.get("provider_name", LLM_PROVIDER)

# Apply background for the chosen topic
keywords = TOPIC_BACKGROUNDS.get(country, None)
bg_url = choose_background_url(keywords)
# apply_bg_css(bg_url)

# create provider
provider = make_provider(provider_name)
tone_rules = ["use simple words", "be cheerful", "use emojis"]

# ---------- Immediate attention-grabber ----------
if country and my_culture:
    diff_text = asyncio.run(provider.compare_cultures(my_culture, country, tone_rules))
    about_text = asyncio.run(provider.kid_friendly_guide(country, tone_rules))
if country and not my_culture:
    about_text = asyncio.run(provider.kid_friendly_guide(country, tone_rules))
    diff_text = "Add your own culture in the box above to see how they compare!"


col_a, col_b = st.columns([1,1])
with col_a:
    st.subheader("🌟 About")
    st.markdown(about_text)
with col_b:
    st.subheader("🌟 Differences")
    st.markdown(diff_text)

# ---------- Curiosity / Interactive toggles ----------
if "interactive" not in st.session_state:
    st.session_state["interactive"] = False

# col_a, col_b = st.columns([1,1])
# with col_a:
#     left, middle, right = st.columns(3)
#     if middle.button("Curious to know more? 🤔", key="curious_button"):
#         st.session_state["interactive"] = True
# with col_b:
#     left, middle, right = st.columns(3)
#     if right.button("Back to Explore ✨", key="back_button",type='primary'):
#         # reset the exploration state so user can enter new inputs
#         st.session_state["explored"] = False
#         st.session_state["interactive"] = False
#         st.session_state.pop("history", None)
#         st.rerun()
cola,colb,colc = st.columns(3)
if colc.button("More curious? 🤔", key="curious_button"):
    st.session_state["interactive"] = True


# ---------- Interactive Chat Session ----------
if st.session_state["interactive"]:
    if "history" not in st.session_state:
        st.session_state["history"] = []

    st.subheader("💬 Ask me anything about this culture!")

    # Render history
    for role, msg in st.session_state["history"]:
        with st.chat_message(role):
            st.markdown(msg)

    # Chat input for follow-ups
    user_question = st.chat_input("Ask about foods, animals, schools...")
    if user_question:
        # persist user message
        st.session_state["history"].append(("user", user_question))

        # build prompt (include tone rules so LLM keeps kid-friendly style)
        prompt = f"Kid asks about {country}: {user_question}\nTone rules: {', '.join(tone_rules)}"

        # generate answer (show spinner while waiting)
        with st.toast("Thinking..."):
            answer = asyncio.run(provider.generate(prompt))
            # apply your provider's guardrails
            if hasattr(provider, "apply_guardrails"):
                answer = provider.apply_guardrails(answer)

        # persist assistant reply and rerun to display
        st.session_state["history"].append(("assistant", answer))
        st.rerun()
        
# --- Add Clear Chat button here ---
    if len(st.session_state["history"]) > 1:
        clear_placeholder = st.empty()
        with clear_placeholder.container():
            cola, colb, colc, cold, cole, colf, colg,colh,coli = st.columns(9)
            if coli.button("🧹 ", key="clear_chat", type="secondary",help="Clear chat history"):
                st.session_state["history"] = []
                st.session_state["interactive"] = False
                st.rerun()
# # footer
# st.markdown(f"<br><br><center>{UI.footer_text}</center>", unsafe_allow_html=True)
