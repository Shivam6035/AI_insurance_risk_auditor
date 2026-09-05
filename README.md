# 🛡️ AI Insurance Risk Auditor

An **AI-powered insurance policy auditing and comparison platform** that uses **LLMs, agentic workflows, structured reasoning, and real-time policy guideline search** to help identify coverage gaps, exclusions, inconsistencies, and potential risk areas in insurance policies.

The system combines **Google Gemini, LangGraph, Tavily Search, FastAPI, Pydantic, and Railway** to transform lengthy insurance policy text into structured and actionable risk insights.

---

## 🎯 Business Problem

Insurance policies are often long, complex, and filled with technical clauses, exclusions, deductibles, conditions, and coverage limitations.

For customers, brokers, and underwriting teams, manually reviewing these documents can be:

* Time-consuming
* Inconsistent across reviewers
* Difficult to compare across policies
* Prone to overlooked exclusions or hidden conditions
* Dependent on domain expertise
* Hard to translate into clear business decisions

A user may know the premium of a policy but still struggle to answer questions such as:

> What risks are actually covered?

> Which exclusions could create financial exposure?

> Are there unusual clauses that need attention?

> Which of two policies provides stronger protection?

> Does a policy align with commonly available insurance guidelines?

The **AI Insurance Risk Auditor** is designed to reduce this information gap.

---

# 💡 Proposed Solution

The platform converts raw insurance policy information into a structured AI-driven audit.

Instead of relying on a single LLM prompt, the system uses an **agentic workflow** that can reason about a policy, determine when external information is required, call specialized tools, and generate a structured final assessment.

### Core workflow

1. User submits insurance policy information.
2. FastAPI validates and sends the request to the AI workflow.
3. Gemini analyses the policy context.
4. The agent determines whether additional policy/regulatory information is required.
5. Tavily-powered search retrieves relevant insurance guidelines.
6. Search results are returned to the agent.
7. Gemini combines policy data and external context.
8. The result is validated against a structured Pydantic response schema.
9. The frontend displays the final risk assessment.

The platform can also support **policy-to-policy comparison**, helping users identify differences in coverage, exclusions, benefits, and risk exposure.

---
# System Architecture
<img width="482" height="634" alt="image" src="https://github.com/user-attachments/assets/037be730-5f56-4096-81d1-bfb525b03c19" />


# 🤖 Agentic Workflow

The AI layer follows a **reason → act → observe → respond** architecture.

```text
                   ┌─────────────────────┐
                   │    User Request     │
                   └──────────┬──────────┘
                              │
                              ▼
                   ┌─────────────────────┐
                   │   Gemini Reasoning  │
                   │       Agent         │
                   └──────────┬──────────┘
                              │
                       Tool required?
                         /         \
                       YES          NO
                       /             \
                      ▼               ▼
           ┌──────────────────┐   Final Analysis
           │ Insurance Search │         │
           │      Tool         │         │
           └────────┬─────────┘         │
                    │                   │
                    ▼                   │
             Search Guidelines          │
                    │                   │
                    └──────► Gemini ◄───┘
                              │
                              ▼
                    Structured Response
                              │
                              ▼
                     Pydantic Validation
                              │
                              ▼
                       Audit Results
```

This architecture is more flexible than a traditional single-prompt LLM application because the model can dynamically decide when it needs additional context.

---

# 🔍 Key Features

### AI-Powered Policy Auditing

Analyses insurance policy information and converts complex policy language into structured findings.

### Agentic Reasoning

LangGraph orchestrates multi-step reasoning and tool execution rather than relying on a single LLM call.

### Real-Time Guideline Search

The agent can use **Tavily Search** to retrieve additional policy-related information when its internal context is insufficient.

### Structured AI Responses

LLM output is validated using **Pydantic schemas**, providing predictable responses that can be safely consumed by APIs and frontend applications.

### Policy Comparison

Allows policies to be evaluated side-by-side to highlight differences in areas such as:

* Coverage
* Exclusions
* Conditions
* Benefits
* Potential risk exposure

### REST API

FastAPI exposes the AI workflow through production-friendly API endpoints.

### Web Interface

A lightweight frontend allows users to interact with the auditing and comparison workflows without directly calling APIs.

### Cloud Deployment

The application is containerized using Docker and deployed on **Railway**, with:

* Health checks
* Environment-based secrets
* Public networking
* Automated deployments from GitHub

---

# 🛠️ Technology Stack

| Layer                            | Technology                           |
| -------------------------------- | ------------------------------------ |
| **Programming Language**         | Python                               |
| **Backend API**                  | FastAPI                              |
| **LLM**                          | Google Gemini                        |
| **Agent Orchestration**          | LangGraph                            |
| **LLM Integration**              | LangChain / `langchain-google-genai` |
| **External Search**              | Tavily                               |
| **Data Validation**              | Pydantic                             |
| **Frontend**                     | HTML, CSS, JavaScript                |
| **Configuration**                | Pydantic Settings, python-dotenv     |
| **Application Server**           | Uvicorn                              |
| **Containerization**             | Docker                               |
| **Deployment**                   | Railway                              |
| **Version Control / CI Trigger** | GitHub                               |

