# 🚀 SRE Failure Patterns Demo

A hands-on demo to **visually explain how small issues turn into big outages** — perfect for SRE talks, workshops, and live demos.

---

## 🧠 What This Code Does

This demo application:

- 🌐 Creates a **web server** using **Flask**
- 🧪 Allows you to **toggle different failure modes**
- 📊 Displays **real-time system metrics**
- 💥 Simulates:
  - Memory leaks
  - Slow queries
  - Cascading failures across the system

---

## 🛠️ Prerequisites

- ✅ Python **3.x**
- ✅ `pip3` installed

---

## 📦 Installation

### Step 1: Install `psutil`

We use `psutil` to monitor memory and system usage.

```bash
pip3 install psutil
```
### 📦 Step 2: Install Required Python Packages

Install the required dependencies using `pip`:

```bash
pip3 install flask flask-cors
```

## ▶️ Running the Demo

### 🚀 Step 1: Start the Server

Run the demo server:
```bash
python3 demo.py
```
### 📟 Expected Output
```bash
============================================================
🚀 SRE DEMO SERVER STARTING
============================================================
📍 Open your browser and go to: http://localhost:5000
⚠️  Press Ctrl+C to stop the server

* Running on http://0.0.0.0:5000
* Running on http://127.0.0.1:5000
============================================================
```
### 🌍 Step 2: Open Your Browser

Open Chrome / Firefox / Safari and visit:
```bash
http://localhost:5000
```

✅ You should see a colorful dashboard with:

### 📊 Live metrics

- 🎛️ Action buttons

- 📜 Real-time activity logs


## 🟢 Scene 1: Normal Operation

👉 What to Do

- Click “Test Single Request” 3–4 times

🔍 What to Expect

- ⏱️ Response time: ~10–50ms

- ✅ Success rate: 100%

- 🧠 Memory usage: Stable

- 📜 Activity log: All green checkmarks

## 🧠 Scene 2: Memory Leak

👉 What to Do

- Click “Memory Leak Mode”

- Click “Test Single Request” 5–6 times

🔍 What to Observe

- 📈 Memory usage climbing 20MB → 40MB → 60MB → ...

- ⏳ Response time increasing 50ms → 200ms → 500ms

- ⚠️ Warnings appearing in the activity log

## 🐌 Scene 3: Slow Queries

👉 What to Do

- Click “Slow Query Mode”

- Click “Test Single Request”

🔍 What to Observe

- 🕰️ Requests taking 2–5 seconds

- ⚠️ No errors — only increased latency

## 🔥 Scene 4: Full Cascade Failure

👉 What to Do

- Click “Full Cascade Mode”

- Click “Test Single Request” multiple times

🔍 What to Observe

- ❌ Most requests failing (red errors)

- 📉 Success rate dropping to 30–40%

- 🧠 Memory usage continuing to increase

- ⏱️ High response times for successful requests

- 🔴 System status indicator turning RED

## 🔄 Scene 5: Recovery

👉 What to Do

- Click “Reset Everything”

- Wait 2–3 seconds

- Click “Test Single Request” a few times

🔍 What to Observe

- ♻️ Metrics reset

- 🧹 Memory cleared

- ⚡ Response times back to normal

- ✅ Success rate restored to 100%