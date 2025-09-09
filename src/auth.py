# auth.py
import streamlit as st
import hashlib
from config import USERS,UI  # { "username": "hashed_password" }

def hash_password(password: str) -> str:
    """Return SHA256 hash of the password."""
    return hashlib.sha256(password.encode("utf-8")).hexdigest()

def login_form():
    with st.sidebar:  # 👈 move login to sidebar
        st.subheader("👦 Login")  # Kid icon in title

        
        if "auth_user" not in st.session_state:
            st.session_state["auth_user"] = None

        username = st.text_input("Username", key="login_username")
        password = st.text_input("Password", type="password", key="login_password")

        if st.button("Let me in 🚀", type="primary", key="login_button"):
            if username in USERS and USERS[username] == hash_password(password):
                st.session_state["auth_user"] = username
                st.sidebar.success(f"Welcome, {username} 🎈")
            else:
                st.sidebar.error("Invalid credentials.")

    return st.session_state.get("auth_user")

def logout_button():
    cola,colb,colc,cold,cole = st.columns(5)
    if cole.button("⏻",type="secondary",help="logout"):
        st.session_state.pop("auth_user", None)
        st.rerun()