---

# 📁 Project Structure

```text
AI_insurance_risk_auditor/
│
├── app/
│   │
│   ├── main.py
│   │   └── FastAPI application entry point
│   │
│   ├── api/
│   │   └── routes.py
│   │       └── Audit and comparison API endpoints
│   │
│   ├── agent/
│   │   ├── graph.py
│   │   │   └── LangGraph workflow definition
│   │   │
│   │   ├── nodes.py
│   │   │   └── Gemini reasoning and tool execution nodes
│   │   │
│   │   ├── tools.py
│   │   │   └── External insurance search tools
│   │   │
│   │   └── prompts.py
│   │       └── Agent system prompts
│   │
│   ├── models/
│   │   └── response.py
│   │       └── Structured Pydantic response models
│   │
│   └── core/
│       ├── config.py
│       │   └── Environment and application configuration
│       │
│       └── exceptions.py
│           └── Centralized exception handling
│
├── frontend/
│   ├── index.html
│   ├── compare.html
│   │
│   ├── css/
│   │   └── Application styling
│   │
│   └── js/
│       └── Frontend API interaction
│
├── requirements.txt
│   └── Python dependencies
│
├── Dockerfile
│   └── Production container configuration
│
├── Procfile
│   └── Application startup configuration
│
├── .env.example
│   └── Environment variable template
│
└── README.md
```

---

# ⚙️ How the Agent Works

A simplified execution flow is:

```python
User Policy
    ↓
FastAPI
    ↓
LangGraph State
    ↓
Gemini Agent
    ↓
Tool Call?
    ├── Yes → Tavily Search → ToolMessage → Gemini
    └── No
           ↓
Structured AuditResponse
           ↓
Pydantic Validation
           ↓
API Response
```

One important engineering decision is separating **tool-selection responses** from **final structured responses**.

During tool calling, an LLM response may intentionally contain no textual content because it is requesting a tool execution. The workflow therefore waits until tool execution is complete before producing and validating the final audit result.

This prevents intermediate model messages from being incorrectly treated as final JSON responses.

---

# 🚀 Running Locally

### 1. Clone the repository

```bash
git clone https://github.com/Shivam6035/AI_insurance_risk_auditor.git

cd AI_insurance_risk_auditor
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it and install dependencies:

```bash
pip install -r requirements.txt
```

### 3. Configure environment variables

Create a `.env` file:

```env
GOOGLE_API_KEY=your_google_api_key
TAVILY_API_KEY=your_tavily_api_key
```

Never commit real API credentials to GitHub.

### 4. Start the application

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8080
```

Open:

```text
http://localhost:8080
```

Health check:

```text
http://localhost:8080/health
```

---

# ☁️ Deployment

The project is containerized using Docker and deployed on Railway.

Production flow:

```text
GitHub main branch
       │
       ▼
Automatic Railway Build
       │
       ▼
Docker Image
       │
       ▼
FastAPI + Uvicorn
       │
       ▼
Health Check (/health)
       │
       ▼
Public Application
```

The `/health` endpoint allows the deployment platform to confirm that the API has successfully started before routing user traffic to it.

---

# 📈 Business Value

The larger opportunity behind this project is not simply summarizing insurance documents.

An intelligent policy-auditing system could become a **decision-support layer** for:

* Insurance customers
* Brokers
* Underwriters
* Risk analysts
* Claims teams
* Compliance teams

By converting unstructured policy documents into structured risk information, such a system could help reduce review time, improve consistency, and surface clauses that deserve human attention earlier in the decision-making process.

The system is intended to **augment professional review rather than replace underwriting, compliance, or legal judgment**.

---

# 🔮 Future Scope

Several extensions could turn the current system into a more complete insurance intelligence platform.

**Document Intelligence** — Direct PDF policy uploads with OCR/document parsing and clause-level extraction.

**Retrieval-Augmented Generation** — Build a verified insurance knowledge base using policy documents, regulatory material, and insurer guidelines instead of relying only on external search.

**Explainable Risk Scoring** — Generate transparent scores with clause-level evidence explaining why each risk was identified.

**Multi-Policy Benchmarking** — Compare multiple policies and rank them based on coverage quality, exclusions, premium, and user-specific requirements.

**Human-in-the-Loop Review** — Allow underwriters or analysts to approve, reject, or modify AI findings before finalization.

**Audit History & Monitoring** — Persist previous audits and track changes across policy versions.

**Enterprise Integration** — Integrate the auditing engine with underwriting, policy administration, CRM, or claims platforms through APIs.

---

# 🎯 Engineering Takeaways

This project demonstrates practical experience across:

**Generative AI + Agentic Systems + Backend Engineering + API Design + Structured Outputs + Tool Calling + Cloud Deployment + Insurance Domain Applications**

Rather than building a simple chatbot, the project focuses on creating an **end-to-end AI workflow capable of reasoning, using external tools, validating its output, and exposing the result through a deployable production API.**

---

## 👨‍💻 Author

**Shivam Kumar**

Built as an end-to-end applied AI project exploring how **agentic LLM systems can improve insurance policy analysis and risk decision support**.
