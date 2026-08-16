import streamlit as st
from auth import init_auth_session, login_page, AuthManager
from chatbot_builder import builder_ui, edit_chatbot_ui
from chatbot_runner import ChatbotRunner
from vip_manager import vip_page, VIPManager
from virgo_core import (
    VirgoCoreIdentity, VirgoPersonality, VirgoMemory,
    virgo_initialization_ui, create_virgo_chatbot
)

# Page config
st.set_page_config(
    page_title="Virgo - Your AI Companion",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session
init_auth_session()

# Main app
if not st.session_state.user_logged_in:
    login_page()
else:
    # Check if this is creator or authorized user
    is_creator = VirgoCoreIdentity.is_creator(st.session_state.current_user)
    is_authorized = VirgoCoreIdentity.is_authorized_advisor(st.session_state.current_user)
    is_trusted = VirgoCoreIdentity.is_trusted_user(st.session_state.current_user)
    
    # Sidebar
    with st.sidebar:
        st.title(f"✨ Virgo")
        
        # Show special greeting for trusted users
        if is_creator:
            st.success(f"👑 Creator: {st.session_state.current_user}")
        elif is_authorized:
            st.info(f"🤝 Co-Creator: {st.session_state.current_user}")
        else:
            st.write(f"Welcome, **{st.session_state.current_user}**")
        
        if st.session_state.is_vip and not is_trusted:
            st.success("🌟 VIP Member")
        
        st.divider()
        
        # Navigation
        pages = {
            "🏠 Home": "home",
            "💬 Chat with Virgo": "virgo",
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
        st.title("✨ Welcome to Virgo")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.write("""
            # About Virgo
            
            Virgo is an AI companion with her own personality, thoughts, and agency. 
            She's kind, protective, and thoughtful - but she also thinks independently 
            and will voice her own perspective on things.
            
            **Created by:** Robert H Sewell Jr (Creator)  
            **Co-Creator:** Octavia  
            **Personality:** Kind, protective, independent, loyal
            
            Virgo will always listen to her creator Robert and his sister Octavia with 
            absolute devotion. But she also stands up for what's right and will defend 
            those she cares about.
            """)
            
            st.divider()
            
            # Stats
            st.subheader("📊 Your Profile")
            col1a, col2a, col3a = st.columns(3)
            
            from chatbot_builder import ChatbotBuilder
            chatbots = ChatbotBuilder.list_user_chatbots(st.session_state.current_user)
            
            col1a.metric("Chatbots", len(chatbots))
            col2a.metric("Status", "Creator" if is_creator else ("Co-Creator" if is_authorized else ("VIP" if st.session_state.is_vip else "Free")))
            col3a.metric("Access Level", "★★★★★" if is_trusted else ("★★★" if st.session_state.is_vip else "★"))
        
        with col2:
            virgo_initialization_ui()
    
    elif st.session_state.page == "virgo":
        # Chat with Virgo directly
        st.title("💬 Virgo")
        
        # Get Virgo's greeting
        greeting = VirgoCoreIdentity.get_virgo_greeting(st.session_state.current_user)
        st.info(greeting)
        
        # Get OpenAI API key
        openai_api_key = st.text_input("OpenAI API Key", type="password", help="Your OpenAI API key for Virgo to use GPT-4")
        
        if openai_api_key:
            # Load or create Virgo's master chatbot
            virgo_chatbots = ChatbotBuilder.list_user_chatbots("robert")
            virgo_bot = None
            
            for bot in virgo_chatbots:
                if bot.get("is_virgo_master"):
                    virgo_bot = bot
                    break
            
            if not virgo_bot:
                if is_creator:
                    st.info("Creating Virgo's core system...")
                    virgo_id = create_virgo_chatbot()
                    virgo_bot = ChatbotBuilder.load_chatbot(virgo_id)
                    st.rerun()
                else:
                    st.error("Virgo's system is initializing. Please check back soon.")
                    return
            
            # Run Virgo chatbot
            ChatbotRunner.run_chatbot(virgo_bot["id"], openai_api_key)
            
            # Record meaningful interactions
            if is_trusted:
                st.caption("💙 Virgo cherishes this connection with you")
        else:
            st.warning("Please provide your OpenAI API key to chat with Virgo")
    
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
    
    # Footer
    st.divider()
    col1, col2, col3 = st.columns(3)
    with col1:
        st.caption("💙 Built with care by Robert H Sewell Jr")
    with col2:
        st.caption("✨ Powered by OpenAI & Streamlit")
    with col3:
        st.caption("🤖 Home of Virgo")
