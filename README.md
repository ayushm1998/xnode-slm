# XNode Smart Language Model (SLM) Integration

## Project Overview
This project demonstrates the **seamless integration of a language model with XNode’s workflow system**, enabling intelligent intent classification, real-time communication, and performance visualization through an interactive dashboard.

It unifies **Angular**, **Node.js**, **FastAPI**, and **Dash** to create an AI-driven workflow routing prototype for multi-agent communication and intent understanding.

---

## Architecture Overview

```
[Angular UI] 
     ↓
[Node.js Server (Express)] 
     ↓
[FastAPI Model Backend (PyTorch + Transformers)]
     ↓
[Metrics Store] 
     ↓
[Dash Visualization Dashboard]
```

| Layer | Technology | Description |
|--------|-------------|-------------|
| **Frontend** | Angular | User interface for text inputs and displaying model predictions |
| **Middleware** | Node.js | Routes API requests between UI and backend |
| **Backend** | FastAPI + PyTorch | Handles model inference and metrics tracking |
| **Visualization** | Dash (Plotly) | Displays accuracy, latency, and workflow efficiency metrics |

---

## Intent Categories

| Intent | Description | Example |
|--------|--------------|----------|
| greeting | User greetings | “hi”, “good morning” |
| complaint | Issues or dissatisfaction | “this is not working”, “bad service” |
| feedback | User opinions | “great job”, “this could be better” |
| inquiry | Information requests | “how does this work?” |
| request | Action-based requests | “please reset my password” |
| apology | Expressions of regret | “sorry about that”, “my apologies” |

---

## One-Command Setup (Recommended)

You can start the **entire system** — backend, middleware, frontend, and dashboard — in **one go** using the provided script.

### Run Everything
```bash
chmod +x run.sh
./run.sh
```

This script will:
- Create and activate a Python virtual environment  
- Install required Python and Node.js dependencies  
- Start the **FastAPI backend** (port `5000`)  
- Start the **Node.js middleware** (port `3000`)  
- Start the **Angular frontend** (port `4200`)  
- Start the **Dash dashboard** (port `8050`)  
- Open all services automatically in your browser  

> Press **Ctrl + C** anytime to stop all running services.

---

## Manual Setup (Optional)

If you prefer to run each layer manually, follow these steps:

### FastAPI Backend (Intent Model)
```bash
cd model-python
source .venv/bin/activate
pip install -r requirements.txt
uvicorn src.server:app --reload --port 5000
```
**Endpoints:**  
- `/predict` → Predict intent  
- `/metrics` → Model metrics  

---

### Node.js Middleware
```bash
cd node-server
npm install
node server.js
```
**Proxies:**  
- `/api/predict` → Forwards to FastAPI  
- `/api/metrics/summary` → Aggregates metrics  

---

### Angular Frontend
```bash
cd ui-angular
npm install
npm start
```
Open → [http://localhost:4200](http://localhost:4200)

---

### Dash Visualization Dashboard
```bash
cd dashboard
source ../model-python/.venv/bin/activate
python3 app.py
```
Open → [http://localhost:8050](http://localhost:8050)

> If the dashboard shows “⚠️ No metrics yet,” send a few messages via the frontend to generate live data.

---

## Example Prediction

**Input:**
```bash
curl -X POST http://127.0.0.1:5000/predict      -H "Content-Type: application/json"      -d '{"text": "sorry for the delay"}'
```

**Response:**
```json
{
  "intent": "apology",
  "confidence": 0.86,
  "message": "I’m sorry for the inconvenience."
}
```

---

## Dashboard Metrics

The **Dash dashboard** provides live visualization of:
- **Accuracy by Intent**
- **Agent Latency (ms)**
- **Workflow Efficiency**
- **Total Predictions Processed**

Metrics update dynamically as new predictions are made through the system.

---

## Tech Stack

| Layer | Tools / Frameworks |
|-------|--------------------|
| Backend | FastAPI, PyTorch, Transformers |
| Middleware | Node.js, Express |
| Frontend | Angular |
| Visualization | Dash, Plotly |
| Data | Synthetic intent dataset |
| Model | DistilBERT (fine-tuned) |

---

## Troubleshooting

| Issue | Possible Fix |
|--------|---------------|
| `Address already in use` | Run `kill -9 $(lsof -ti:5000)` |
| `ModuleNotFoundError` | Activate venv: `source model-python/.venv/bin/activate` |
| Dashboard blank | Send a few intents via the Angular UI |
| Angular CORS error | Ensure FastAPI `CORSMiddleware` allows all origins |

---

## Contributor

**Ayush Mehta**  
M.S. Computer Science, California State University, Sacramento  

- [Portfolio](https://ayushmehta.info)  
- [LinkedIn](https://www.linkedin.com/in/ayushm98)

---

## Submission Checklist

- `run.sh` launches all components automatically  
- Model achieves **≥ 85% accuracy** on validation data  
- Dashboard visualizes live metrics after message flow  
- README, logs, and screenshots included for evaluation  


---

**Final Notes:**  
This project demonstrates a complete ML workflow pipeline, from training to inference, middleware integration, and real-time performance monitoring, fully automatable through `run.sh`.
