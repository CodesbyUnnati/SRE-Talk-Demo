from flask import Flask, jsonify, render_template_string
from flask_cors import CORS
import time
import random
import threading
import psutil
import os

app = Flask(__name__)
CORS(app)

# Demo configuration
config = {
    'memory_leak_enabled': False,
    'slow_queries_enabled': False,
    'connection_limit_enabled': False,
    'cascade_failure_enabled': False
}

# Tracking metrics
metrics = {
    'total_requests': 0,
    'successful_requests': 0,
    'failed_requests': 0,
    'avg_response_time': 0,
    'memory_usage_mb': 0
}

# Simulate memory leak
memory_leak_storage = []

# Simulate connection pool
connection_pool = []
MAX_CONNECTIONS = 10

# HTML Template for the dashboard
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>SRE Demo - Cascading Failures</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', system-ui, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
        }
        
        h1 {
            color: white;
            text-align: center;
            margin-bottom: 30px;
            font-size: 2.5em;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        
        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 20px;
            margin-bottom: 20px;
        }
        
        .card {
            background: white;
            border-radius: 12px;
            padding: 25px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        }
        
        .card h2 {
            color: #667eea;
            margin-bottom: 20px;
            font-size: 1.4em;
            border-bottom: 3px solid #667eea;
            padding-bottom: 10px;
        }
        
        .metric {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin: 15px 0;
            padding: 12px;
            background: #f8f9fa;
            border-radius: 8px;
        }
        
        .metric-label {
            font-weight: 600;
            color: #495057;
        }
        
        .metric-value {
            font-size: 1.8em;
            font-weight: bold;
            color: #667eea;
        }
        
        .status-indicator {
            display: inline-block;
            width: 20px;
            height: 20px;
            border-radius: 50%;
            margin-left: 10px;
        }
        
        .status-healthy { background: #10b981; }
        .status-warning { background: #f59e0b; }
        .status-critical { background: #ef4444; }
        
        button {
            width: 100%;
            padding: 15px;
            margin: 8px 0;
            border: none;
            border-radius: 8px;
            font-size: 1em;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        
        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 12px rgba(0,0,0,0.15);
        }
        
        button:active {
            transform: translateY(0);
        }
        
        .btn-test { background: #3b82f6; color: white; }
        .btn-normal { background: #10b981; color: white; }
        .btn-memory { background: #f59e0b; color: white; }
        .btn-slow { background: #f97316; color: white; }
        .btn-cascade { background: #ef4444; color: white; }
        .btn-reset { background: #6b7280; color: white; }
        
        .log-container {
            background: #1e293b;
            color: #10b981;
            padding: 20px;
            border-radius: 8px;
            font-family: 'Monaco', 'Courier New', monospace;
            font-size: 0.9em;
            max-height: 400px;
            overflow-y: auto;
        }
        
        .log-entry {
            padding: 8px;
            margin: 5px 0;
            border-left: 3px solid #10b981;
            padding-left: 12px;
        }
        
        .log-error { 
            border-left-color: #ef4444; 
            color: #ef4444; 
        }
        
        .log-warning { 
            border-left-color: #f59e0b; 
            color: #f59e0b; 
        }
        
        .config-status {
            padding: 8px 16px;
            border-radius: 20px;
            font-weight: bold;
            display: inline-block;
            margin: 5px 0;
        }
        
        .config-off { background: #10b981; color: white; }
        .config-on { background: #ef4444; color: white; }
        
        .instructions {
            background: white;
            border-radius: 12px;
            padding: 25px;
            margin-top: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        }
        
        .instructions h3 {
            color: #667eea;
            margin-bottom: 15px;
            font-size: 1.3em;
        }
        
        .instructions ol {
            margin-left: 25px;
        }
        
        .instructions li {
            margin: 12px 0;
            line-height: 1.8;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔥 SRE Demo: Cascading Failures 🔥</h1>
        
        <div class="grid">
            <!-- Metrics Card -->
            <div class="card">
                <h2>📊 System Metrics</h2>
                <div class="metric">
                    <span class="metric-label">Total Requests</span>
                    <span class="metric-value" id="total-requests">0</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Success Rate</span>
                    <span class="metric-value" id="success-rate">100%</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Avg Response Time</span>
                    <span class="metric-value" id="avg-response">0ms</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Memory Usage</span>
                    <span class="metric-value" id="memory-usage">0 MB</span>
                </div>
                <div class="metric">
                    <span class="metric-label">System Status</span>
                    <span class="status-indicator status-healthy" id="status-indicator"></span>
                </div>
            </div>
            
            <!-- Configuration Card -->
            <div class="card">
                <h2>⚙️ Current Configuration</h2>
                <div style="margin: 15px 0;">
                    <strong>Memory Leak:</strong>
                    <span class="config-status config-off" id="memory-status">OFF</span>
                </div>
                <div style="margin: 15px 0;">
                    <strong>Slow Queries:</strong>
                    <span class="config-status config-off" id="slow-status">OFF</span>
                </div>
                <div style="margin: 15px 0;">
                    <strong>Connection Limit:</strong>
                    <span class="config-status config-off" id="connection-status">OFF</span>
                </div>
                <div style="margin: 15px 0;">
                    <strong>Cascade Mode:</strong>
                    <span class="config-status config-off" id="cascade-status">OFF</span>
                </div>
            </div>
            
            <!-- Controls Card -->
            <div class="card">
                <h2>🎮 Demo Controls</h2>
                <button class="btn-test" onclick="testRequest()">🧪 Test Single Request</button>
                <button class="btn-normal" onclick="setMode('normal')">✅ Normal Mode</button>
                <button class="btn-memory" onclick="setMode('memory')">💾 Memory Leak Mode</button>
                <button class="btn-slow" onclick="setMode('slow')">🐌 Slow Query Mode</button>
                <button class="btn-cascade" onclick="setMode('cascade')">💥 Full Cascade Mode</button>
                <button class="btn-reset" onclick="resetDemo()">🔄 Reset Everything</button>
            </div>
        </div>
        
        <!-- Log Card -->
        <div class="card">
            <h2>📝 Activity Log</h2>
            <div class="log-container" id="log-container">
                <div class="log-entry">System initialized and ready...</div>
            </div>
        </div>
        
        <!-- Instructions -->
        <div class="instructions">
            <h3>📋 How to Use This Demo</h3>
            <ol>
                <li><strong>Test Normal:</strong> Click "Test Single Request" to see healthy system behavior (fast response)</li>
                <li><strong>Memory Leak:</strong> Enable to simulate CrowdStrike's config issue - watch memory grow and responses slow</li>
                <li><strong>Slow Queries:</strong> Enable to add 2-5 second delays - simulates database issues</li>
                <li><strong>Full Cascade:</strong> Enable ALL failures at once - watch the system struggle and fail</li>
                <li><strong>Reset:</strong> Clear all failures and metrics to start fresh</li>
            </ol>
            <p style="margin-top: 15px; padding: 15px; background: #fef3c7; border-radius: 8px;">
                <strong>💡 Tip:</strong> Start with "Test Single Request" to show normal operation, then progressively enable failures to demonstrate cascading issues.
            </p>
        </div>
    </div>
    
    <script>
        let autoRequestInterval = null;
        
        function addLog(message, type = 'info') {
            const container = document.getElementById('log-container');
            const entry = document.createElement('div');
            entry.className = 'log-entry' + (type === 'error' ? ' log-error' : type === 'warning' ? ' log-warning' : '');
            const timestamp = new Date().toLocaleTimeString();
            entry.textContent = `[${timestamp}] ${message}`;
            container.insertBefore(entry, container.firstChild);
            
            while (container.children.length > 50) {
                container.removeChild(container.lastChild);
            }
        }
        
        async function testRequest() {
            const startTime = Date.now();
            addLog('Sending test request...', 'info');
            
            try {
                const response = await fetch('/api/data');
                const data = await response.json();
                const duration = Date.now() - startTime;
                
                if (response.ok) {
                    addLog(`✅ Request successful in ${duration}ms`, 'info');
                    updateMetrics();
                } else {
                    addLog(`❌ Request failed: ${data.error}`, 'error');
                }
            } catch (error) {
                addLog(`❌ Request error: ${error.message}`, 'error');
            }
        }
        
        async function updateMetrics() {
            try {
                const response = await fetch('/api/metrics');
                const data = await response.json();
                
                document.getElementById('total-requests').textContent = data.total_requests;
                document.getElementById('success-rate').textContent = 
                    data.total_requests > 0 
                        ? Math.round((data.successful_requests / data.total_requests) * 100) + '%'
                        : '100%';
                document.getElementById('avg-response').textContent = Math.round(data.avg_response_time) + 'ms';
                document.getElementById('memory-usage').textContent = Math.round(data.memory_usage_mb) + ' MB';
                
                // Update status indicator
                const indicator = document.getElementById('status-indicator');
                const successRate = data.total_requests > 0 
                    ? (data.successful_requests / data.total_requests) * 100 
                    : 100;
                
                if (successRate >= 95 && data.avg_response_time < 500) {
                    indicator.className = 'status-indicator status-healthy';
                } else if (successRate >= 70 || data.avg_response_time < 2000) {
                    indicator.className = 'status-indicator status-warning';
                } else {
                    indicator.className = 'status-indicator status-critical';
                }
                
                // Update config status
                document.getElementById('memory-status').textContent = data.config.memory_leak_enabled ? 'ON' : 'OFF';
                document.getElementById('memory-status').className = 
                    data.config.memory_leak_enabled ? 'config-status config-on' : 'config-status config-off';
                
                document.getElementById('slow-status').textContent = data.config.slow_queries_enabled ? 'ON' : 'OFF';
                document.getElementById('slow-status').className = 
                    data.config.slow_queries_enabled ? 'config-status config-on' : 'config-status config-off';
                
                document.getElementById('connection-status').textContent = data.config.connection_limit_enabled ? 'ON' : 'OFF';
                document.getElementById('connection-status').className = 
                    data.config.connection_limit_enabled ? 'config-status config-on' : 'config-status config-off';
                
                document.getElementById('cascade-status').textContent = data.config.cascade_failure_enabled ? 'ON' : 'OFF';
                document.getElementById('cascade-status').className = 
                    data.config.cascade_failure_enabled ? 'config-status config-on' : 'config-status config-off';
                
            } catch (error) {
                console.error('Failed to update metrics:', error);
            }
        }
        
        async function setMode(mode) {
            addLog(`Setting mode to: ${mode.toUpperCase()}`, 'warning');
            
            try {
                const response = await fetch(`/api/mode/${mode}`, { method: 'POST' });
                const data = await response.json();
                
                if (response.ok) {
                    addLog(`✅ Mode changed to ${mode}`, 'info');
                    updateMetrics();
                    
                    // Start auto-requests if not normal mode
                    if (mode !== 'normal' && !autoRequestInterval) {
                        addLog('Starting continuous requests...', 'info');
                        autoRequestInterval = setInterval(testRequest, 3000);
                    }
                } else {
                    addLog(`❌ Failed to change mode: ${data.error}`, 'error');
                }
            } catch (error) {
                addLog(`❌ Error: ${error.message}`, 'error');
            }
        }
        
        async function resetDemo() {
            addLog('🔄 Resetting demo...', 'warning');
            
            if (autoRequestInterval) {
                clearInterval(autoRequestInterval);
                autoRequestInterval = null;
            }
            
            try {
                const response = await fetch('/api/reset', { method: 'POST' });
                const data = await response.json();
                
                if (response.ok) {
                    addLog('✅ Demo reset complete', 'info');
                    updateMetrics();
                } else {
                    addLog(`❌ Reset failed: ${data.error}`, 'error');
                }
            } catch (error) {
                addLog(`❌ Error: ${error.message}`, 'error');
            }
        }
        
        // Update metrics every 2 seconds
        setInterval(updateMetrics, 2000);
        updateMetrics();
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    """Serve the main dashboard"""
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/data')
def api_data():
    """Main API endpoint that can fail in various ways"""
    start_time = time.time()
    
    try:
        # Simulate memory leak
        if config['memory_leak_enabled']:
            # Add 5MB to memory leak storage each request
            memory_leak_storage.append(' ' * 5 * 1024 * 1024)
            time.sleep(0.2)  # Slight delay as memory operations slow down
        
        # Simulate slow queries
        if config['slow_queries_enabled']:
            delay = random.uniform(2, 5)
            time.sleep(delay)
        
        # Simulate connection pool exhaustion
        if config['connection_limit_enabled']:
            if len(connection_pool) >= MAX_CONNECTIONS:
                metrics['failed_requests'] += 1
                metrics['total_requests'] += 1
                return jsonify({'error': 'Connection pool exhausted'}), 503
            connection_pool.append(1)
            time.sleep(0.1)
            connection_pool.pop()
        
        # Cascade failure mode - everything fails
        if config['cascade_failure_enabled']:
            if random.random() > 0.3:  # 70% failure rate
                metrics['failed_requests'] += 1
                metrics['total_requests'] += 1
                return jsonify({'error': 'Cascading failure - system overloaded'}), 500
        
        # Success
        metrics['successful_requests'] += 1
        metrics['total_requests'] += 1
        
        # Update average response time
        response_time = (time.time() - start_time) * 1000
        if metrics['avg_response_time'] == 0:
            metrics['avg_response_time'] = response_time
        else:
            metrics['avg_response_time'] = (metrics['avg_response_time'] * 0.9) + (response_time * 0.1)
        
        # Update memory usage
        process = psutil.Process(os.getpid())
        metrics['memory_usage_mb'] = process.memory_info().rss / 1024 / 1024
        
        return jsonify({
            'status': 'success',
            'response_time_ms': round(response_time, 2),
            'message': 'Request processed successfully'
        }), 200
        
    except Exception as e:
        metrics['failed_requests'] += 1
        metrics['total_requests'] += 1
        return jsonify({'error': str(e)}), 500

@app.route('/api/metrics')
def get_metrics():
    """Get current system metrics"""
    return jsonify({
        **metrics,
        'config': config
    })

@app.route('/api/mode/<mode>', methods=['POST'])
def set_mode(mode):
    """Set system mode"""
    if mode == 'normal':
        config['memory_leak_enabled'] = False
        config['slow_queries_enabled'] = False
        config['connection_limit_enabled'] = False
        config['cascade_failure_enabled'] = False
    elif mode == 'memory':
        config['memory_leak_enabled'] = True
        config['slow_queries_enabled'] = False
        config['connection_limit_enabled'] = False
        config['cascade_failure_enabled'] = False
    elif mode == 'slow':
        config['memory_leak_enabled'] = False
        config['slow_queries_enabled'] = True
        config['connection_limit_enabled'] = False
        config['cascade_failure_enabled'] = False
    elif mode == 'cascade':
        config['memory_leak_enabled'] = True
        config['slow_queries_enabled'] = True
        config['connection_limit_enabled'] = True
        config['cascade_failure_enabled'] = True
    else:
        return jsonify({'error': 'Invalid mode'}), 400
    
    return jsonify({'status': 'success', 'mode': mode, 'config': config})

@app.route('/api/reset', methods=['POST'])
def reset():
    """Reset demo to initial state"""
    global memory_leak_storage, connection_pool
    
    memory_leak_storage = []
    connection_pool = []
    
    config['memory_leak_enabled'] = False
    config['slow_queries_enabled'] = False
    config['connection_limit_enabled'] = False
    config['cascade_failure_enabled'] = False
    
    metrics['total_requests'] = 0
    metrics['successful_requests'] = 0
    metrics['failed_requests'] = 0
    metrics['avg_response_time'] = 0
    metrics['memory_usage_mb'] = 0
    
    return jsonify({'status': 'reset complete'})

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🚀 SRE DEMO SERVER STARTING")
    print("="*60)
    print("\n📍 Open your browser and go to: http://localhost:5002")
    print("\n⚠️  Press Ctrl+C to stop the server\n")
    print("="*60 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5002)