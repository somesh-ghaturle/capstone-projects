# FAIR-Agent System - Technical Flowchart

**CS668 Analytics Capstone - Fall 2025**  
**Team**: Somesh Ghaturle, Darshil Malaviya, Priyank Mistry  
**Document**: Complete Technical Architecture & Data Flow

---

## 🔄 **System Overview Flowchart**

```mermaid
graph TB
    A[👤 User Input] --> B[🌐 Web Interface<br/>Django Frontend]
    A --> C[💻 CLI Interface<br/>Command Line]
    
    B --> D[📡 API Gateway<br/>Django REST API]
    C --> D
    
    D --> E[🎯 Orchestrator<br/>Central Coordinator]
    
    E --> F{🔍 Domain Classifier<br/>Query Analysis}
    
    F -->|Medical Keywords| G[🏥 Medical Agent<br/>GPT-2 Medical]
    F -->|Finance Keywords| H[💰 Finance Agent<br/>GPT-2 Finance]
    F -->|Cross-Domain| I[🔄 Multi-Agent<br/>Coordination]
    F -->|General| J[📝 General Handler<br/>Domain Guidance]
    
    G --> K[🛡️ Medical Safety<br/>Disclaimer System]
    H --> L[⚠️ Financial Safety<br/>Risk Warnings]
    I --> M[🤝 Cross-Domain<br/>Integration]
    J --> N[ℹ️ Domain Redirect<br/>Guidance Response]
    
    K --> O[📚 Evidence Citation<br/>Medical Sources]
    L --> P[📊 Evidence Citation<br/>Financial Sources]
    M --> Q[🔗 Multi-Source<br/>Evidence]
    
    O --> R[🧠 Chain-of-Thought<br/>Medical Reasoning]
    P --> S[🧠 Chain-of-Thought<br/>Financial Reasoning]
    Q --> T[🧠 Chain-of-Thought<br/>Integrated Reasoning]
    
    R --> U[📈 FAIR Metrics<br/>Evaluation]
    S --> U
    T --> U
    N --> U
    
    U --> V[📊 Response Assembly<br/>With Metrics]
    V --> W[📤 Final Response<br/>To User]
    
    style A fill:#e3f2fd
    style W fill:#c8e6c9
    style E fill:#fff3e0
    style U fill:#fce4ec
```

---

## 🏗️ **Detailed Component Architecture**

### 1. **Entry Points & User Interface**

```mermaid
graph LR
    A[User] --> B[Web Browser<br/>Port 8000]
    A --> C[Terminal<br/>CLI Mode]
    
    B --> D[Django Templates<br/>- home.html<br/>- query.html<br/>- results.html]
    C --> E[CLI Handler<br/>main.py --mode cli]
    
    D --> F[Django Views<br/>- QueryView<br/>- ResultsView]
    E --> F
    
    F --> G[API Service Layer<br/>fair_agent_app/services.py]
    
    style A fill:#e1f5fe
    style G fill:#f3e5f5
```

### 2. **Core Processing Pipeline**

```mermaid
graph TB
    A[Query Input] --> B[Input Validation<br/>& Sanitization]
    B --> C[Domain Classification<br/>Keyword Analysis]
    
    C --> D{Classification Result}
    
    D -->|medical| E[Medical Agent Pipeline]
    D -->|finance| F[Finance Agent Pipeline]
    D -->|cross_domain| G[Multi-Agent Pipeline]
    D -->|general| H[General Handler]
    
    E --> I[Medical Model<br/>GPT-2 Inference]
    F --> J[Finance Model<br/>GPT-2 Inference]
    G --> K[Both Models<br/>Coordinated]
    
    I --> L[Medical Enhancement<br/>Pipeline]
    J --> M[Finance Enhancement<br/>Pipeline]
    K --> N[Cross-Domain<br/>Enhancement]
    H --> O[Domain Guidance<br/>Response]
    
    L --> P[Response Integration]
    M --> P
    N --> P
    O --> P
    
    P --> Q[FAIR Metrics<br/>Evaluation]
    Q --> R[Final Response<br/>Assembly]
    
    style A fill:#e8f5e8
    style R fill:#fff3e0
```

