# VEDAS.AI

> Your Personal AI Assistant Inspired by JARVIS

VEDAS.AI is a modular, extensible, voice and text-controlled AI assistant designed to automate everyday tasks, enhance productivity, and serve as a personal desktop companion.

Built with Python and a plugin-based architecture, VEDAS.AI allows developers to easily add new capabilities while keeping the core system lightweight and maintainable.

---

## ✨ Features

### 🎙️ Voice & Text Interaction
- Speech-to-Text (STT)
- Text-to-Speech (TTS)
- Wake Word Detection
- Natural Language Command Processing

### 🔌 Plugin System
- Dynamic Plugin Loading
- Easy Plugin Development
- Isolated Plugin Execution
- Automatic Plugin Discovery

### 🧠 AI Assistant Capabilities
- General Question Answering
- Web Search Integration
- Translation Support
- Weather Information
- Time & Date Queries
- Calculator
- News Updates
- Movie & Music Search

### ⚙️ Automation
- Reminders
- Scheduled Tasks
- Application Launching
- Website Launching
- WhatsApp Automation
- Email Automation
- Media Playback

### 💾 Memory & Personalization
- User Preferences
- Conversation Context
- Persistent Memory
- Custom Assistant Configuration

### 🛠 Developer Friendly
- Class-Based Architecture
- Modular Design
- Easy Configuration
- Environment Variable Support
- Extensible API Structure

---

## 📂 Project Structure

```text
Vedas.ai/
├── ideas/
├── manager/
│   ├── __pycache__/
│   ├── __init__.py
│   ├── env_manager.py
│   ├── memory_manager.py
│   └── plugin_manager.py
├── plugins/
│   ├── __pycache__/
│   ├── __init__.py
│   ├── datetime_plugin.py
│   ├── greeting_plugin.py
│   └── system_info_plugin.py
├── runtime/
│   ├── lid.176.ftz
|   ├── output.mp3
|   ├── .env
│   └── vedas_voice_registry.json
├── utlis/
│   ├── __pycache__/
│   ├── __init__.py
│   ├── audio.py
│   ├── state.py
│   ├── text_normalizer.py
│   └── translator.py
├── README.md
├── .gitignore
└── main.py

```

---

## 🚀 Installation

### 1. Clone Repository

```bash
git clone https://github.com/yourusername/VEDAS.AI.git
cd VEDAS.AI
```

### 2. Create Virtual Environment

```bash
python -m venv .venv
```

### 3. Activate Virtual Environment

#### Windows

```bash
.venv\Scripts\activate
```

#### Linux/macOS

```bash
source .venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

Create a `.env` file in the project root.

```bash
cp runtime/.env.source runtime/.env
```

```env
OPENAI_API_KEY=your_key_here
OPEN_WEATHER_API_KEY=your_key_here

DEFAULT_CITY=Mumbai
DEFAULT_LANGUAGE=en

DEFAULT_LATITUDE=0.0
DEFAULT_LONGITUDE=0.0
```

---

## ▶️ Running VEDAS.AI

```bash
python main.py
```

---

## 🔌 Creating a Plugin

Example plugin:

```python
class Vedas:
    def __init__(self, config=None, **kwargs):
        self.name = ""  # Name of the plugin
        self.description = ""  # Description of the plugin
        self.parameters = ["input_data"]

        # Keywords to match from user query for execution
        self.keywords = []

        self.dependencies = []  # Dependencies for the plugin (e.g., external libraries, APIs)
        self.tool_map = {}
        self.config = config or {}
        self.enabled = True  # Flag to enable or disable the plugin
        self.last_query = None  # Store the last query for history and context, debugging and logging purpose

    def matches_query(self, query):
        self.last_query = query
        query_lower = query
        return any(keyword in query_lower for keyword in self.keywords)

    def run(self, input_data=None, **kwargs):
        query = (self.last_query or input_data or "").lower()

    def __str__(self):
        return str(self.keywords)
```

Place the file inside:

```text
plugins/
```

The Plugin Manager will automatically discover and load it.

---

## 🧩 Current Plugins

- Weather Plugin
- Date & Time Plugin
- YouTube Search Plugin
- YouTube Play Plugin
- Calculator Plugin
- Translation Plugin
- Web Search Plugin

---

## 🎯 Future Roadmap

### Phase 1
- [x] Plugin Manager
- [x] Weather Integration
- [ ] Voice Input
- [x] Text Commands

### Phase 2
- [ ] Wake Word Engine
- [ ] Advanced Memory System
- [ ] Local LLM Support
- [ ] GUI Dashboard

### Phase 3
- [ ] Multi-Agent System
- [ ] Home Automation
- [ ] Vision Capabilities
- [ ] Self-Hosted Workflow Engine
- [ ] Remote Access

---

## 🤝 Contributing

Contributions are welcome.

1. Fork the repository
2. Create a feature branch

```bash
git checkout -b feature/new-feature
```

3. Commit your changes

```bash
git commit -m "Added new feature"
```

4. Push to GitHub

```bash
git push origin feature/new-feature
```

5. Open a Pull Request

---

## 📜 License

This project is licensed under the MIT License.

---

## 👨‍💻 Author

**Onkar Joshi**

Building an open, extensible, JARVIS-inspired AI ecosystem focused on automation, productivity, and intelligent assistance.

---

## ⭐ Support

If you like this project:

- Star the repository
- Report bugs
- Suggest new features
- Contribute plugins

---

> "Technology should work for you, not the other way around."