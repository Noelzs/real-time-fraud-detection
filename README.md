# Real-Time Fraud Detection

A proof-of-concept fraud detection system that identifies suspicious credit card transactions in real-time. Built to demonstrate how machine learning can catch fraud without annoying legitimate customers.
**Achieves 50,000+ transactions/second** through intelligent batch processing - matching production payment processor scale.

> Note: This is a proof-of-concept, not a production system. It's designed to show what's possible, not handle millions of transactions.
This is a full-stack **real-time fraud detection system** combining Python backend with React frontend.  
The project simulates and tracks transactions in real-time, predicts fraudulent activity using ML models, and presents an interactive dashboard.

---

## Update (Feb 2026)

Project reorganized into a **monorepo structure** for improved clarity and maintainability:  

- `backend/` — All ML model code, training scripts, and versioned models  
- `frontend/` — React-based real-time dashboard  

This restructure improves project clarity, maintainability, and demonstrates professional software practices.
Originally, the backend was a standalone repo: [real-time-fraud-detection-engine](https://github.com/Noelzs/real-time-fraud-detection-engine).

---

## Repository Structure
real-time-fraud-detection/
│
├─ backend/ # Python backend with ML models and utilities
├─ frontend/ # React frontend with real-time dashboard
├─ .gitignore
└─ README.md

---

## Backend

Python FastAPI backend serving ML models via WebSocket.

### Keyfiles
- **`main.py`** - FastAPI server with WebSocket endpoints  
- **`train_model.py`** - Model training pipeline 
- **`real_model.py`** - Final model wrapper
- **`model_utils.py`** - Model versioning utilities
- **`stress_test_beta.py`** - Performance testing(beta)

Model versions (model_versions/)
v1 → v4: experimental/vanity models
`v5_xg_20251109_154848`: This was our final model and the system is designed to use this model

Exploratory data analysis plots (plot_figures/)
All plotting scripts used during EDA and model evaluation

---

## Frontend - Real-Time Dashboard

React dashboard with WebSocket connection to backend.

### Features
- Real-time transaction streaming
- Dual mode: Simulation vs Real XGBoost
- "Interesting Only" transaction filter
- Live performance metrics
- Fixed optimal threshold (0.063)

## Quick Start

### 1. **Get the Data**
First, grab the dataset from [IEEE-CIS Fraud Detection on Kaggle](https://www.kaggle.com/c/ieee-fraud-detection).
You'll need these files:
- train_transaction.csv
- train_identity.csv

Put them in your project folder.

### 2. **Setup**
# Install what you need
pip install -r requirements.txt

### 3. **Train Your First Model**
python train_model.py

This creates two models:

Random Forest - Reliable, explainable
XGBoost - Fast, sophisticated

### 4. **Confirm the models are functioning**
python run_model.py

### 5. **Launch the system**
Open two terminals:

**Terminal 1 (Backend):**
cd backend
python main.py

**Terminal 2 (Frontend):**
cd frontend
npm install  # only first time
npm start

Then open http://localhost:3000 in your browser
---

## Features

### Backend
- **Dual Engine**: Simulation + Real XGBoost model
- **WebSocket Streaming**: Real-time transaction feed
- **Batch Processing**: 50,000+ transactions/second
- **Model Versioning**: Track experiments systematically

### Frontend
- **Live Dashboard**: Real-time transaction monitoring
- **Dual Display Modes**: "All" vs "Interesting Only"
- **Performance Metrics**: Detection rate, speed, alerts
- **Business Context**: Indian Rupee display in the simulation, fixed threshold

## Performance

| Metric | Value |
|--------|-------|
| Fraud Detection | 39.7% |
| False Alarms | 8.8% |
| Processing Speed | 50,000+ tx/sec (batch) |
| Model AUC | 0.77 |
| Threshold | 0.063 (business-optimized) |

## Tech Stack

### Backend
- FastAPI (WebSocket + REST)
- XGBoost / scikit-learn
- Pandas / NumPy
- Python 3.9+

### Frontend
- React 18
- TailwindCSS
- WebSocket API
- Recharts (for potential future graphs)
