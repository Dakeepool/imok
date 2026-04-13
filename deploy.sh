#!/bin/bash

# Production Deployment Script
# This script deploys the FastAPI authentication system to production

set -e

echo "=== FastAPI Auth System Deployment ==="

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Check if .env.production exists
if [ ! -f ".env.production" ]; then
    echo "ERROR: .env.production file not found!"
    echo "Please copy .env.example to .env.production and configure it."
    exit 1
fi

# Load environment variables
export $(grep -v '^#' .env.production | xargs)

# Check required environment variables
if [ -z "$SECRET_KEY" ] || [ "$SECRET_KEY" = "CHANGE_THIS_TO_A_STRONG_RANDOM_KEY_AT_LEAST_32_CHARACTERS_LONG" ]; then
    echo "ERROR: Please set a strong SECRET_KEY in .env.production"
    exit 1
fi

if [ -z "$MYSQL_ROOT_PASSWORD" ]; then
    echo "ERROR: Please set MYSQL_ROOT_PASSWORD in .env.production"
    exit 1
fi

echo "1. Building Docker images..."
docker-compose build

echo "2. Starting services..."
docker-compose up -d

echo "3. Waiting for database to be ready..."
sleep 30

echo "4. Running database migrations..."
docker-compose exec web python -c "
from database import engine, Base
Base.metadata.create_all(bind=engine)
print('Database tables created successfully!')
"

echo "5. Checking service health..."
if curl -f http://localhost:8000/health > /dev/null 2>&1; then
    echo "=== Deployment Successful! ==="
    echo "Application is running at: http://localhost:8000"
    echo "API Documentation: http://localhost:8000/docs"
    echo ""
    echo "To stop the application: docker-compose down"
    echo "To view logs: docker-compose logs -f"
    echo "To restart: docker-compose restart"
else
    echo "ERROR: Health check failed!"
    echo "Check logs with: docker-compose logs"
    exit 1
fi
