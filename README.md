# 🔬 AI Research Lab Simulator

[![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![LangGraph](https://img.shields.io/badge/LangGraph-0.0.62-green.svg)](https://github.com/langchain-ai/langgraph)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.29.0-red.svg)](https://streamlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Multi-agent LLM research pipeline using **LangGraph**, **LangChain**, **Gemini 2.0 Flash**, and **Groq Mixtral**. Autonomous research generation through collaborative AI agents with iterative refinement.

![Architecture](https://img.shields.io/badge/Architecture-Multi--Agent-purple)
![LLMs](https://img.shields.io/badge/LLMs-Gemini%20%2B%20Groq-orange)

---

## 🎯 Features

- **🤖 5 Specialized AI Agents**: Researcher, Reviewer, Editor, Fact Checker, Citation Validator
- **🔄 LangGraph Workflow**: StateGraph with conditional routing and iterative refinement
- **🚀 Multi-LLM Integration**: Gemini 2.0 Flash + Groq Mixtral working in tandem
- **📊 Quality Metrics**: 4-dimensional scoring (accuracy, coherence, completeness, depth)
- **💬 3 User Interfaces**: Research Dashboard, Interactive Chat, Direct Agent Chat
- **⚡ Fast Mode**: Quick results in ~15-20 seconds
- **📤 Multiple Export Formats**: TXT, Full Report, JSON
- **🔍 Real-time Streaming**: Live agent responses and progress tracking

---

## 📋 Table of Contents

- [Quick Start](#-quick-start)
- [Architecture](#-architecture)
- [Installation](#-installation)
- [Usage](#-usage)
- [Project Structure](#-project-structure)
- [Configuration](#-configuration)
- [Interfaces](#-interfaces)
- [API Keys](#-api-keys)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🚀 Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/ai-research-lab.git
cd ai-research-lab

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set up environment variables
cp .env.example .env
# Edit .env and add your API keys

# 4. Run the application
streamlit run ui/app.py
```

---

## 🏗️ Architecture

### Multi-Agent System

```
┌─────────────────────────────────────────────────────────────┐
│                    LANGGRAPH WORKFLOW                       │
└─────────────────────────────────────────────────────────────┘

    START → Research → Review → Fact Check → Citation → Editor
                         ↑                                  ↓
                         └──────── (Loop if needed) ────────┘
                                        ↓
                                    Finalize → END
```

### Agent Roles

| Agent | Model | Role | Output |
|-------|-------|------|--------|
| 🔍 **Researcher** | Gemini 2.0 Flash | Content Generation | Research text |
| 📝 **Reviewer** | Groq Mixtral | Quality Evaluation | Feedback + Score |
| ✏️ **Editor** | Gemini 2.0 Flash | Content Refinement | Improved text |
| ✅ **Fact Checker** | Groq Mixtral | Claim Verification | Verified/Flagged |
| 📚 **Citation Validator** | Gemini 2.0 Flash | Source Validation | Citation analysis |

---

## 📦 Installation

### Prerequisites

- Python 3.13 or higher
- pip package manager
- Google Gemini API key
- Groq API key

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Dependencies

- `streamlit==1.29.0` - Web interface
- `langgraph==0.0.62` - Workflow orchestration
- `langchain==0.1.0` - LLM framework
- `langchain-core==0.1.10` - Core components
- `langchain-google-genai==1.0.1` - Gemini integration
- `langchain-groq==0.1.3` - Groq integration
- `python-dotenv==1.0.0` - Environment variables

---

## 🎮 Usage

### 1. Research Dashboard (Main Interface)

Generate research documents through automated multi-agent collaboration.

```bash
streamlit run ui/app.py
```

**Features:**
- Real-time progress tracking
- Agent dialogue visualization
- Quality metrics display
- Workflow controls (Start/Stop/Pause)
- Parameter adjustment
- Export options

### 2. Research Chat (Interactive Q&A)

Chat with AI agents about generated research documents.

```bash
streamlit run ui/research_chat.py
```

**Features:**
- Generate or upload research
- Context-aware responses
- Quick actions (Summarize, Key Points, etc.)
- Switch between agent perspectives

### 3. Agent Chat (Direct Interaction)

Direct conversation with individual agents.

```bash
streamlit run ui/chat.py
```

**Features:**
- Select any agent
- General-purpose chat
- No research context required

---

## 📁 Project Structure

```
ai-research-lab/
├── agents/                  # Multi-agent system
│   ├── base_agent.py       # Base agent class
│   ├── researcher.py       # Content generation
│   ├── reviewer.py         # Quality evaluation
│   ├── editor.py           # Content refinement
│   ├── fact_checker.py     # Claim verification
│   ├── citation_validator.py # Source validation
│   └── agent_factory.py    # Agent creation
│
├── config/                  # Configuration
│   ├── settings.py         # Workflow parameters
│   ├── models.py           # Model factory
│   └── speed_settings.py   # Performance tuning
│
├── tools/                   # Research tools
│   ├── search.py           # Knowledge retrieval
│   ├── citation.py         # Citation tracking
│   ├── quality_metrics.py  # Quality scoring
│   ├── bias_detector.py    # Bias detection
│   ├── fact_validator.py   # Fact validation
│   └── tool_manager.py     # Tool interface
│
├── workflow/                # LangGraph workflow
│   ├── state.py            # State schema
│   ├── nodes.py            # Workflow nodes
│   ├── graph.py            # Graph creation
│   ├── runner.py           # Workflow execution
│   └── visualizer.py       # Graph visualization
│
├── ui/                      # Streamlit interfaces
│   ├── app.py              # Research dashboard
│   ├── research_chat.py    # Interactive Q&A
│   └── chat.py             # Direct agent chat
│
├── .env.example             # Environment template
├── .gitignore              # Git ignore rules
├── requirements.txt         # Dependencies
├── README.md               # This file
└── PROJECT_REPORT.html     # Detailed documentation
```

---

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the root directory:

```env
GOOGLE_API_KEY=your_gemini_api_key_here
GROQ_API_KEY=your_groq_api_key_here
```

### Workflow Parameters

Edit `config/settings.py`:

```python
MAX_ITERATIONS = 2              # Maximum refinement cycles
CONVERGENCE_THRESHOLD = 0.7     # Quality score threshold
TEMPERATURE = 0.9               # LLM temperature
```

### Model Configuration

Edit `config/models.py` to change models:

```python
GEMINI_MODEL = "gemini-2.0-flash-exp"
GROQ_MODEL = "mixtral-8x7b-32768"
```

---

## 🖥️ Interfaces

### Research Dashboard

**Purpose:** Automated research document generation

**Access:** `streamlit run ui/app.py`

**Workflow:**
1. Enter research topic
2. Configure parameters (optional)
3. Click "Start Research"
4. Monitor real-time progress
5. Download results

### Research Chat

**Purpose:** Interactive Q&A about research

**Access:** `streamlit run ui/research_chat.py`

**Workflow:**
1. Generate or upload research
2. Select an agent
3. Ask questions
4. Get context-aware responses

**Example Questions:**
- "Summarize the key findings"
- "What are the main arguments?"
- "Are there any gaps in this research?"
- "Suggest improvements"

### Agent Chat

**Purpose:** General conversation with agents

**Access:** `streamlit run ui/chat.py`

**Workflow:**
1. Select an agent
2. Start chatting
3. No research context needed

---

## 🔑 API Keys

### Get Gemini API Key

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with Google account
3. Create API key
4. Copy to `.env` file

### Get Groq API Key

1. Visit [Groq Console](https://console.groq.com/)
2. Sign up/Sign in
3. Navigate to API Keys
4. Create new key
5. Copy to `.env` file

---

## 📊 Quality Metrics

The system evaluates research using 4 dimensions:

1. **Accuracy (35%)**: Verified vs flagged claims
2. **Coherence (25%)**: Sentence structure + vocabulary
3. **Completeness (25%)**: Required sections coverage
4. **Depth (15%)**: Content length and detail

**Overall Score:** Weighted combination of all metrics

---

## ⚡ Performance

### Speed Optimizations

- **Reduced Iterations:** 2 instead of 5 (60% faster)
- **Truncated Prompts:** Max 500 chars context
- **Fast Mode:** 1 iteration, 0.6 threshold (~15-20s)
- **Streaming:** Real-time response display

### Typical Execution Times

- **Normal Mode:** ~20-30 seconds
- **Fast Mode:** ~15-20 seconds
- **Per Agent:** ~3-5 seconds

---

## 🔄 Workflow

### LangGraph StateGraph

```python
Research → Review → Fact Check → Citation → Editor
              ↑                                ↓
              └────── (Loop if needed) ────────┘
```

### Convergence Criteria

Workflow exits when:
- Quality score ≥ threshold (0.7)
- OR iterations ≥ max (2)

---

## 📤 Export Formats

1. **Research Document (.txt)** - Clean output
2. **Full Report (.txt)** - Document + metadata + logs
3. **JSON Data (.json)** - Complete structured export
4. **Process Logs (.txt)** - Timestamped execution

---

## 🛠️ Development

### Run Tests

```bash
python test_imports.py      # Test module imports
python test_quality_metrics.py  # Test quality scoring
python test_speed.py        # Test pipeline speed
```

### Visualize Workflow

```bash
python visualize_graph.py   # Display LangGraph workflow
```

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **LangGraph** - Workflow orchestration framework
- **LangChain** - LLM application framework
- **Google Gemini** - Advanced language model
- **Groq** - Fast inference platform
- **Streamlit** - Web interface framework

---

## 📞 Support

For issues, questions, or suggestions:

- Open an [Issue](https://github.com/yourusername/ai-research-lab/issues)
- Check [PROJECT_REPORT.html](PROJECT_REPORT.html) for detailed documentation
- Review the code comments and docstrings

---

## 🚀 Future Enhancements

- [ ] RAG implementation with vector databases
- [ ] Web search integration
- [ ] Multi-language support
- [ ] Parallel agent execution
- [ ] Custom workflow builder
- [ ] REST API
- [ ] Mobile app
- [ ] Fine-tuned models

---

## 📈 Version History

- **v1.1.0** - Added Research Chat interface
- **v1.0.0** - Initial release with multi-agent workflow

---

## 🌟 Star History

If you find this project useful, please consider giving it a star ⭐

---

**Built with ❤️ using LangGraph, LangChain, Gemini, and Groq**
