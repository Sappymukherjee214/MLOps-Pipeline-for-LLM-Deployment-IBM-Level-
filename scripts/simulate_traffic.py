import requests
import time
import random
import concurrent.futures
from loguru import logger

API_URL = "http://localhost:8000/api/v1/predict"

PROMPTS = [
    "What is MLOps?",
    "Explain quantum computing simply.",
    "How do I build a production API?",
    "Tell me a joke about robots.",
    "What is the capital of France?",
    "Write a short poem about AI monitoring.",
    "How to detect data drift in LLMs?",
    "Short summary of Kubernetes.",
    "Why is logging important in production?",
    "Translate 'Hello World' to 5 languages."
]

def send_request(i):
    prompt = random.choice(PROMPTS)
    # Occasionally send very long prompts to simulate varied traffic
    if random.random() > 0.8:
        prompt = prompt * 10
        
    try:
        start_time = time.time()
        response = requests.post(API_URL, json={"prompt": prompt}, timeout=15)
        latency = (time.time() - start_time) * 1000
        
        if response.status_code == 200:
            logger.info(f"Req {i}: Success | Latency: {latency:.2f}ms")
        else:
            logger.warning(f"Req {i}: Failed with status {response.status_code}")
    except Exception as e:
        logger.error(f"Req {i}: Error: {str(e)}")

def simulate_traffic(num_requests=50, max_workers=5):
    logger.info(f"Starting traffic simulation: {num_requests} requests with {max_workers} workers...")
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(send_request, i) for i in range(num_requests)]
        concurrent.futures.wait(futures)
        
    logger.info("Traffic simulation completed.")

if __name__ == "__main__":
    simulate_traffic()
