## **What this code does:**

*   Creates a web server with Flask
    
*   Has different failure modes you can enable
    
*   Shows real-time metrics
    
*   Simulates memory leaks, slow queries, and cascading failures
    

### Step 1: Install psutil Package

We need psutil for memory monitoring:


```bash
`   pip3 install psutil   `
```
### Step 2: Install Required Python Packages

```
pip3 install flask flask-cors
```

Running the Demo
----------------

### Step 1: Start the Server

```
python3 demo.py

```

**Expected output:**

```
============================================================  🚀 SRE DEMO SERVER STARTING  ============================================================
 📍 Open your browser and go to: http://localhost:5000
 ⚠️  Press Ctrl+C to stop the server  ============================================================
 * Running on http://0.0.0.0:5000   * Running on http://127.0.0.1:5000   `
```
### Step 2: Open Your Browser

Open **Chrome, Firefox, or Safari** and go to:
```
http://localhost:5000

````
**You should see:** A colorful dashboard with metrics, buttons, and a log

Demo Script for Your Talk
-------------------------

### Scene 1: Normal Operation

**What to do:**

1.  Point to the dashboard on screen
    
2.  Click **"Test Single Request"** button 3-4 times
    
3.  Show the audience:
    
    *   Response time: ~10-50ms
        
    *   Success rate: 100%
        
    *   Memory: stable
        
    *   Activity log: all green checkmarks
        

### Scene 2: Memory Leak

**What to do:**

1.  Click **"Memory Leak Mode"** button
    
2.  Click **"Test Single Request"** several times (5-6 times)
    
3.  Watch and point out:
    
    *   Memory Usage climbing (20MB → 40MB → 60MB...)
        
    *   Response time increasing (50ms → 200ms → 500ms...)
        
    *   Activity log showing warnings
        

### Scene 3: Slow Queries

**What to do:**

1.  Click **"Slow Query Mode"** button
    
2.  Click **"Test Single Request"**
    
3.  Watch it take 2-5 seconds to complete
    

### Scene 4: Full Cascade

**What to do:**

1.  Click **"Full Cascade Mode"** button
    
2.  Click **"Test Single Request"** multiple times
    
3.  Point out:
    
    *   Most requests failing (red errors in log)
        
    *   Success rate dropping to 30-40%
        
    *   Response times very high when successful
        
    *   Memory still climbing
        
    *   System Status indicator turns RED
        

### Scene 5: Recovery

**What to do:**

1.  Click **"Reset Everything"** button
    
2.  Wait 2-3 seconds
    
3.  Click **"Test Single Request"** a few times
    
4.  Show:
    
    *   Metrics reset
        
    *   Memory cleared
        
    *   Response times back to normal
        
    *   Success rate back to 100%
