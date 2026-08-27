# AI_insurance_risk_auditor
Here is a professional, developer-focused `README.md` designed to impress technical recruiters and engineering managers. It highlights your architectural decisions, the real-world impact of your code, and your forward-thinking approach to AI development.

---

# 🛡️ AI Insurance Policy Auditor

An autonomous, agentic AI system that audits health insurance policies in real-time. By leveraging **LangGraph** and **Google Gemini**, this application autonomously scrapes the web for official policy documents, evaluates clauses against a strict algorithmic rubric, and generates a standardized "Policy Health Score" (300-900).

---

## 🚨 The Problem

**Information Asymmetry in Healthcare Insurance.**
Modern health insurance policies are buried in 50+ pages of dense legalese. Consumers routinely buy policies based on top-line "Sum Insured" numbers, only to face devastating financial shocks during medical emergencies due to hidden **Room Rent Capping**, **Co-Payments**, **Disease Sub-limits**, and **Pre-Existing Disease (PED) Waiting Periods**.

## 💡 The Solution

This system replaces hours of manual document review with an autonomous agent.

1. **Intelligent Retrieval:** The agent uses tool-calling to execute targeted web searches across official insurance domains.
2. **Deterministic Grading:** It identifies hidden clauses and applies a deterministic penalty rubric (e.g., -100 points for 1% room rent capping).
3. **Structured Output:** It returns a mathematically justified Policy Health Score, detailed deduction logs, and verifiable source URLs.

## 🌍 Impact

* **For Common People (Consumers):** Democratizes financial literacy. It translates predatory legalese into a simple, credit-score-like number, saving families from unexpected out-of-pocket medical debts.
* **For the Industry (B2B / InsurTech):** Provides brokers, underwriters, and aggregators with an automated tool for competitor analysis, compliance verification, and standardized policy rating.

---

## 🛠️ Tech Stack & Architecture

This project is built with a decoupled, asynchronous architecture optimized for LLM latency.

* **AI & Agent Orchestration:** `LangGraph` (Stateful agent routing), `LangChain Core`, `Tavily Search API`
* **Large Language Model:** `Google Gemini 1.5 Flash` (Chosen for high-speed tool-calling and low token cost)
* **Backend Framework:** `FastAPI` (Async I/O for non-blocking LLM calls), `Pydantic V2` (Strict schema validation)
* **Frontend:** `Vanilla JavaScript`, `HTML5`, `Tailwind CSS` (CDN), `html2pdf.js` (Client-side reporting)
* **Testing & DevOps:** `Pytest`, `Docker`, `Docker Compose`

---

## 📂 Project Structure

```text
insurance_auditor/
├── app/                        # FastAPI Backend Application
│   ├── agent/                  # LangGraph Agent Core
│   │   ├── graph.py            # State graph definition (Nodes & Edges)
│   │   ├── nodes.py            # Reasoning and Tool-Execution logic
│   │   ├── prompts.py          # System instructions & scoring rubric
│   │   └── tools.py            # Tavily web scraping tool integration
│   ├── api/                    # API Routing
│   │   └── routes.py           # /api/v1/audit endpoint definition
│   ├── core/                   # Application Config
│   │   ├── config.py           # Pydantic Settings & Env Vars
│   │   └── exceptions.py       # Global error handling
│   ├── models/                 # Pydantic Schemas
│   │   ├── request.py          # Input validation
│   │   └── response.py         # Structured JSON output schema
│   └── main.py                 # FastAPI application factory & CORS
├── frontend/                   # Client-Side Interface
│   ├── css/
│   │   └── style.css           # Animations & responsive tweaks
│   ├── js/
│   │   └── app.js              # State management & API integration
│   └── index.html              # Tailwind-powered dashboard layout
├── tests/                      # Pytest Test Suite
│   ├── test_agent.py           # Unit tests for LangGraph routing
│   └── test_api.py             # Integration tests for FastAPI endpoints
├── .env.example                # Environment variable template
├── docker-compose.yml          # Multi-container orchestration
├── Dockerfile                  # Multi-stage production build
├── pytest.ini                  # Pytest configuration
└── requirements.txt            # Python dependencies

```

---

## 🚀 Getting Started

### 1. Local Development Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/insurance_auditor.git
cd insurance_auditor

# Create a virtual environment
python -m venv env
source env/bin/activate  # On Windows: .\env\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure Environment Variables
cp .env.example .env
# Edit .env and add your GOOGLE_API_KEY and TAVILY_API_KEY

```

### 2. Run Tests

The system uses `pytest` for unit and integration testing, mocking external LLM calls to ensure CI/CD reliability.

```bash
python -m pytest -v

```

### 3. Launch the Application

Start the Uvicorn server. The frontend is served statically on the root route.

```bash
uvicorn app.main:app --reload --port 8000

```

Navigate to `http://localhost:8000/` in your browser.

### 4. Docker Deployment (Production)

```bash
docker compose up -d --build

```

---

## 🔮 Future Roadmap: Human-in-the-Loop (HITL)

While the current agent operates fully autonomously, the next major architectural evolution involves implementing a **Human-in-the-Loop (HITL)** system utilizing LangGraph's `interrupt` nodes.

**Why HITL?**
Insurance policies occasionally contain highly ambiguous edge-case clauses (e.g., experimental treatments).

* **The Upgrade:** The system will pause execution when confidence in a clause deduction is low, routing the parsed data to a human insurance auditor's dashboard.
* **Continuous Learning:** The human expert will approve, reject, or modify the penalty. This human feedback will be logged and utilized for dynamic few-shot prompting in future runs, effectively allowing the AI to learn complex underwriting nuances over time without requiring fine-tuning.

---

*Designed & Engineered by Shivam Kumar*