#!/bin/bash

echo "SRE Demo Control Script"
echo "======================="
echo ""
echo "1. Normal Mode"
echo "2. Enable Memory Leak"
echo "3. Enable Slow Queries"
echo "4. Enable BOTH (Full Cascade)"
echo "5. Reset Demo"
echo ""
read -p "Select option (1-5): " choice

case $choice in
    1)
        echo "Setting normal mode..."
        echo "ENABLE_MEMORY_LEAK=false" > .env
        echo "ENABLE_SLOW_QUERIES=false" >> .env
        echo "REDIS_POOL_SIZE=10" >> .env
        docker-compose restart api
        echo "✅ Normal mode active"
        ;;
    2)
        echo "⚠️  Enabling memory leak..."
        echo "ENABLE_MEMORY_LEAK=true" > .env
        echo "ENABLE_SLOW_QUERIES=false" >> .env
        echo "REDIS_POOL_SIZE=10" >> .env
        docker-compose restart api
        echo "💥 Memory leak enabled - watch the cascade!"
        ;;
    3)
        echo "⚠️  Enabling slow queries..."
        echo "ENABLE_MEMORY_LEAK=false" > .env
        echo "ENABLE_SLOW_QUERIES=true" >> .env
        echo "REDIS_POOL_SIZE=10" >> .env
        docker-compose restart api
        echo "🐌 Slow queries enabled - watch response times!"
        ;;
    4)
        echo "🔥 ENABLING FULL CASCADE FAILURE..."
        echo "ENABLE_MEMORY_LEAK=true" > .env
        echo "ENABLE_SLOW_QUERIES=true" >> .env
        echo "REDIS_POOL_SIZE=5" >> .env
        docker-compose restart api
        echo "💥💥 Full cascade active - system will struggle!"
        ;;
    5)
        echo "Resetting demo..."
        curl -X GET http://localhost:5001/reset
        echo "ENABLE_MEMORY_LEAK=false" > .env
        echo "ENABLE_SLOW_QUERIES=false" >> .env
        echo "REDIS_POOL_SIZE=10" >> .env
        docker-compose restart api
        echo "✅ Demo reset complete"
        ;;
    *)
        echo "Invalid option"
        ;;
esac