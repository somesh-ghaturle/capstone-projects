#!/bin/bash

# FAIR-Agent Docker Startup Script

echo "🚀 Starting FAIR-Agent Project Setup..."

# Function to check if Docker is running
check_docker() {
    if ! docker info > /dev/null 2>&1; then
        echo "❌ Docker is not running. Please start Docker and try again."
        exit 1
    fi
    echo "✅ Docker is running"
}

# Function to build the Docker image
build_image() {
    echo "📦 Building FAIR-Agent Docker image..."
    docker build -t fair-agent:latest .
    if [ $? -eq 0 ]; then
        echo "✅ Docker image built successfully"
    else
        echo "❌ Failed to build Docker image"
        exit 1
    fi
}

# Function to create necessary directories
create_directories() {
    echo "📁 Creating necessary directories..."
    mkdir -p data/finance data/medicine logs
    echo "✅ Directories created"
}

# Function to download datasets
download_datasets() {
    echo "📊 Downloading datasets..."
    docker run --rm -v $(pwd)/data:/app/data fair-agent:latest python scripts/preprocess_finance.py
    docker run --rm -v $(pwd)/data:/app/data fair-agent:latest python scripts/preprocess_medical.py
    echo "✅ Datasets downloaded"
}

# Function to run the pipeline
run_pipeline() {
    echo "🔧 Running FAIR-Agent pipeline..."
    docker run --rm -v $(pwd)/data:/app/data -v $(pwd)/logs:/app/logs fair-agent:latest python scripts/run_pipeline.py
}

# Function to run evaluation
run_evaluation() {
    echo "📈 Running evaluation..."
    docker run --rm -v $(pwd)/data:/app/data -v $(pwd)/logs:/app/logs fair-agent:latest python scripts/evaluate.py
}

# Function to start interactive container
start_interactive() {
    echo "💻 Starting interactive container..."
    docker run -it --rm -v $(pwd)/data:/app/data -v $(pwd)/logs:/app/logs fair-agent:latest /bin/bash
}

# Main menu
show_menu() {
    echo ""
    echo "🤖 FAIR-Agent Docker Management"
    echo "================================"
    echo "1. Setup (Build image + Create directories)"
    echo "2. Download datasets"
    echo "3. Run pipeline"
    echo "4. Run evaluation"
    echo "5. Start interactive container"
    echo "6. Full setup and run"
    echo "7. Exit"
    echo ""
}

# Main execution
main() {
    check_docker
    
    if [ "$1" == "--auto" ]; then
        # Automated setup
        create_directories
        build_image
        download_datasets
        run_pipeline
        exit 0
    fi
    
    while true; do
        show_menu
        read -p "Choose an option (1-7): " choice
        
        case $choice in
            1)
                create_directories
                build_image
                ;;
            2)
                download_datasets
                ;;
            3)
                run_pipeline
                ;;
            4)
                run_evaluation
                ;;
            5)
                start_interactive
                ;;
            6)
                create_directories
                build_image
                download_datasets
                run_pipeline
                ;;
            7)
                echo "👋 Goodbye!"
                exit 0
                ;;
            *)
                echo "❌ Invalid option. Please choose 1-7."
                ;;
        esac
    done
}

# Run main function with all arguments
main "$@"