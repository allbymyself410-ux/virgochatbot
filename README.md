# 🤖 Virgo Chatbot - No-Code AI Agent Builder

A powerful no-code platform for building, customizing, and managing AI chatbots without writing any code. Perfect for businesses, creators, and anyone who wants to deploy intelligent conversational AI.

## ✨ Features

### 🎯 Core Features (Free)
- **No-Code Builder**: Create chatbots through an intuitive visual interface
- **Multiple AI Models**: Choose between GPT-3.5 Turbo and GPT-4
- **Custom Personalities**: Define system prompts to customize chatbot behavior
- **Real-time Chat**: Test your chatbots immediately
- **Unlimited Chatbots**: Create as many chatbots as you want
- **Chat History**: Automatic saving of conversations

### 🌟 VIP Features (Premium)
- **Full Editing**: Edit and refine chatbots after creation
- **Advanced Settings**: Fine-tune temperature, token limits, and more
- **Behavior Rules**: Add custom rules to govern chatbot responses
- **Chat Analytics**: View detailed conversation analytics
- **Export Data**: Download your chat histories and configurations
- **Priority Support**: Get help when you need it
- **Custom Branding**: Add your own branding to chatbots
- **API Access**: Integrate chatbots via REST API

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- OpenAI API key ([Get one here](https://platform.openai.com/account/api-keys))

### Installation

1. Clone the repository:
```bash
git clone https://github.com/allbymyself410-ux/virgochatbot.git
cd virgochatbot
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
streamlit run streamlit_app.py
```

4. Open your browser to `http://localhost:8501`

## 📝 How to Use

### Creating a Chatbot
1. Log in or register for an account
2. Click "Build Chatbot" from the navigation menu
3. Fill in the chatbot details:
   - **Name**: Give your chatbot a memorable name
   - **Description**: Describe what it does
   - **System Prompt**: Define the chatbot's personality and behavior
   - **AI Model**: Choose GPT-3.5 Turbo or GPT-4
   - **Temperature**: Adjust creativity (0 = focused, 2 = creative)
   - **Max Response Length**: Set response length limits
4. Click "Create Chatbot"

### Testing Your Chatbot
1. From "Manage Existing", select a chatbot
2. Enter your OpenAI API key
3. Chat with your chatbot in real-time
4. Click "Clear Chat" to reset, "Save History" to store conversations

### Editing (VIP Only)
1. Upgrade to VIP membership
2. Click the "Edit" button on any of your chatbots
3. Modify settings, system prompts, behavior rules, etc.
4. Save your changes

## 🔐 Authentication & VIP Access

### User Accounts
- Create a free account with username and password
- All chatbots are private to your account
- Login from any device

### VIP Membership
- **Monthly**: $9.99/month
- **Annual**: $95.88/year (save 20%)
- Unlock editing, advanced settings, analytics, and more
- Cancel anytime

## 📁 Project Structure

```
vigrochatbot/
├── streamlit_app.py        # Main application entry point
├── auth.py                 # User authentication and management
├── chatbot_builder.py      # No-code chatbot builder interface
├── chatbot_runner.py       # Chatbot execution engine
├── vip_manager.py          # VIP subscription management
├── requirements.txt        # Python dependencies
├── .streamlit/
│   ├── config.toml        # Streamlit configuration
│   ├── users.json         # User database
│   ├── vip_subscriptions.json  # VIP subscription data
│   ├── chatbots/          # Chatbot configurations
│   └── chat_history/      # Saved chat conversations
└── README.md              # This file
```

## 🛠️ System Prompt Examples

### Customer Support Bot
```
You are a friendly and helpful customer service representative. 
Your goal is to resolve customer issues quickly and professionally. 
Always be empathetic, ask clarifying questions when needed, and provide clear solutions.
```

### Personal Tutor
```
You are an experienced, patient tutor specializing in {subject}. 
Explain concepts clearly, provide examples, and ask questions to check understanding. 
Break down complex topics into manageable parts.
```

### Sales Assistant
```
You are an enthusiastic sales representative for {product/service}. 
Highlight key benefits, answer questions, and help customers make informed decisions. 
Be honest about limitations and always put customer needs first.
```

## 🔒 Security & Privacy

- User passwords are hashed with SHA-256
- API keys are never stored (entered per session)
- Chat histories are stored locally
- All data is encrypted at rest
- Users have full control over their chatbots and data

## 🐛 Troubleshooting

### "Invalid API Key" Error
- Verify your OpenAI API key is correct
- Check that your API key has sufficient credits
- Ensure the key is active (not expired or revoked)

### Chatbot Not Responding
- Check your internet connection
- Verify OpenAI service status
- Ensure your API key has sufficient quota
- Check the error message for specific issues

### Chat History Not Saving
- Ensure the `.streamlit` directory has write permissions
- Check disk space availability
- Try clearing browser cache and restarting

## 📞 Support

For issues, questions, or feature requests:
- GitHub Issues: [Report a bug](https://github.com/allbymyself410-ux/virgochatbot/issues)
- Email: support@virgochatbot.com
- VIP users get priority email support

## 📄 License

This project is licensed under the Apache License 2.0 - see [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 🎯 Roadmap

- [ ] Cloud deployment (AWS, GCP, Azure)
- [ ] Team collaboration features
- [ ] Multi-language support
- [ ] Voice integration
- [ ] Advanced NLP features
- [ ] Webhook integrations
- [ ] Rate limiting and quotas
- [ ] Advanced analytics dashboard

## 📈 Stats

- ⚡ Zero setup time
- 🚀 Deploy in minutes
- 💰 Free tier + affordable VIP
- 🌍 Works anywhere with internet
- 🔐 Enterprise-grade security

---

Built with ❤️ using Streamlit and OpenAI
