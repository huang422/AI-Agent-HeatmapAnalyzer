#!/bin/bash

# Store Heatmap - Docker Startup Script with Ngrok
# This script starts the application and displays the ngrok public URL

set -e

echo "================================="
echo "Store Heatmap - Docker Startup"
echo "================================="
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "Error: Docker is not installed."
    echo "Please install Docker from: https://docs.docker.com/get-docker/"
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo "Error: Docker Compose is not installed."
    echo "Please install Docker Compose from: https://docs.docker.com/compose/install/"
    exit 1
fi

# Check if data directory exists
if [ ! -d "./data" ]; then
    echo "Error: Data directory not found."
    echo "Please ensure the './data' directory exists with data.csv file."
    exit 1
fi

# Check if data.csv exists
if [ ! -f "./data/data.csv" ]; then
    echo "Warning: data.csv not found in ./data directory."
    echo "The application may not work properly without data."
    read -p "Continue anyway? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

echo "Starting Docker containers..."
echo ""

# Check if we need sudo for docker
DOCKER_SUDO=""
if ! docker ps &> /dev/null; then
    if sudo docker ps &> /dev/null 2>&1; then
        echo "Note: Using sudo for Docker commands"
        DOCKER_SUDO="sudo"
    fi
fi

# Use docker compose (newer) or docker-compose (older)
if ${DOCKER_SUDO} docker compose version &> /dev/null; then
    DOCKER_COMPOSE="${DOCKER_SUDO} docker compose"
else
    DOCKER_COMPOSE="${DOCKER_SUDO} docker-compose"
fi

# Start services
$DOCKER_COMPOSE up -d --build

echo ""
echo "Waiting for services to be healthy..."
sleep 5

# Wait for backend to be healthy
echo "Checking backend..."
until ${DOCKER_SUDO} docker exec store-heatmap-backend python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" 2>/dev/null; do
    echo "Backend not ready yet, waiting..."
    sleep 2
done
echo "Backend is ready!"

# Wait for frontend to be healthy
echo "Checking frontend..."
until ${DOCKER_SUDO} docker exec store-heatmap-frontend wget --no-verbose --tries=1 --spider http://localhost/ 2>/dev/null; do
    echo "Frontend not ready yet, waiting..."
    sleep 2
done
echo "Frontend is ready!"

# Wait a bit for ngrok to establish tunnel
echo "Starting ngrok tunnel..."
sleep 3

echo ""
echo "================================="
echo "Application Started Successfully!"
echo "================================="
echo ""
echo "Local Access:"
echo "  Frontend:  http://localhost"
echo "  Backend:   http://localhost:8000"
echo "  API Docs:  http://localhost:8000/docs"
echo ""
echo "Ngrok Public Access:"
echo "  Dashboard: http://localhost:4040"
echo ""

# Try to get ngrok public URL
echo "Fetching public URL from ngrok..."
sleep 2

# Attempt to get the public URL from ngrok API
NGROK_URL=$(curl -s http://localhost:4040/api/tunnels | grep -o '"public_url":"[^"]*' | grep -o 'https://[^"]*' | head -1)

if [ -n "$NGROK_URL" ]; then
    echo ""
    echo "========================================================"
    echo ""
    echo "  PUBLIC URL (share this with others):"
    echo ""
    echo "  $NGROK_URL"
    echo ""
    echo "========================================================"
    echo ""
    echo "Anyone can access your app using this URL!"
    echo ""
else
    echo "Could not automatically retrieve ngrok URL."
    echo "Please visit http://localhost:4040 to see your public URL."
    echo ""
fi

echo "Useful Commands:"
echo "  View logs:         $DOCKER_COMPOSE logs -f"
echo "  Stop services:     $DOCKER_COMPOSE down"
echo "  Restart services:  $DOCKER_COMPOSE restart"
echo "  View ngrok URL:    curl http://localhost:4040/api/tunnels"
echo ""
echo "Press Ctrl+C to view logs (containers will keep running)"
echo ""

# Follow logs
$DOCKER_COMPOSE logs -f
