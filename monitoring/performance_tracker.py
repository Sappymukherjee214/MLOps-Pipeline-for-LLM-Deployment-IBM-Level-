import json
import time
from datetime import datetime
from loguru import logger

class PerformanceTracker:
    """Tracks and summarizes model performance trends."""
    
    def __init__(self, log_path: str = "logs/performance_reports.json"):
        self.log_path = log_path
        self.metrics_history = []
        self.summary_history = [] # Store history of summaries for charts

    def record_metrics(self, latency_ms: float, status: str):
        self.metrics_history.append({
            "timestamp": datetime.now().isoformat(),
            "latency_ms": latency_ms,
            "status": status
        })

    def generate_summary(self):
        """Generates a summary report with rolling averages and trends."""
        if not self.metrics_history:
            return {"status": "no_data"}

        # Use last 50 requests for rolling stats
        window = self.metrics_history[-50:]
        total_requests = len(window)
        failed_requests = sum(1 for m in window if m["status"] == "error")
        avg_latency = sum(m["latency_ms"] for m in window) / total_requests
        
        # Use current time for calculations
        now = datetime.now()
        
        # Calculate Throughput (RPM) based on actual time elapsed (max 5m)
        now_ts = now.timestamp()
        first_ts = datetime.fromisoformat(self.metrics_history[0]["timestamp"]).timestamp()
        time_elapsed_mins = (now_ts - first_ts) / 60
        
        # Use at least 0.1 minutes to avoid division by zero, max 5 minutes
        denominator = max(0.1, min(5.0, time_elapsed_mins))
        
        recent_reqs = [m for m in self.metrics_history if datetime.fromisoformat(m["timestamp"]).timestamp() > (now_ts - 300)]
        rpm = len(recent_reqs) / denominator

        summary = {
            "period_end": now.isoformat(),
            "display_time": now.strftime("%H:%M"),
            "window_size": total_requests,
            "error_rate": f"{(failed_requests/total_requests)*100:.2f}%",
            "avg_latency_ms": round(avg_latency, 2),
            "throughput_rpm": round(rpm, 1),
            "status": "operational" if failed_requests / total_requests < 0.1 else "degraded"
        }
        
        logger.info(f"Performance Summary Generated: {summary}")
        
        self.summary_history.append(summary)
        if len(self.summary_history) > 100:
            self.summary_history.pop(0)

        with open(self.log_path, "a") as f:
            f.write(json.dumps(summary) + "\n")
            
        return summary

    def get_history(self):
        return self.summary_history

performance_tracker = PerformanceTracker()
