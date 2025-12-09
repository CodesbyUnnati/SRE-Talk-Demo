from flask import Flask, jsonify, request
import redis
import time
import os
import random
from prometheus_client import Counter, Histogram, generate_latest, REGISTRY
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

# Prometheus metrics
REQUEST_COUNT = Counter('api_requests_total', 'Total API requests', ['endpoint', 'status'])
REQUEST_DURATION = Histogram('api_request_duration_seconds', 'API request duration')
ERROR_COUNT = Counter('api_errors_total', 'Total API errors', ['type'])

# Configuration - THIS IS WHERE WE'LL INJECT FAILURES
ENABLE_MEMORY_LEAK = os.getenv('ENABLE_MEMORY_LEAK', 'false').lower() == 'true'
ENABLE_SLOW_QUERIES = os.getenv('ENABLE_SLOW_QUERIES', 'false').lower() == 'true'
REDIS_CONNECTION_POOL_SIZE = int(os.getenv('REDIS_POOL_SIZE', '10'))

# Redis connection
redis_client = redis.Redis(
    host='redis',
    port=6379,
    decode_responses=True,
    socket_connect_timeout=5,
    socket_timeout=5,
    max_connections=REDIS_CONNECTION_POOL_SIZE
)

# This will simulate memory leak
memory_hog = []

@app.route('/health')
def health():
    try:
        redis_client.ping()
        return jsonify({"status": "healthy", "redis": "connected"}), 200
    except Exception as e:
        ERROR_COUNT.labels(type='redis_connection').inc()
        return jsonify({"status": "unhealthy", "error": str(e)}), 503

@app.route('/api/data')
@REQUEST_DURATION.time()
def get_data():
    try:
        # Simulate memory leak if enabled (like CrowdStrike's config issue)
        if ENABLE_MEMORY_LEAK:
            # Each request leaks 1MB of memory
            memory_hog.append(' ' * 1024 * 1024)
            logging.warning(f"Memory leak active - current size: {len(memory_hog)} MB")
        
        # Simulate slow queries if enabled
        if ENABLE_SLOW_QUERIES:
            time.sleep(random.uniform(2, 5))
            logging.warning("Slow query executed")
        
        # Try to get data from Redis
        value = redis_client.get('counter')
        if value is None:
            value = 0
        else:
            value = int(value)
        
        value += 1
        redis_client.set('counter', value)
        
        REQUEST_COUNT.labels(endpoint='/api/data', status='success').inc()
        return jsonify({
            "message": "Success",
            "counter": value,
            "memory_leak_enabled": ENABLE_MEMORY_LEAK,
            "slow_queries_enabled": ENABLE_SLOW_QUERIES
        }), 200
        
    except redis.ConnectionError as e:
        ERROR_COUNT.labels(type='redis_connection').inc()
        REQUEST_COUNT.labels(endpoint='/api/data', status='error').inc()
        logging.error(f"Redis connection error: {e}")
        return jsonify({"error": "Database connection failed"}), 503
    except Exception as e:
        ERROR_COUNT.labels(type='unknown').inc()
        REQUEST_COUNT.labels(endpoint='/api/data', status='error').inc()
        logging.error(f"Unexpected error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/metrics')
def metrics():
    return generate_latest(REGISTRY)

@app.route('/reset')
def reset():
    """Reset the demo - clear memory leak"""
    global memory_hog
    memory_hog = []
    redis_client.set('counter', 0)
    return jsonify({"message": "Demo reset"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=False)