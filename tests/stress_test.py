import asyncio
import httpx
import time
from loguru import logger

BASE_URL = "http://localhost:8000/api/v1"

async def send_request(client, request_id):
    payload = {
        "prompt": f"Stress test prompt #{request_id}: Tell me a long story about AI.",
        "parameters": {"temperature": 0.7}
    }
    try:
        start = time.time()
        response = await client.post(f"{BASE_URL}/predict", json=payload)
        duration = time.time() - start
        if response.status_code == 200:
            return duration
        else:
            logger.error(f"Request {request_id} failed with status {response.status_code}")
            return None
    except Exception as e:
        logger.error(f"Request {request_id} error: {str(e)}")
        return None

async def run_stress_test(concurrency=10, total=50):
    logger.info(f"Starting stress test with concurrency={concurrency}, total={total}")
    async with httpx.AsyncClient(timeout=30.0) as client:
        start_time = time.time()
        tasks = []
        for i in range(total):
            tasks.append(send_request(client, i))
            if len(tasks) >= concurrency:
                await asyncio.gather(*tasks)
                tasks = []
        
        if tasks:
            await asyncio.gather(*tasks)
            
        total_duration = time.time() - start_time
        logger.success(f"Stress test finished. Total time: {total_duration:.2f}s, Avg throughput: {total/total_duration:.2f} req/s")

if __name__ == "__main__":
    # Simulate a high load
    asyncio.run(run_stress_test(concurrency=10, total=30))