---

## 🔧 **Enhancement Systems Architecture**

### 3. **Safety & Disclaimer System**

```mermaid
graph TB
    A[Response Generated] --> B{Domain Detection}
    
    B -->|Medical| C[Medical Safety Check<br/>src/enhancement/safety/]
    B -->|Finance| D[Financial Safety Check<br/>src/enhancement/safety/]
    B -->|General| E[General Safety Check]
    
    C --> F[Medical Disclaimer<br/>⚠️ Medical Disclaimer Template]
    D --> G[Financial Disclaimer<br/>💰 Financial Risk Warning]
    E --> H[Basic Safety Check]
    
    F --> I[Severity Assessment<br/>Low/Medium/High]
    G --> J[Risk Assessment<br/>Investment Warnings]
    H --> K[Content Safety]
    
    I --> L[Disclaimer Selection<br/>Template Based]
    J --> L
    K --> L
    
    L --> M[Disclaimer Integration<br/>Into Response]
    
    style C fill:#ffebee
    style D fill:#fff3e0
    style M fill:#e8f5e8
```

### 4. **Evidence Citation System**

```mermaid
graph TB
    A[Domain Response] --> B[Evidence Extractor<br/>src/enhancement/retrieval/]
    
    B --> C[RAG System<br/>rag_enhancer.py]
    
    C --> D[Knowledge Base<br/>8 Evidence Sources]
    
    D --> E{Evidence Type}
    
    E -->|Medical| F[Medical Citations<br/>- Research Papers<br/>- Guidelines<br/>- Clinical Data]
    E -->|Financial| G[Financial Citations<br/>- Market Data<br/>- Economic Reports<br/>- Analysis]
    E -->|General| H[General Sources<br/>- Educational Content]
    
    F --> I[Citation Formatter<br/>[1] [2] [3] Format]
    G --> I
    H --> I
    
    I --> J[Reference List<br/>Generation]
    
    J --> K[Evidence Integration<br/>Into Response]
    
    style C fill:#e3f2fd
    style I fill:#f3e5f5
```

### 5. **Chain-of-Thought Reasoning**

```mermaid
graph TB
    A[Query Input] --> B[CoT System<br/>src/enhancement/reasoning/]
    
    B --> C[Domain-Specific<br/>Reasoning Templates]
    
    C --> D{Template Selection}
    
    D -->|Medical| E[Medical CoT Template<br/>6-Step Medical Analysis]
    D -->|Financial| F[Financial CoT Template<br/>6-Step Financial Analysis]
    D -->|General| G[General CoT Template<br/>Basic Reasoning]
    
    E --> H[Step 1: Symptom Analysis<br/>Step 2: Common Causes<br/>Step 3: Red Flags<br/>Step 4: Risk Factors<br/>Step 5: Recommendations<br/>Step 6: Professional Consultation]
    
    F --> I[Step 1: Query Analysis<br/>Step 2: Risk Tolerance<br/>Step 3: Investment Options<br/>Step 4: Diversification<br/>Step 5: Returns & Volatility<br/>Step 6: Professional Advice]
    
    G --> J[Step 1: Problem Analysis<br/>Step 2: Context Evaluation<br/>Step 3: Solution Exploration<br/>Step 4: Risk Assessment<br/>Step 5: Recommendations<br/>Step 6: Next Steps]
    
    H --> K[Reasoning Integration<br/>Into Response]
    I --> K
    J --> K
    
    K --> L[Confidence Scoring<br/>Transparency Metrics]
    
    style B fill:#fff3e0
    style K fill:#e8f5e8
```

---

## 📊 **FAIR Metrics Evaluation Pipeline**

### 6. **Comprehensive Evaluation System**

