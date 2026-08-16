import streamlit as st
import json
from datetime import datetime
from pathlib import Path
import uuid

# Chatbot configuration storage
CHATBOTS_DIR = Path(".streamlit/chatbots")
CHATBOTS_DIR.mkdir(exist_ok=True)

class ChatbotBuilder:
    """No-code chatbot builder interface"""
    
    @staticmethod
    def create_chatbot_config(
        name,
        description,
        system_prompt,
        model="gpt-3.5-turbo",
        temperature=0.7,
        max_tokens=500,
        owner=""
    ):
        """Create a new chatbot configuration"""
        chatbot_id = str(uuid.uuid4())
        config = {
            "id": chatbot_id,
            "name": name,
            "description": description,
            "system_prompt": system_prompt,
            "model": model,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "owner": owner,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "is_active": True,
            "custom_context": [],
            "behavior_rules": []
        }
        
        config_path = CHATBOTS_DIR / f"{chatbot_id}.json"
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)
        
        return chatbot_id, config
    
    @staticmethod
    def load_chatbot(chatbot_id):
        """Load chatbot configuration"""
        config_path = CHATBOTS_DIR / f"{chatbot_id}.json"
        if config_path.exists():
            with open(config_path, 'r') as f:
                return json.load(f)
        return None
    
    @staticmethod
    def save_chatbot(chatbot_id, config):
        """Save chatbot configuration"""
        config["updated_at"] = datetime.now().isoformat()
        config_path = CHATBOTS_DIR / f"{chatbot_id}.json"
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)
    
    @staticmethod
    def list_user_chatbots(username):
        """List all chatbots owned by a user"""
        chatbots = []
        for config_path in CHATBOTS_DIR.glob("*.json"):
            with open(config_path, 'r') as f:
                config = json.load(f)
                if config.get("owner") == username:
                    chatbots.append(config)
        return sorted(chatbots, key=lambda x: x["created_at"], reverse=True)
    
    @staticmethod
    def delete_chatbot(chatbot_id):
        """Delete a chatbot"""
        config_path = CHATBOTS_DIR / f"{chatbot_id}.json"
        if config_path.exists():
            config_path.unlink()
            return True
        return False
    
    @staticmethod
    def duplicate_chatbot(chatbot_id, new_owner):
        """Duplicate a chatbot for a new owner"""
        config = ChatbotBuilder.load_chatbot(chatbot_id)
        if config:
            config["owner"] = new_owner
            new_id, _ = ChatbotBuilder.create_chatbot_config(
                name=f"{config['name']} (Copy)",
                description=config["description"],
                system_prompt=config["system_prompt"],
                model=config["model"],
                temperature=config["temperature"],
                max_tokens=config["max_tokens"],
                owner=new_owner
            )
            return new_id
        return None

