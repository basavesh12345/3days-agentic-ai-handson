# 3-Day Hands-on Workshop on Agentic AI

> **A placement-focused, intensive hands-on workshop on Agentic AI for Computer Science & Engineering students and software engineers.**  
> **Conducted by:** Basavesh D. (Assistant Professor & AI Trainer, Dept. of CSE, Jyothy Institute of Technology, Bengaluru)

---

## 🚀 Overview

This repository contains the complete interactive courseware, slide handouts, reference guides, and production-ready code samples for the **3-Day Agentic AI Hands-on Workshop**. 

Topics covered include:
- **Python & LLM Integration** (LangChain, Ollama, OpenAI)
- **Retrieval-Augmented Generation (RAG)** with ChromaDB & Vector Stores
- **Stateful Agent Workflows** with LangGraph (Self-healing loops, Fact-checking, Multi-agent debate)
- **Autonomous Multi-Agent Software Teams** with CrewAI
- **Agent Interoperability** with Model Context Protocol (MCP) and Automation (n8n)

---

## 📂 Repository Structure

```text
├── index.html                     # Workshop overview, curriculum & outcomes portal
├── day1.html                      # Day 1: Foundations, Prompt Engineering & RAG
├── day2.html                      # Day 2: LangGraph & Multi-Agent Workflows
├── day3.html                      # Day 3: CrewAI Autonomous Software Companies
├── n8n.html                       # n8n AI Agent Automation Guide
├── style.css                      # Modern dark/light theme styling for the portal
├── content.css                    # Detailed content typography & styles
├── script.js                      # Interactive UI scripts (navigation, theme switcher)
├── *.pdf                          # Downloadable slide decks (index, day1, day2, day3)
├── college_info.txt               # Sample context document for RAG demonstrations
├── final_approved_post.md         # Sample generated multi-agent output
├── code_samples/
│   ├── requirements.txt           # Python dependencies
│   ├── day1_01_first_chatbot.py   # Simple conversational LLM agent
│   ├── day1_02_resume_reviewer.py # Structured resume evaluation agent
│   ├── day1_03_college_qa_rag.py  # End-to-end RAG system with ChromaDB
│   ├── college_qa.py              # CLI interactive college Q&A system
│   ├── day2_01_research_assistant.py # Tool-augmented research agent
│   ├── day2_02_doc_analysis_graph.py # LangGraph document processing pipeline
│   ├── day2_02_fact_checker.py    # Fact-checking verification loop
│   ├── day2_03_mcp_server_client.py  # Model Context Protocol (MCP) demo
│   ├── day2_03_self_healing_coder.py # Self-correcting code generation agent
│   ├── day2_04_debate_arena.py    # Multi-agent debate simulation
│   ├── day2_05_writer_critic_duo.py  # Iterative writer-critic feedback loop
│   └── day3_01_ai_software_company.py # Autonomous software engineering crew (CrewAI)
```

---

## 🛠️ Setup & Installation

### 1. Prerequisites
- **Python 3.10+** installed
- **Ollama** installed locally ([ollama.com](https://ollama.com)) for local open-source models:
  ```bash
  ollama pull llama3.2
  ollama pull nomic-embed-text
  ```

### 2. Environment Setup
```bash
# Clone the repository
git clone https://github.com/basavesh12345/3days-agentic-ai-handson.git
cd 3days-agentic-ai-handson

# Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r code_samples/requirements.txt
```

---

## 💻 Running the Code Samples

### Day 1: LLM & RAG
```bash
# 1. First Chatbot
python code_samples/day1_01_first_chatbot.py

# 2. Resume Reviewer
python code_samples/day1_02_resume_reviewer.py

# 3. College Q&A RAG System
python code_samples/day1_03_college_qa_rag.py
```

### Day 2: LangGraph & Agentic Patterns
```bash
# 1. Research Assistant with Tools
python code_samples/day2_01_research_assistant.py

# 2. Fact-Checking Agent
python code_samples/day2_02_fact_checker.py

# 3. Self-Healing Code Generator
python code_samples/day2_03_self_healing_coder.py

# 4. Multi-Agent Debate Arena
python code_samples/day2_04_debate_arena.py

# 5. Writer-Critic Duo
python code_samples/day2_05_writer_critic_duo.py
```

### Day 3: CrewAI Autonomous Software Team
```bash
python code_samples/day3_01_ai_software_company.py
```

---

## 🌐 Viewing the Courseware Offline
Open `index.html` directly in any web browser to view the curriculum, session breakdowns, interactive quizzes, and visual diagrams.

---

## 📜 License
This repository and materials are created for educational purposes for the Agentic AI Workshop.