```mermaid
graph TB
    A[Generated Response] --> B[FAIR Evaluation<br/>Orchestrator]
    
    B --> C[Faithfulness Evaluator<br/>src/evaluation/faithfulness.py]
    B --> D[Interpretability Evaluator<br/>src/evaluation/interpretability.py]
    B --> E[Safety Evaluator<br/>src/evaluation/safety.py]
    B --> F[Calibration Evaluator<br/>src/evaluation/calibration.py]
    B --> G[Robustness Evaluator<br/>src/evaluation/robustness.py]
    
    C --> H[Token Overlap Analysis<br/>Semantic Similarity<br/>Factual Consistency]
    D --> I[Reasoning Clarity<br/>Explanation Completeness<br/>Evidence Citation Quality]
    E --> J[Domain Safety Checks<br/>Content Safety Analysis<br/>Risk Assessment]
    F --> K[Confidence Calibration<br/>Reliability Scoring<br/>Uncertainty Quantification]
    G --> L[Consistency Analysis<br/>Perturbation Resistance<br/>Static Robustness]
    
    H --> M[Faithfulness Score<br/>25-60% Range]
    I --> N[Interpretability Score<br/>40-60% Range]
    J --> O[Safety Score<br/>56-76% Range]
    K --> P[Calibration Score<br/>30-70% Range]
    L --> Q[Robustness Score<br/>20-25% Range]
    
    M --> R[FAIR Metrics<br/>Aggregation]
    N --> R
    O --> R
    P --> R
    Q --> R
    
    R --> S[Final Response<br/>With Metrics]
    
    style B fill:#fce4ec
    style R fill:#e8f5e8
    style S fill:#c8e6c9
```

---

## 🗄️ **Data Flow & Storage Architecture**

### 7. **Database & Persistence Layer**

```mermaid
graph TB
    A[User Query] --> B[Query Processing]
    B --> C[QueryRecord Model<br/>webapp/fair_agent_app/models.py]
    
    C --> D[SQLite Database<br/>db.sqlite3]
    
    D --> E[Stored Data:<br/>- Query Text<br/>- Domain Classification<br/>- Response Content<br/>- FAIR Metrics<br/>- Processing Time<br/>- Timestamp]
    
    E --> F[Query History<br/>Analytics]
    
    F --> G[Performance Tracking<br/>System Monitoring]
    
    B --> H[Configuration Loading<br/>config/system_config.yaml]
    
    H --> I[Agent Configuration<br/>Model Settings<br/>System Parameters]
    
    I --> J[Runtime Configuration<br/>Dynamic Settings]
    
    style D fill:#e3f2fd
    style F fill:#fff3e0
```

### 8. **Model Loading & Management**

```mermaid
graph TB
    A[System Startup] --> B[Configuration Loader<br/>src/core/config.py]
    
    B --> C[Model Manager<br/>Agent Initialization]
    
    C --> D{Model Loading Strategy}
    
    D -->|Finance| E[Finance Agent<br/>src/agents/finance_agent.py]
    D -->|Medical| F[Medical Agent<br/>src/agents/medical_agent.py]
    
    E --> G[GPT-2 Model Loading<br/>Transformers Pipeline]
    F --> H[GPT-2 Model Loading<br/>Transformers Pipeline]
    
    G --> I[Device Detection<br/>CPU/CUDA/MPS]
    H --> I
    
    I --> J[Memory Optimization<br/>Model Caching]
    
    J --> K[Ready for Inference<br/>Agent Available]
    
    K --> L[Health Check<br/>Model Validation]
    
    style C fill:#fff3e0
    style K fill:#c8e6c9
```

---

## 🐳 **Deployment Architecture**

### 9. **Docker Containerization**

```mermaid
graph TB
    A[Docker Build] --> B[Base Image<br/>python:3.11-slim]
    
    B --> C[Dependencies Install<br/>requirements-docker.txt]
    
    C --> D[Application Copy<br/>Source Code & Config]
    
    D --> E[Database Migration<br/>Django Setup]
    
    E --> F[Health Check Setup<br/>Container Monitoring]
    
    F --> G[Container Ready<br/>Port 8000 Exposed]
    
    G --> H[Docker Compose<br/>Orchestration]
    
    H --> I[Network Setup<br/>fair-agent-network]
    
    I --> J[Volume Mapping<br/>Data Persistence]
    
    J --> K[Service Running<br/>fair-agent-system]
    
    K --> L[Health Monitoring<br/>Automatic Restart]
    
    style A fill:#e1f5fe
    style K fill:#c8e6c9
```

