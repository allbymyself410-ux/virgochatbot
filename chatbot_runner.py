import streamlit as st
from openai import OpenAI
from chatbot_builder import ChatbotBuilder
from datetime import datetime
import json
from pathlib import Path

# Chat history storage
HISTORY_DIR = Path(".streamlit/chat_history")
HISTORY_DIR.mkdir(exist_ok=True)

class ChatbotRunner:
    """Executes chatbot conversations"""
    
    @staticmethod
    def initialize_session(chatbot_id):
        """Initialize chat session for a chatbot"""
        if f"chatbot_{chatbot_id}_messages" not in st.session_state:
            st.session_state[f"chatbot_{chatbot_id}_messages"] = []
    
    @staticmethod
    def save_chat_history(chatbot_id, username, messages):
        """Save chat conversation"""
        history_file = HISTORY_DIR / f"{chatbot_id}_{username}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(history_file, 'w') as f:
            json.dump({
                "chatbot_id": chatbot_id,
                "username": username,
                "timestamp": datetime.now().isoformat(),
                "messages": messages
            }, f, indent=2)
    
    @staticmethod
    def run_chatbot(chatbot_id, openai_api_key):
        """Run chatbot interface"""
        chatbot = ChatbotBuilder.load_chatbot(chatbot_id)
        if not chatbot:
            st.error("Chatbot not found")
            return
        
        st.title(f"💬 {chatbot['name']}")
        st.write(chatbot["description"])
        
        # Initialize chat session
        ChatbotRunner.initialize_session(chatbot_id)
        messages_key = f"chatbot_{chatbot_id}_messages"
        
        # Display chat history
        for message in st.session_state[messages_key]:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # Chat input
        if prompt := st.chat_input("Your message..."):
            # Add user message
            st.session_state[messages_key].append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            
            try:
                # Create OpenAI client
                client = OpenAI(api_key=openai_api_key)
                
                # Build messages with system prompt
                api_messages = [
                    {"role": "system", "content": chatbot["system_prompt"]}
                ]
                api_messages.extend(st.session_state[messages_key])
                
                # Generate response
                stream = client.chat.completions.create(
                    model=chatbot["model"],
                    messages=api_messages,
                    temperature=chatbot["temperature"],
                    max_tokens=chatbot["max_tokens"],
                    stream=True
                )
                
                # Stream response
                with st.chat_message("assistant"):
                    response = st.write_stream(stream)
                
                # Add assistant message
                st.session_state[messages_key].append({
                    "role": "assistant",
                    "content": response
                })
                
                # Save history periodically
                if len(st.session_state[messages_key]) % 10 == 0:
                    ChatbotRunner.save_chat_history(
                        chatbot_id,
                        st.session_state.current_user,
                        st.session_state[messages_key]
                    )
            
            except Exception as e:
                st.error(f"Error: {str(e)}")
        
        # Chat controls
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("🔄 Clear Chat", use_container_width=True):
                st.session_state[messages_key] = []
                st.rerun()
        
        with col2:
            if st.button("💾 Save History", use_container_width=True):
                ChatbotRunner.save_chat_history(
                    chatbot_id,
                    st.session_state.current_user,
                    st.session_state[messages_key]
                )
                st.success("Chat saved!")
        
        with col3:
            if st.button("⬅️ Back", use_container_width=True):
                st.session_state.selected_chatbot = None
                st.rerun()
