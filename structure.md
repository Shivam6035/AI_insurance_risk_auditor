insurance_auditor/
├── .github/
│   └── workflows/
│       └── main.yml              # CI/CD pipeline for testing and deployment
├── app/
│   ├── __init__.py
│   ├── main.py                   # FastAPI application entry point
│   ├── api/                      # API routing and endpoints
│   │   ├── __init__.py
│   │   └── routes.py             # Endpoints for policy upload and scoring
│   ├── agent/                    # Core LangGraph Agent Logic
│   │   ├── __init__.py
│   │   ├── graph.py              # LangGraph StateGraph (ReAct loop definition)
│   │   ├── state.py              # TypedDict defining the agent's memory/state
│   │   ├── nodes.py              # Node functions (search, evaluate, score)
│   │   ├── tools.py              # Tool definitions (Tavily search, web scraper)
│   │   └── prompts.py            # System instructions and evaluation rubrics
│   ├── core/                     # Application configuration
│   │   ├── config.py             # Pydantic BaseSettings for env variables
│   │   └── exceptions.py         # Custom error handling (e.g., DataNotFound)
│   └── models/                   # Pydantic data schemas
│       ├── request.py            # Input validation for user data
│       └── response.py           # Output schema for the final health score
├── tests/                        # Evaluation and unit tests
│   ├── test_agent.py
│   └── test_api.py
├── .env.example                  # Template for required API keys
├── .gitignore
├── Dockerfile                    # Containerization instructions
├── docker-compose.yml            # Local development orchestration
├── requirements.txt              # Python dependencies
└── README.md