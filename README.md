# Production-Grade MLOps Pipeline for LLM Deployment

This project demonstrates a real-world MLOps system for deploying, monitoring, and maintaining Large Language Model (LLM) applications.

## 🚀 System Architecture
- **Backend**: FastAPI (Python 3.11) with logic for inference, monitoring, and drift detection.
- **Frontend**: React + Vite + Tailwind CSS dashboard for real-time observability.
- **Infrastructure**: Dockerized (Multi-container setup with Docker Compose).
- **CI/CD**: GitHub Actions for automated testing and container building.

## 🛠️ Key Features
- **Inference Service**: Robust API with rate limiting, circuit breaking, and timeout handling.
- **Monitoring**: Real-time tracking of latency, throughput, and error rates using standard rolling averages.
- **Drift Detection**: Statistical drift detection using the Kolmogorov-Smirnov test on input distributions (prompt lengths).
- **Observability**: Production-grade logging with Loguru and a specialized log viewer in the dashboard.
- **Reliability**: Integrated Circuit Breaker pattern to handle LLM provider outages.

## 🏃 Getting Started

### Prerequisites
- Docker & Docker Compose
- Python 3.11+ (for local development)

### Running with Docker (Recommended)
```bash
docker-compose up --build
```
- Backend API: [http://localhost:8000](http://localhost:8000)
- Web Dashboard: [http://localhost:3000](http://localhost:3000)

### Local Development
1. **Backend**:
   ```bash
   pip install -r requirements.txt
   uvicorn app.main:app --reload
   ```
2. **Dashboard**:
   ```bash
   cd dashboard
   npm install
   npm run dev
   ```

## 📊 Performance Testing
To populate the dashboard with realistic data, run the simulation script:
```bash
python scripts/simulate_traffic.py
```

## 📂 Project Structure
- `app/`: FastAPI application routes and middleware.
- `monitoring/`: Core logic for drift detection and performance tracking.
- `dashboard/`: React source code and frontend assets.
- `deployment/`: Dockerfiles, Kubernetes manifests, and Prometheus config.
- `scripts/`: Reliability and traffic simulation scripts.
- `models/`: LLM provider integrations (Gemini, Mock).
