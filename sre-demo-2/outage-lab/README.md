# 🌍 Planet-Scale Outages Lab  
_Reproducing Real-World Failure Patterns from CrowdStrike, Cloudflare & AWS_

This repository contains a **hands-on SRE demo** that recreates **failure patterns behind some of the biggest global outages in the last 18 months**.

Instead of showing “a service going down”, this lab demonstrates **why systems fail even when infrastructure looks healthy**.

---

## 🎯 Demo Goals

This demo is designed to teach **incident thinking**, not just tools.

You will learn how:
- a *security change* can globally break production (CrowdStrike-style)
- a *safe change* can fail only at scale (Cloudflare-style)
- infrastructure can be healthy while users are broken (AWS-style)
- metrics can lie during partial outages
- the **wrong fix** makes outages worse
- the **right fix** is often a rollback, not a restart

> **Key takeaway:**  
> _Outages are not caused by bugs alone — they are caused by how fast changes move through systems._

---

## 🧠 Mental Model

Think of this app as a **tiny version of the internet**:

- Kubernetes = control plane
- Go service = edge / API layer
- ConfigMap = global config / security push
- Users = curl traffic

Kubernetes stays **green the entire time**.  
Users do not.

---

## 🏗 Architecture Overview

Client
|
| HTTP
v
Edge / API ← Feature flags & config rollout
|
v
Application Service
|
v
Simulated Dependencies (latency)


### Observability Truth
- Pods stay `Running`
- No crashes
- No restarts
- Failures happen **inside the request path**

---

## 🧰 Tech Stack

| Component        | Tool |
|-----------------|------|
| Language        | Go |
| Orchestration   | Kubernetes (kind) |
| Config Rollout  | ConfigMaps |
| Failure Type    | Config-driven logic |
| Traffic         | curl |

---

## ⚙️ How the Application Works

The Go service:
- reloads config every **5 seconds**
- applies feature flags dynamically
- never crashes
- never restarts
- fails requests **intentionally**

### Failure Hooks Inside the App

| Failure | Real Incident | Behavior |
|------|--------------|----------|
| Global block | CrowdStrike | 100% traffic fails |
| Partial failure | Cloudflare | ~30% traffic fails |
| Latency | AWS | Requests slow, no crashes |

---

## 🚀 Setup Instructions

### 1️⃣ Create a Local Kubernetes Cluster

```bash
kind create cluster --name outage-lab
```

### 2️⃣ Build and Load the Application Image

```bash 
docker build -t outage-app:latest app/
kind load docker-image outage-app:latest --name outage-lab
```

### 3️⃣ Deploy to Kubernetes

```bash 
kubectl apply -f k8s/
```

### 4️⃣ Expose the Service

```bash 
kubectl port-forward svc/outage-service -n outage-demo 8080:80
```

### 5️⃣ Generate Continuous Traffic

```bash 
while true; do
  curl -s -o /dev/null -w "%{http_code}\n" localhost:8080
  sleep 0.2
done
```
This simulates real user traffic.


## Scenario 1️⃣ — CrowdStrike-Style Global Failure

#### Action
```bash 
kubectl create configmap app-config -n outage-demo \
 --from-file=config.json=config/bad-security-rule.json \
 -o yaml --dry-run=client | kubectl apply -f -
```

#### What Happens

- No pods crash

- No restarts

- 100% user failure

## Scenario 2️⃣ — Cloudflare-Style Partial Failure

#### Action

```bash 
kubectl create configmap app-config -n outage-demo \
 --from-file=config.json=config/regex-feature.json \
 -o yaml --dry-run=client | kubectl apply -f -
```

#### What Happens

- ~70% success

- ~30% failure

- Averages look fine

## Scenario 3️⃣ — ❌ The Wrong Fix

#### Action

```bash 
kubectl rollout restart deploy outage-app -n outage-demo
```

#### What Happens

- Nothing improves

- Outage continues


## Scenario 4️⃣ — ✅ The Right Fix

#### Action

```bash 
kubectl create configmap app-config -n outage-demo \
 --from-file=config.json=config/good-config.json \
 -o yaml --dry-run=client | kubectl apply -f -
```

#### What Happens

- Immediate recovery

- No restarts needed