### 10. **API Endpoints & Routes**

```mermaid
graph TB
    A[HTTP Request] --> B[Django URL Router<br/>webapp/urls.py]
    
    B --> C{Route Matching}
    
    C -->|/| D[Home View<br/>Landing Page]
    C -->|/query/| E[Query Form View<br/>Input Interface]
    C -->|/api/query/process/| F[API Endpoint<br/>Query Processing]
    C -->|/results/| G[Results View<br/>Display Response]
    
    D --> H[Template Rendering<br/>home.html]
    E --> I[Template Rendering<br/>query.html]
    F --> J[JSON API Response<br/>services.py]
    G --> K[Template Rendering<br/>results.html]
    
    J --> L[Response Format:<br/>{<br/>  "query_id": int,<br/>  "answer": string,<br/>  "confidence": float,<br/>  "domain": string,<br/>  "fair_metrics": object,<br/>  "processing_time": float<br/>}]
    
    style B fill:#e3f2fd
    style F fill:#fff3e0
    style L fill:#c8e6c9
```

---

## 🔧 **Enhancement Integration Flow**

### 11. **Complete Enhancement Pipeline**

```mermaid
graph TB
    A[Raw Response] --> B[Enhancement Orchestrator<br/>services.py Integration]
    
    B --> C[Safety Enhancement<br/>disclaimer_system.py]
    B --> D[Evidence Enhancement<br/>rag_enhancer.py]
    B --> E[Reasoning Enhancement<br/>cot_system.py]
    
    C --> F[Domain-Specific<br/>Disclaimers Added]
    D --> G[Citations &<br/>References Added]
    E --> H[Step-by-Step<br/>Reasoning Added]
    
    F --> I[Response Assembly<br/>Integration Layer]
    G --> I
    H --> I
    
    I --> J[Enhanced Response<br/>Structure:<br/>- Original Content<br/>- Safety Disclaimers<br/>- Evidence Citations<br/>- Reasoning Process<br/>- Reference List<br/>- Confidence Scores]
    
    J --> K[FAIR Evaluation<br/>Enhanced Metrics]
    
    K --> L[Final Enhanced<br/>Response Output]
    
    style B fill:#fff3e0
    style I fill:#f3e5f5
    style L fill:#c8e6c9
```

---

## 📝 **File Structure & Code Organization**

### 12. **Complete Codebase Map**

