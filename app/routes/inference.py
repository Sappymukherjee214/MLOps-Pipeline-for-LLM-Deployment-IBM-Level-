import time
import asyncio
from fastapi import APIRouter, Request, HTTPException, BackgroundTasks
from pydantic import BaseModel, Field
from typing import Dict, Any

from configs.settings import settings
from models.llm_provider import get_llm_provider
from monitoring.drift_detection import drift_detector
from monitoring.performance_tracker import performance_tracker
from utils.circuit_breaker import llm_circuit_breaker
from loguru import logger

router = APIRouter()

class PredictRequest(BaseModel):
    prompt: str = Field(..., min_length=1)
    parameters: Dict[str, Any] = Field(default_factory=dict)

class PredictResponse(BaseModel):
    response: str
    model: str
    latency_ms: float
    status: str = "success"

async def background_monitoring(prompt: str, latency_ms: float, status: str):
    """Processes monitoring data in the background to minimize user latency."""
    drift_detector.add_data(len(prompt))
    performance_tracker.record_metrics(latency_ms, status)
    logger.debug(f"Background monitoring completed for prompt length: {len(prompt)}")

@router.post("/predict", response_model=PredictResponse)
async def predict(request: Request, input_data: PredictRequest, background_tasks: BackgroundTasks):
    logger.info(f"Inference request received: {input_data.prompt[:50]}...")
    
    start_time = time.time()
    
    async def run_inference():
        provider = get_llm_provider(
            provider_type=settings.LLM_PROVIDER,
            api_key=settings.GEMINI_API_KEY,
            model_name=settings.MODEL_NAME
        )
        return await provider.generate(input_data.prompt, **input_data.parameters)

    try:
        # Wrap inference in Circuit Breaker with a 30s timeout
        result = await asyncio.wait_for(
            llm_circuit_breaker.call(run_inference),
            timeout=30.0
        )
        
        latency_ms = (time.time() - start_time) * 1000
        
        # Offload monitoring to background tasks
        background_tasks.add_task(background_monitoring, input_data.prompt, latency_ms, "success")
        
        return PredictResponse(
            response=result["text"],
            model=result["model"],
            latency_ms=latency_ms
        )
    except Exception as e:
        logger.error(f"Inference failure: {str(e)}")
        background_tasks.add_task(performance_tracker.record_metrics, 0, "error")
        raise HTTPException(status_code=503, detail="Service unstable or model provider failure")