def builder_ui():
    """Display no-code chatbot builder interface"""
    from auth import AuthManager
    
    st.header("🤖 Build Your Chatbot")
    
    tab1, tab2 = st.tabs(["Create New", "Manage Existing"])
    
    with tab1:
        st.subheader("Create a New Chatbot")
        
        with st.form("chatbot_form"):
            name = st.text_input(
                "Chatbot Name",
                placeholder="e.g., Customer Support Bot",
                help="Give your chatbot a memorable name"
            )
            
            description = st.text_area(
                "Description",
                placeholder="What does this chatbot do?",
                help="Describe the purpose of your chatbot"
            )
            
            system_prompt = st.text_area(
                "System Prompt",
                placeholder="You are a helpful customer service representative...",
                height=150,
                help="Define how your chatbot should behave and respond"
            )
            
            col1, col2 = st.columns(2)
            with col1:
                model = st.selectbox(
                    "AI Model",
                    ["gpt-3.5-turbo", "gpt-4"],
                    help="Select the language model to use"
                )
                
                temperature = st.slider(
                    "Temperature (Creativity)",
                    min_value=0.0,
                    max_value=2.0,
                    value=0.7,
                    step=0.1,
                    help="Lower = more focused, Higher = more creative"
                )
            
            with col2:
                max_tokens = st.slider(
                    "Max Response Length",
                    min_value=100,
                    max_value=2000,
                    value=500,
                    step=50,
                    help="Maximum length of chatbot responses"
                )
            
            submitted = st.form_submit_button("✨ Create Chatbot", use_container_width=True)
            
            if submitted:
                if not name or not description or not system_prompt:
                    st.error("Please fill in all fields")
                else:
                    chatbot_id, config = ChatbotBuilder.create_chatbot_config(
                        name=name,
                        description=description,
                        system_prompt=system_prompt,
                        model=model,
                        temperature=temperature,
                        max_tokens=max_tokens,
                        owner=st.session_state.current_user
                    )
                    st.success(f"✅ Chatbot '{name}' created successfully!")
                    st.session_state.selected_chatbot = chatbot_id
                    st.rerun()
    
    with tab2:
        st.subheader("Manage Your Chatbots")
        
        chatbots = ChatbotBuilder.list_user_chatbots(st.session_state.current_user)
        
        if not chatbots:
            st.info("You haven't created any chatbots yet. Create one in the 'Create New' tab!")
        else:
            for chatbot in chatbots:
                with st.container(border=True):
                    col1, col2, col3 = st.columns([3, 1, 1])
                    
                    with col1:
                        st.write(f"**{chatbot['name']}**")
                        st.caption(chatbot["description"])
                        st.caption(f"Created: {chatbot['created_at'][:10]} | Model: {chatbot['model']}")
                    
                    with col2:
                        if st.button("✏️ Edit", key=f"edit_{chatbot['id']}"):
                            st.session_state.selected_chatbot = chatbot["id"]
                            st.session_state.edit_mode = True
                            st.rerun()
                    
                    with col3:
                        if st.button("🗑️ Delete", key=f"delete_{chatbot['id']}"):
                            ChatbotBuilder.delete_chatbot(chatbot["id"])
                            st.success("Chatbot deleted")
                            st.rerun()

def edit_chatbot_ui(chatbot_id, is_vip):
    """Edit chatbot configuration (VIP only)"""
    if not is_vip:
        st.error("🔒 Editing requires VIP access. Upgrade to VIP to unlock this feature!")
        return
    
    chatbot = ChatbotBuilder.load_chatbot(chatbot_id)
    if not chatbot:
        st.error("Chatbot not found")
        return
    
    st.header(f"✏️ Edit: {chatbot['name']}")
    
    with st.form("edit_chatbot_form"):
        chatbot["name"] = st.text_input("Chatbot Name", value=chatbot["name"])
        chatbot["description"] = st.text_area("Description", value=chatbot["description"])
        chatbot["system_prompt"] = st.text_area("System Prompt", value=chatbot["system_prompt"], height=150)
        
        col1, col2 = st.columns(2)
        with col1:
            chatbot["model"] = st.selectbox(
                "AI Model",
                ["gpt-3.5-turbo", "gpt-4"],
                index=0 if chatbot["model"] == "gpt-3.5-turbo" else 1
            )
            chatbot["temperature"] = st.slider(
                "Temperature",
                0.0, 2.0,
                value=chatbot["temperature"],
                step=0.1
            )
        
        with col2:
            chatbot["max_tokens"] = st.slider(
                "Max Response Length",
                100, 2000,
                value=chatbot["max_tokens"],
                step=50
            )
        
        # VIP-only features
        st.divider()
        st.write("**🌟 VIP Features**")
        
        chatbot["is_active"] = st.checkbox("Activate Chatbot", value=chatbot["is_active"])
        
        st.write("**Behavior Rules** (Advanced)")
        if "behavior_rules" not in chatbot:
            chatbot["behavior_rules"] = []
        
        rules_text = st.text_area(
            "Add custom behavior rules (one per line)",
            value="\n".join(chatbot["behavior_rules"]),
            height=100
        )
        chatbot["behavior_rules"] = [r.strip() for r in rules_text.split("\n") if r.strip()]
        
        if st.form_submit_button("💾 Save Changes", use_container_width=True):
            ChatbotBuilder.save_chatbot(chatbot_id, chatbot)
            st.success("✅ Chatbot updated successfully!")
            st.session_state.edit_mode = False
            st.rerun()
