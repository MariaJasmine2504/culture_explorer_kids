import streamlit as st

def base_theme():
    st.markdown('''
    <style>
      h1, h2, h3 { font-family: 'Comic Sans MS', 'Fredoka', 'Poppins', sans-serif; }
      .kid-card {
        background: #ffffffaa;
        border-radius: 20px;
        padding: 1rem 1.2rem;
        box-shadow: 0 6px 28px rgba(0,0,0,0.12);
      }
      .emoji { font-size: 1.2rem; }
      .stButton > button { border-radius: 10px; }
    </style>
    ''', unsafe_allow_html=True)
