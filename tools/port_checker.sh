#!/bin/bash

# Port Checker Utility
# This script checks if commonly used development ports are available
# Documentation: .cursor/rules/tools/port-checker.mdc

echo "Checking port availability for development..."

# Define port categories
FRONTEND_PORTS=(3000 3100 3200 3300 3400)
BACKEND_PORTS=(8000 8001 8080 8090 8100 8200)
DATABASE_PORTS=(5432 3306 27017 6379 9200)

# Function to check if a port is in use
check_port() {
  nc -z localhost $1 &>/dev/null
  if [ $? -eq 0 ]; then
    echo "❌ Port $1 is in use"
    return 1
  else
    echo "✅ Port $1 is available"
    return 0
  fi
}

# Check frontend ports
echo -e "\n📱 Frontend Ports:"
for port in "${FRONTEND_PORTS[@]}"; do
  check_port $port
done

# Check backend ports
echo -e "\n⚙️ Backend Ports:"
for port in "${BACKEND_PORTS[@]}"; do
  check_port $port
done

# Check database ports
echo -e "\n💾 Database Ports:"
for port in "${DATABASE_PORTS[@]}"; do
  check_port $port
done

# Summary
echo -e "\n📊 Summary:"
echo "If any required ports are in use, you can:"
echo "1. Stop the service using that port"
echo "2. Configure your application to use a different port"
echo "3. Document the port change in your project README"

echo -e "\nRefer to .cursor/rules/port-standardization.mdc for port allocation guidelines." 