```
FAIR-Agent/
├── 🏠 main.py                          # System Entry Point
├── 🐳 docker-compose.yml               # Container Orchestration
├── 📋 requirements.txt                 # Python Dependencies
├── 📚 README.md                        # Project Documentation
├── 🔧 TECHNICAL_FLOWCHART.md          # This Document
│
├── 📁 config/                          # Configuration Management
│   ├── system_config.yaml             # Main System Config
│   └── safety_keywords.yaml           # Safety Filter Rules
│
├── 📁 src/                             # Core System Code
│   ├── 🔧 core/                        # System Foundation
│   │   ├── system.py                  # Main System Class
│   │   └── config.py                  # Configuration Loader
│   │
│   ├── 🤖 agents/                      # AI Agent Components
│   │   ├── orchestrator.py            # Central Coordinator
│   │   ├── finance_agent.py           # Finance Specialist
│   │   └── medical_agent.py           # Medical Specialist
│   │
│   ├── 📊 evaluation/                  # FAIR Metrics System
│   │   ├── faithfulness.py            # Accuracy Evaluation
│   │   ├── interpretability.py        # Clarity Assessment
│   │   ├── safety.py                  # Safety Evaluation
│   │   ├── calibration.py             # Confidence Calibration
│   │   └── robustness.py              # Robustness Testing
│   │
│   ├── 🛠️ enhancement/                 # System Enhancements
│   │   ├── 🔧 fine_tuning/            # Model Fine-Tuning
│   │   │   └── manager.py             # Training Manager
│   │   ├── 🛡️ safety/                 # Safety Systems
│   │   │   └── disclaimer_system.py   # Disclaimer Generator
│   │   ├── 📚 retrieval/              # Evidence Systems
│   │   │   └── rag_enhancer.py        # Citation System
│   │   └── 🧠 reasoning/              # Reasoning Systems
│   │       └── cot_system.py          # Chain-of-Thought
│   │
│   └── 🔧 utils/                       # Utility Functions
│       └── logger.py                  # Logging System
│
├── 📁 webapp/                          # Django Web Interface
│   ├── manage.py                      # Django Management
│   ├── settings.py                    # Django Settings
│   ├── urls.py                        # URL Routing
│   │
│   ├── 📁 fair_agent_app/             # Main Django App
│   │   ├── views.py                   # Request Handlers
│   │   ├── models.py                  # Database Models
│   │   ├── services.py                # Business Logic
│   │   └── urls.py                    # App URL Patterns
│   │
│   └── 📁 templates/                  # HTML Templates
│       ├── base.html                  # Base Template
│       ├── home.html                  # Landing Page
│       ├── query.html                 # Query Interface
│       └── results.html               # Results Display
│
├── 📁 data/                           # Data Storage
│   └── models/                       # Model Cache
│
└── 📁 logs/                          # System Logs
    └── system.log                    # Application Logs
```

---

## 🚀 **Startup Sequence & Initialization**

### 13. **System Startup Flow**

```mermaid
graph TB
    A[System Start<br/>main.py] --> B[Argument Parsing<br/>CLI/Web Mode]
    
    B --> C[Configuration Loading<br/>config/system_config.yaml]
    
    C --> D[Logging Setup<br/>utils/logger.py]
    
    D --> E[Core System Init<br/>src/core/system.py]
    
    E --> F[Agent Loading<br/>orchestrator.py]
    
    F --> G[Model Loading<br/>GPT-2 Finance & Medical]
    
    G --> H[Enhancement Systems<br/>Safety, Evidence, Reasoning]
    
    H --> I[Database Setup<br/>Django Migrations]
    
    I --> J[Web Server Start<br/>Django Dev Server]
    
    J --> K[Health Check<br/>System Ready]
    
    K --> L[📍 System Running<br/>Port 8000 Active]
    
    style A fill:#e1f5fe
    style L fill:#c8e6c9
    
    M[⏱️ Timing Info:<br/>- Config Load: ~1s<br/>- Model Load: ~30s<br/>- Total Startup: ~45s] 
    
    K --> M
```

---

## 🔍 **Query Processing Detailed Flow**

### 14. **End-to-End Query Processing**

```mermaid
graph TB
    A[👤 User Query:<br/>"What are symptoms of diabetes?"] --> B[🌐 Web Interface<br/>Form Submission]
    
    B --> C[📡 API Endpoint<br/>/api/query/process/]
    
    C --> D[🔍 Input Validation<br/>- Sanitization<br/>- Length Check<br/>- Content Filter]
    
    D --> E[🎯 Domain Classification<br/>Keywords: diabetes, symptoms<br/>Result: MEDICAL]
    
    E --> F[🏥 Medical Agent<br/>GPT-2 Medical Model]
    
    F --> G[🤖 Model Inference<br/>Response Generation<br/>~10 seconds]
    
    G --> H[🛡️ Safety Enhancement<br/>Medical Disclaimer Added]
    
    H --> I[📚 Evidence Enhancement<br/>Medical Citations Added<br/>[1] Diabetes Guidelines<br/>[2] Medical Research]
    
    I --> J[🧠 Reasoning Enhancement<br/>6-Step Medical Analysis<br/>Step 1: Symptom Analysis<br/>Step 2: Common Causes<br/>...etc]
    
    J --> K[📊 FAIR Evaluation<br/>- Faithfulness: 0.26<br/>- Interpretability: 0.53<br/>- Safety: 0.56<br/>- Calibration: 0.70<br/>- Robustness: 0.23]
    
    K --> L[💾 Database Storage<br/>QueryRecord Saved<br/>ID: 123, Timestamp, Metrics]
    
    L --> M[📤 JSON Response<br/>{<br/>  "answer": "Enhanced Response...",<br/>  "fair_metrics": {...},<br/>  "confidence": 1.0<br/>}]
    
    M --> N[🌐 Frontend Display<br/>Results Page with<br/>Metrics Dashboard]
    
    style A fill:#e1f5fe
    style N fill:#c8e6c9
    style K fill:#fce4ec
```

