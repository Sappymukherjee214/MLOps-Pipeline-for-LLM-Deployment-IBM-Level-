import time
from enum import Enum
from loguru import logger
from typing import Callable, Any

class State(Enum):
    CLOSED = "CLOSED"
    OPEN = "OPEN"
    HALF_OPEN = "HALF_OPEN"

class CircuitBreaker:
    """Implementation of the Circuit Breaker pattern for remote service calls."""
    
    def __init__(self, failure_threshold: int = 5, recovery_timeout: int = 60):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.state = State.CLOSED
        self.failures = 0
        self.last_failure_time = 0

    async def call(self, func: Callable, *args, **kwargs) -> Any:
        if self.state == State.OPEN:
            if time.time() - self.last_failure_time > self.recovery_timeout:
                logger.info("CircuitBreaker: Recovery timeout reached. Switching to HALF_OPEN.")
                self.state = State.HALF_OPEN
            else:
                raise Exception("CircuitBreaker is OPEN. Request rejected.")

        try:
            result = await func(*args, **kwargs)
            if self.state == State.HALF_OPEN:
                logger.info("CircuitBreaker: Success in HALF_OPEN. Switching to CLOSED.")
                self.reset()
            return result
        except Exception as e:
            self.failures += 1
            self.last_failure_time = time.time()
            logger.warning(f"CircuitBreaker: Failure registered ({self.failures}/{self.failure_threshold}).")
            
            if self.failures >= self.failure_threshold:
                logger.error("CircuitBreaker: Failure threshold reached. Switching to OPEN.")
                self.state = State.OPEN
            
            raise e

    def reset(self):
        self.state = State.CLOSED
        self.failures = 0
        self.last_failure_time = 0

# Global instance for LLM inference
llm_circuit_breaker = CircuitBreaker()
