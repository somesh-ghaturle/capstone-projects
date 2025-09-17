# FAIR-Agent Project Makefile

.PHONY: help build run download evaluate clean interactive setup

help:
	@echo "FAIR-Agent Project Commands:"
	@echo "  setup     - Complete setup (build + directories)"
	@echo "  build     - Build Docker image"
	@echo "  run       - Run the pipeline"
	@echo "  download  - Download datasets"
	@echo "  evaluate  - Run evaluation"
	@echo "  interactive - Start interactive container"
	@echo "  clean     - Remove containers and images"
	@echo "  help      - Show this help"

setup:
	@echo "Setting up FAIR-Agent project..."
	mkdir -p data/finance data/medicine logs
	docker build -t fair-agent:latest .

build:
	@echo "Building Docker image..."
	docker build -t fair-agent:latest .

run:
	@echo "Running FAIR-Agent pipeline..."
	docker run --rm -v $(PWD)/data:/app/data -v $(PWD)/logs:/app/logs fair-agent:latest python scripts/run_pipeline.py

download:
	@echo "Downloading datasets..."
	docker run --rm -v $(PWD)/data:/app/data fair-agent:latest python scripts/preprocess_finance.py
	docker run --rm -v $(PWD)/data:/app/data fair-agent:latest python scripts/preprocess_medical.py

evaluate:
	@echo "Running evaluation..."
	docker run --rm -v $(PWD)/data:/app/data -v $(PWD)/logs:/app/logs fair-agent:latest python scripts/evaluate.py

interactive:
	@echo "Starting interactive container..."
	docker run -it --rm -v $(PWD)/data:/app/data -v $(PWD)/logs:/app/logs fair-agent:latest /bin/bash

clean:
	@echo "Cleaning up..."
	docker container prune -f
	docker image rm fair-agent:latest 2>/dev/null || true
	docker system prune -f