# auth.py
import streamlit as st
import hashlib
from config import USERS  # { "username": "hashed_password" }

def hash_password(password: str) -> str:
    """Return SHA256 hash of the password."""
    return hashlib.sha256(password.encode("utf-8")).hexdigest()

def login_form():
    st.subheader("Login")
    if "auth_user" not in st.session_state:
        st.session_state["auth_user"] = None

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Let me in 🚀", type="primary"):
        if username in USERS and USERS[username] == hash_password(password):
            st.session_state["auth_user"] = username
            st.success(f"Welcome, {username} 🎈")
        else:
            st.error("Invalid credentials.")
    return st.session_state.get("auth_user")

def logout_button():
    if st.button("Logout"):
        st.session_state.pop("auth_user", None)
        st.experimental_rerun()
