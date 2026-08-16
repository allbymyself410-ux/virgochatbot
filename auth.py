import streamlit as st
import json
from datetime import datetime, timedelta
import hashlib
import os
from pathlib import Path

# User data management
USERS_FILE = Path(".streamlit/users.json")
USERS_FILE.parent.mkdir(exist_ok=True)

class AuthManager:
    """Manages user authentication and VIP access control"""
    
    @staticmethod
    def load_users():
        """Load user data from file"""
        if USERS_FILE.exists():
            with open(USERS_FILE, 'r') as f:
                return json.load(f)
        return {}
    
    @staticmethod
    def save_users(users):
        """Save user data to file"""
        with open(USERS_FILE, 'w') as f:
            json.dump(users, f, indent=2)
    
    @staticmethod
    def hash_password(password):
        """Hash password for storage"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    @staticmethod
    def register_user(username, password, is_vip=False):
        """Register a new user"""
        users = AuthManager.load_users()
        if username in users:
            return False, "Username already exists"
        
        users[username] = {
            "password_hash": AuthManager.hash_password(password),
            "is_vip": is_vip,
            "created_at": datetime.now().isoformat(),
            "chatbots": []
        }
        AuthManager.save_users(users)
        return True, "User registered successfully"
    
    @staticmethod
    def login_user(username, password):
        """Authenticate user"""
        users = AuthManager.load_users()
        if username not in users:
            return False, "User not found"
        
        user = users[username]
        if user["password_hash"] != AuthManager.hash_password(password):
            return False, "Invalid password"
        
        return True, user
    
    @staticmethod
    def is_vip_user(username):
        """Check if user has VIP access"""
        users = AuthManager.load_users()
        return users.get(username, {}).get("is_vip", False)
    
    @staticmethod
    def promote_to_vip(username):
        """Upgrade user to VIP"""
        users = AuthManager.load_users()
        if username in users:
            users[username]["is_vip"] = True
            AuthManager.save_users(users)
            return True
        return False

def init_auth_session():
    """Initialize authentication session state"""
    if "user_logged_in" not in st.session_state:
        st.session_state.user_logged_in = False
    if "current_user" not in st.session_state:
        st.session_state.current_user = None
    if "is_vip" not in st.session_state:
        st.session_state.is_vip = False

def login_page():
    """Display login/register page"""
    st.title("🔐 Virgo Chatbot - Login")
    
    tab1, tab2 = st.tabs(["Login", "Register"])
    
    with tab1:
        st.write("Sign in to your account")
        username = st.text_input("Username", key="login_user")
        password = st.text_input("Password", type="password", key="login_pass")
        
        if st.button("Login", key="login_btn"):
            success, result = AuthManager.login_user(username, password)
            if success:
                st.session_state.user_logged_in = True
                st.session_state.current_user = username
                st.session_state.is_vip = result.get("is_vip", False)
                st.success(f"Welcome back, {username}!")
                st.rerun()
            else:
                st.error(result)
    
    with tab2:
        st.write("Create a new account")
        new_username = st.text_input("Choose a username", key="reg_user")
        new_password = st.text_input("Choose a password", type="password", key="reg_pass")
        confirm_password = st.text_input("Confirm password", type="password", key="reg_confirm")
        
        if st.button("Register", key="reg_btn"):
            if new_password != confirm_password:
                st.error("Passwords do not match")
            elif len(new_password) < 6:
                st.error("Password must be at least 6 characters")
            else:
                success, message = AuthManager.register_user(new_username, new_password)
                if success:
                    st.success(message)
                    st.info("You can now login with your credentials")
                else:
                    st.error(message)

def logout():
    """Logout current user"""
    st.session_state.user_logged_in = False
    st.session_state.current_user = None
    st.session_state.is_vip = False