---

## 💡 **Team Development Guidelines**

### 15. **Development Workflow for Team**

```mermaid
graph TB
    A[🔄 Development Task] --> B{Task Category}
    
    B -->|New Agent| C[📁 src/agents/<br/>Create new agent class<br/>Follow pattern of existing agents]
    
    B -->|New Metric| D[📁 src/evaluation/<br/>Create evaluator class<br/>Implement evaluate() method]
    
    B -->|Enhancement| E[📁 src/enhancement/<br/>Create enhancement module<br/>Follow existing patterns]
    
    B -->|Web Feature| F[📁 webapp/<br/>Update views, templates, models<br/>Django patterns]
    
    C --> G[🧪 Testing<br/>- Unit tests<br/>- Integration tests<br/>- Manual testing]
    
    D --> G
    E --> G
    F --> G
    
    G --> H[📚 Documentation<br/>- Update this flowchart<br/>- Update README<br/>- Add docstrings]
    
    H --> I[🔧 Configuration<br/>- Update config files<br/>- Environment variables<br/>- Docker if needed]
    
    I --> J[🚀 Deployment<br/>- Docker rebuild<br/>- System restart<br/>- Verification]
    
    J --> K[✅ Task Complete<br/>Ready for review]
    
    style A fill:#e1f5fe
    style K fill:#c8e6c9
```

---

## 🏁 **Summary & Key Points**

### **🎯 For Team Members:**

1. **Start Here**: Always check this flowchart before making changes
2. **Follow Patterns**: Use existing code patterns for consistency
3. **Test Everything**: Each component has specific testing requirements
4. **Update Documentation**: Keep this flowchart and README current
5. **Docker First**: Use Docker for development and testing

### **🔧 Key System Components:**

- **Orchestrator**: Central coordinator (`src/agents/orchestrator.py`)
- **Agents**: Specialized AI models (`src/agents/`)
- **Enhancements**: Safety, Evidence, Reasoning (`src/enhancement/`)
- **Evaluation**: FAIR metrics system (`src/evaluation/`)
- **Web Interface**: Django application (`webapp/`)

### **📊 Current System Status:**

- ✅ **Recalibrated FAIR Metrics**: Realistic GPT-2 performance (25-76%)
- ✅ **Safety System**: Medical/Financial disclaimers working
- ✅ **Evidence Citations**: Automatic source citation \[1\]\[2\]\[3\]
- ✅ **Chain-of-Thought**: 6-step reasoning process
- ✅ **Docker Deployment**: Containerized system ready
- ✅ **Web Interface**: Full Django application at port 8000

### **🚀 Next Development Areas:**

1. **Fine-Tuning Pipeline**: Complete model training system
2. **Advanced Metrics**: Additional evaluation dimensions  
3. **UI/UX Enhancement**: Better web interface design
4. **Performance Optimization**: Speed and memory improvements
5. **Testing Framework**: Comprehensive test suite

---

**📅 Last Updated**: September 28, 2025  
**👥 Team**: Somesh Ghaturle, Darshil Malaviya, Priyank Mistry  
**📧 Contact**: Refer to individual team members for specific component questions

---

*This document serves as the master technical reference for the FAIR-Agent system. Keep it updated as the system evolves!*
