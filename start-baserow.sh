#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}Starting Baserow and n8n containers...${NC}"

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo -e "${RED}Docker is not running! Please start Docker first.${NC}"
    exit 1
fi

# Stop and remove existing Baserow container if it exists
if docker ps -a | grep -q "baserow"; then
    echo -e "${YELLOW}Stopping existing Baserow container...${NC}"
    docker stop baserow > /dev/null 2>&1
    docker rm baserow > /dev/null 2>&1
fi

# Start containers using docker-compose
echo -e "${GREEN}Starting containers with docker-compose...${NC}"
docker-compose up -d

# Wait for services to be ready
echo -e "${YELLOW}Waiting for services to be ready...${NC}"
sleep 5

# Check if containers are running
if docker ps | grep -q "baserow"; then
    echo -e "${GREEN}✓ Baserow is running at: http://localhost${NC}"
else
    echo -e "${RED}✗ Baserow failed to start${NC}"
fi

if docker ps | grep -q "n8n-cursor-integration"; then
    echo -e "${GREEN}✓ n8n is running at: http://localhost:5679${NC}"
    echo -e "${GREEN}  Username: admin${NC}"
    echo -e "${GREEN}  Password: admin${NC}"
else
    echo -e "${RED}✗ n8n failed to start${NC}"
fi

echo ""
echo -e "${GREEN}Container Status:${NC}"
docker ps --filter "name=baserow" --filter "name=n8n-cursor-integration" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

echo ""
echo -e "${YELLOW}To view logs:${NC}"
echo "  Baserow: docker logs -f baserow"
echo "  n8n: docker logs -f n8n-cursor-integration"

echo ""
echo -e "${YELLOW}To stop containers:${NC}"
echo "  docker-compose down"

echo ""
echo -e "${GREEN}Integration Tips:${NC}"
echo "  1. Access Baserow at http://localhost and create your first workspace"
echo "  2. Generate an API token in Baserow (Settings > API tokens)"
echo "  3. In n8n, use the HTTP Request node or custom Baserow nodes"
echo "  4. Baserow API docs: https://baserow.io/api-docs"