# FAIR-Agent Project

**Faithful, Adaptive, Interpretable, and Risk-Aware Agentic LLMs for Finance and Medicine**

A comprehensive multi-agent system that provides trustworthy, domain-specialized AI agents for finance and medical applications. This project addresses the critical need for reliable, interpretable, and risk-aware AI systems in high-stakes domains.

📋 **[Project Overview Statement](PROJECT_OVERVIEW_STATEMENT.md)** - Complete project charter and specifications

## 📚 Documentation

- 🗺️ **[Project Roadmap](ROADMAP.md)** - Development phases, milestones, and timeline
- 🏗️ **[Technical Architecture](ARCHITECTURE.md)** - System design and component specifications
- 📋 **[Project Overview Statement](PROJECT_OVERVIEW_STATEMENT.md)** - Official project charter
- 🚀 **[Getting Started](#usage)** - Quick start guide and installation instructions

## Project Structure

```
fair_agent_project/
├── data/
│   ├── finance/
│   └── medicine/
├── agents/
│   ├── finance_agent.py
│   ├── medical_agent.py
│   └── orchestrator.py
├── scripts/
│   ├── preprocess_finance.py
│   ├── preprocess_medical.py
│   ├── evaluate.py
│   └── run_pipeline.py
├── requirements.txt
├── config.yaml
└── README.md
```

## Installation

### Option 1: Docker (Recommended)

1. Ensure Docker is installed and running on your system
2. Use the automated setup script:
   ```bash
   ./docker-run.sh --auto
   ```
   Or use the interactive menu:
   ```bash
   ./docker-run.sh
   ```

### Option 2: Local Installation

1. Create a virtual environment (recommended):
   ```bash
   python -m venv fair_agent_env
   source fair_agent_env/bin/activate  # On Windows: fair_agent_env\Scripts\activate
   ```

2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Docker Usage (Recommended)

#### Quick Start
```bash
./docker-run.sh --auto
```

#### Interactive Menu
```bash
./docker-run.sh
```

#### Manual Docker Commands

Build the Docker image:
```bash
docker build -t fair-agent:latest .
```

Run with Docker Compose:
```bash
# Download datasets
docker-compose run data-downloader

# Run pipeline
docker-compose up fair-agent

# Run evaluation
docker-compose run evaluator
```

### Local Usage

### 1. Download Datasets

Download and preprocess the finance datasets:
```bash
python scripts/preprocess_finance.py
```

Download and preprocess the medical datasets:
```bash
python scripts/preprocess_medical.py
```

### 2. Run Example Pipeline

Execute the example pipeline to test the agents:
```bash
python scripts/run_pipeline.py
```

### 3. Evaluate the System

Run evaluation on the downloaded datasets:
```bash
python scripts/evaluate.py
```

## Components

### Agents

- **FinanceAgent**: Handles finance-related queries using Llama-2-7b model
- **MedicalAgent**: Handles medical queries using BioBERT model
- **Orchestrator**: Routes queries to appropriate agents based on domain

### Datasets

- **Finance**: IBM FinQA, TAT-QA
- **Medical**: MIMIC-IV, PubMedQA

## Configuration

The `config.yaml` file contains model configurations and dataset specifications. You can modify it to use different models or datasets.

## Features

- Multi-domain query handling
- Modular agent architecture
- Automated dataset downloading and preprocessing
- Evaluation framework
- Easy configuration management

## Requirements

- Python 3.8+
- PyTorch
- Transformers
- Datasets
- Pandas
- LangChain
- Scikit-learn

## Notes

- The first run may take longer due to model downloads
- Ensure you have sufficient disk space for models and datasets
- GPU is recommended for better performance but not required

## Future Enhancements

- Fine-tuning capabilities
- Advanced evaluation metrics
- Multi-agent synchronization
- Safety mitigations
- Web interface
- Additional domain support

## Docker Support

The project includes full Docker support for easy deployment and reproducibility.

### Docker Files

- `Dockerfile`: Main container definition
- `docker-compose.yml`: Multi-service orchestration
- `docker-run.sh`: Interactive management script
- `.dockerignore`: Optimizes build context

### Docker Benefits

- ✅ Consistent environment across systems
- ✅ Easy dependency management
- ✅ Isolated execution
- ✅ Simple deployment
- ✅ Reproducible results

### Container Features

- Python 3.9 slim base image
- Pre-configured environment variables
- Volume mounting for data persistence
- Multi-service support via Docker Compose
- Interactive and automated execution modes