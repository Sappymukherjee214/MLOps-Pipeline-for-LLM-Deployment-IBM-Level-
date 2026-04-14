from fastapi import APIRouter
from monitoring.drift_detection import drift_detector
from monitoring.performance_tracker import performance_tracker
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from fastapi.responses import Response

router = APIRouter()

@router.get("/metrics")
async def metrics():
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)

@router.get("/drift")
async def get_drift():
    return drift_detector.calculate_drift()

@router.get("/performance/summary")
async def get_performance_summary():
    return performance_tracker.generate_summary()

@router.get("/performance/history")
async def get_performance_history():
    return performance_tracker.get_history()

@router.get("/drift/history")
async def get_drift_history():
    return drift_detector.get_history()

@router.get("/dashboard")
async def get_dashboard():
    """Aggregated dashboard view for production monitoring."""
    return {
        "drift": drift_detector.calculate_drift(),
        "performance": performance_tracker.generate_summary(),
        "system": "operational"
    }
