# 🎯 AI Writer Crew - Modern Web Interface

A beautiful, modern chat interface for your AI Writer Crew project with real-time communication, agent management, and RAG integration.

## ✨ Features

### 🎨 Modern Design
- **Dark theme** with beautiful gradients and animations
- **Responsive layout** that works on desktop, tablet, and mobile
- **Smooth animations** and interactive elements
- **Professional typography** with Inter font
- **Toast notifications** for user feedback

### 🤖 Agent Management
- **Visual agent controls** with individual enable/disable toggles
- **Real-time agent status** indicators
- **Specialized agent responses** from your crew
- **Agent avatars and descriptions** for easy identification

### 💬 Advanced Chat Features
- **Real-time messaging** with WebSocket support
- **Typing indicators** during AI processing
- **Message history** with persistent storage
- **Export functionality** for chat sessions
- **Keyboard shortcuts** for power users

### 🧠 LLM & RAG Integration
- **Local LLM support** with llama.cpp integration
- **RAG context enhancement** from your document database
- **Configurable settings** (temperature, tokens, context chunks)
- **System status monitoring** with health checks

### 📱 User Experience
- **Auto-save settings** and chat history
- **Drag-and-drop** file uploads (planned)
- **Search functionality** in chat history
- **Multiple export formats** (JSON, Markdown)

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Launch the Interface

**On Windows:**
```bash
start_web_interface.bat
```

**On Linux/Mac:**
```bash
python launch_web_interface.py
```

### 3. Access the Interface
The launcher will automatically:
- Start the FastAPI backend server
- Open your browser to `http://localhost:8000`
- Show system status and available agents

## 🛠️ Configuration

### Local LLM Setup
1. Download a GGUF model (e.g., from Hugging Face)
2. Place it at: `llm_local/models/model.gguf`
3. Restart the interface

### RAG Documents
1. Add your reference documents to `data/reference_docs/`
2. Supported formats: PDF, DOCX, TXT, MD
3. Documents will be automatically processed

### Agent Configuration
- Enable/disable agents using the sidebar toggles
- Agents are loaded dynamically from your project
- Each agent provides specialized writing assistance

## 🎛️ Interface Controls

### Sidebar Controls
- **Agent Toggles**: Enable/disable individual writing agents
- **RAG Settings**: Adjust temperature, tokens, and context
- **System Status**: Real-time status indicators

### Chat Controls
- **Send Message**: `Enter` key or send button
- **Multi-line**: `Shift + Enter` for new lines
- **Clear Chat**: `Ctrl/Cmd + L`
- **Export Chat**: `Ctrl/Cmd + S`
- **Focus Input**: `Ctrl/Cmd + K`

### Header Actions
- **Clear Chat**: Remove all messages
- **Export**: Download chat as JSON
- **Settings**: Quick access to configuration

## 🔧 Technical Architecture

### Backend (FastAPI)
- **RESTful API** for agent communication
- **WebSocket support** for real-time features
- **Async processing** for better performance
- **Error handling** with graceful fallbacks

### Frontend (Vanilla JS)
- **Modern ES6+** JavaScript
- **No framework dependencies** for fast loading
- **Responsive CSS Grid** layout
- **Local storage** for persistence

### Integration Points
- **Agent Manager**: Interfaces with your existing agents
- **RAG Manager**: Integrates with your document database
- **LLM Manager**: Supports local llama.cpp models
- **Settings**: Uses your existing configuration system

## 📊 API Endpoints

### Core Endpoints
- `GET /api/status` - System health and status
- `POST /api/chat` - Process chat messages
- `GET /api/agents` - Available agents list
- `POST /api/rag/query` - Direct RAG queries

### WebSocket
- `WS /ws/chat` - Real-time chat communication

## 🎨 Customization

### Themes
The interface uses CSS custom properties for easy theming:

```css
:root {
  --primary-bg: #1e1e2e;
  --secondary-bg: #313244;
  --accent-color: #cba6f7;
  --text-color: #cdd6f4;
  --success-color: #a6e3a1;
  --warning-color: #f9e2af;
  --error-color: #f38ba8;
}
```

### Agent Icons
Customize agent avatars by modifying the `getAgentAvatar()` function in the JavaScript.

### Layout
The interface uses CSS Grid for responsive layout. Modify the grid template in `.container` for different layouts.

## 🔒 Security

### Local-First
- No data sent to external services
- Local LLM processing
- Client-side storage only
- CORS protection enabled

### Development Mode
- Auto-reload enabled for development
- Debug information available
- Error logging and monitoring

## 🐛 Troubleshooting

### Common Issues

**Server won't start:**
- Check if port 8000 is available
- Verify Python and pip are working
- Install missing dependencies

**Agents not loading:**
- Check agent_manager.py is working
- Verify agents are properly initialized
- Check console for JavaScript errors

**RAG not working:**
- Ensure documents exist in reference_docs
- Check ChromaDB installation
- Verify vector store is initialized

**LLM not responding:**
- Check if model.gguf exists
- Verify llama-cpp-python installation
- Check model compatibility

### Debug Mode
Add `?debug=true` to the URL for additional debugging information.

### Logs
Check the console output for detailed error messages and system status.

## 🚧 Roadmap

### Planned Features
- **File upload interface** for documents
- **Voice input/output** support
- **Collaborative editing** with multiple users
- **Plugin system** for custom agents
- **Advanced export formats** (PDF, EPUB)
- **Performance analytics** dashboard
- **Mobile app** companion

### Integrations
- **Scrivener** import/export
- **Google Docs** synchronization
- **GitHub** version control
- **Discord** notifications
- **Slack** integration

## 📝 License

This project is part of the AI Writer Crew system and follows the same MIT license.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

### Development Setup
```bash
# Clone the repository
git clone <your-repo-url>

# Install dependencies
pip install -r requirements.txt

# Run in development mode
python launch_web_interface.py
```

## 📞 Support

- **Issues**: Use GitHub Issues for bug reports
- **Discussions**: GitHub Discussions for questions
- **Documentation**: Check the wiki for detailed guides

---

**Made with ❤️ for writers by writers**

Transform your writing process with the power of specialized AI agents and a beautiful, modern interface.
