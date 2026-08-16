import streamlit as st
from auth import AuthManager
from datetime import datetime, timedelta
import json
from pathlib import Path

# VIP subscriptions storage
VIP_FILE = Path(".streamlit/vip_subscriptions.json")

class VIPManager:
    """Manages VIP subscriptions and features"""
    
    VIP_FEATURES = {
        "edit_chatbots": "Edit existing chatbots",
        "advanced_settings": "Access advanced AI settings",
        "behavior_rules": "Create custom behavior rules",
        "analytics": "View detailed chat analytics",
        "export_data": "Export conversation data",
        "priority_support": "Priority customer support",
        "custom_branding": "Custom chatbot branding",
        "api_access": "REST API access"
    }
    
    @staticmethod
    def load_subscriptions():
        """Load VIP subscriptions"""
        if VIP_FILE.exists():
            with open(VIP_FILE, 'r') as f:
                return json.load(f)
        return {}
    
    @staticmethod
    def save_subscriptions(subscriptions):
        """Save VIP subscriptions"""
        with open(VIP_FILE, 'w') as f:
            json.dump(subscriptions, f, indent=2)
    
    @staticmethod
    def upgrade_to_vip(username, plan="monthly"):
        """Upgrade user to VIP"""
        AuthManager.promote_to_vip(username)
        
        subscriptions = VIPManager.load_subscriptions()
        subscriptions[username] = {
            "plan": plan,
            "started_at": datetime.now().isoformat(),
            "expires_at": (datetime.now() + timedelta(days=30)).isoformat() if plan == "monthly" else None,
            "features_enabled": list(VIPManager.VIP_FEATURES.keys())
        }
        VIPManager.save_subscriptions(subscriptions)
        return True
    
    @staticmethod
    def check_vip_feature(username, feature):
        """Check if user has access to a VIP feature"""
        if not AuthManager.is_vip_user(username):
            return False
        
        subscriptions = VIPManager.load_subscriptions()
        if username not in subscriptions:
            return False
        
        sub = subscriptions[username]
        if feature not in sub.get("features_enabled", []):
            return False
        
        # Check if subscription expired
        if sub.get("expires_at"):
            expires = datetime.fromisoformat(sub["expires_at"])
            if datetime.now() > expires:
                return False
        
        return True
    
    @staticmethod
    def get_user_vip_status(username):
        """Get VIP status for user"""
        if not AuthManager.is_vip_user(username):
            return {"is_vip": False, "plan": None}
        
        subscriptions = VIPManager.load_subscriptions()
        if username in subscriptions:
            return {"is_vip": True, **subscriptions[username]}
        
        return {"is_vip": False, "plan": None}

def vip_page():
    """Display VIP information and upgrade page"""
    st.title("🌟 Upgrade to VIP")
    
    current_status = VIPManager.get_user_vip_status(st.session_state.current_user)
    
    if current_status["is_vip"]:
        st.success(f"✅ You are a VIP member! Plan: {current_status['plan']}")
        
        st.subheader("Your VIP Features:")
        features = current_status.get("features_enabled", [])
        for feature_key in features:
            st.write(f"✨ {VIPManager.VIP_FEATURES.get(feature_key, feature_key)}")
        
        if current_status.get("expires_at"):
            st.info(f"Your subscription expires on: {current_status['expires_at'][:10]}")
    
    else:
        st.write("Unlock powerful features to customize and manage your chatbots!")
        
        st.divider()
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📱 Monthly")
            st.write("**$9.99/month**")
            st.write("\n".join([f"✓ {desc}" for desc in VIPManager.VIP_FEATURES.values()]))
            if st.button("Upgrade to Monthly", key="monthly", use_container_width=True):
                VIPManager.upgrade_to_vip(st.session_state.current_user, "monthly")
                st.session_state.is_vip = True
                st.success("🎉 Welcome to VIP!")
                st.rerun()
        
        with col2:
            st.subheader("🎁 Annual (Save 20%)")
            st.write("**$95.88/year**")
            st.write("\n".join([f"✓ {desc}" for desc in VIPManager.VIP_FEATURES.values()]))
            if st.button("Upgrade to Annual", key="annual", use_container_width=True):
                VIPManager.upgrade_to_vip(st.session_state.current_user, "annual")
                st.session_state.is_vip = True
                st.success("🎉 Welcome to VIP!")
                st.rerun()
        
        st.divider()
        st.subheader("Free Features")
        st.write("✓ Create unlimited chatbots")
        st.write("✓ Use GPT-3.5 and GPT-4 models")
        st.write("✓ Basic chat history")
