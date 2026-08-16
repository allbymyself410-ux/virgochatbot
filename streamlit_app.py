import streamlit as st
from auth import init_auth_session, login_page, AuthManager
from chatbot_builder import builder_ui, edit_chatbot_ui
from chatbot_runner import ChatbotRunner
from vip_manager import vip_page, VIPManager

# Page config
st.set_page_config(
    page_title="Virgo Chatbot - No-Code AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session
init_auth_session()

# Main app
if not st.session_state.user_logged_in:
    login_page()
else:
    # Sidebar
    with st.sidebar:
        st.title(f"🤖 Virgo Chatbot")
        st.write(f"Welcome, **{st.session_state.current_user}**")
        
        if st.session_state.is_vip:
            st.success("🌟 VIP Member")
        else:
            if st.button("✨ Upgrade to VIP", use_container_width=True):
                st.session_state.page = "vip"
        
        st.divider()
        
        # Navigation
        pages = {
            "🏠 Home": "home",
            "🤖 Build Chatbot": "builder",
            "🌟 VIP Features": "vip",
            "🚪 Logout": "logout"
        }
        
        page = st.radio("Navigation", list(pages.keys()), label_visibility="collapsed")
        st.session_state.page = pages[page]
    
    # Route pages
    if st.session_state.page == "logout":
        from auth import logout
        logout()
        st.rerun()
    
    elif st.session_state.page == "home":
        st.title("🤖 Welcome to Virgo Chatbot")
        st.write(
            """
            Create and manage custom AI chatbots without writing a single line of code!
            
            ### Getting Started:
            1. **Build** - Create your first chatbot using the builder
            2. **Customize** - Set the personality, model, and behavior
            3. **Deploy** - Use your chatbot in conversations
            4. **Upgrade to VIP** - Unlock advanced editing and features
            """
        )
        
        st.divider()
        st.subheader("📊 Your Stats")
        from chatbot_builder import ChatbotBuilder
        chatbots = ChatbotBuilder.list_user_chatbots(st.session_state.current_user)
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Chatbots Created", len(chatbots))
        col2.metric("Account Status", "VIP" if st.session_state.is_vip else "Free")
        col3.metric("Member Since", "Today")
        
        st.divider()
        st.subheader("🚀 Quick Start")
        if st.button("Create Your First Chatbot", use_container_width=True):
            st.session_state.page = "builder"
            st.rerun()
    
    elif st.session_state.page == "builder":
        # Check if editing existing chatbot
        if "edit_mode" in st.session_state and st.session_state.edit_mode:
            edit_chatbot_ui(st.session_state.selected_chatbot, st.session_state.is_vip)
        
        # Check if running chatbot
        elif "selected_chatbot" in st.session_state and st.session_state.selected_chatbot:
            openai_api_key = st.text_input("OpenAI API Key", type="password")
            if openai_api_key:
                ChatbotRunner.run_chatbot(st.session_state.selected_chatbot, openai_api_key)
            else:
                st.info("Enter your OpenAI API key to test the chatbot")
        
        # Show builder
        else:
            builder_ui()
    
    elif st.session_state.page == "vip":
        vip_page()
