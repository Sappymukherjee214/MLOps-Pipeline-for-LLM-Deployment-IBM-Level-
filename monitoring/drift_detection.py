import numpy as np
import pandas as pd
from scipy.stats import ks_2samp
from loguru import logger
from typing import List, Dict, Any, Optional
from datetime import datetime

class StatisticalDriftDetector:
    """Advanced drift detection using Kolmogorov-Smirnov test."""
    
    def __init__(self, baseline_data: List[float], window_size: int = 200, p_value_threshold: float = 0.05):
        self.baseline = np.array(baseline_data)
        self.window_size = window_size
        self.p_value_threshold = p_value_threshold
        self.current_window = []
        self.drift_history = []

    def add_data(self, value: float):
        self.current_window.append(value)
        if len(self.current_window) > self.window_size:
            self.current_window.pop(0)

    def calculate_drift(self) -> Dict[str, Any]:
        """Performs KS-Test to compare current window with baseline."""
        if len(self.current_window) < self.window_size // 2:
            return {"status": "insufficient_data"}

        # Perform 2-sample KS test
        statistic, p_value = ks_2samp(self.baseline, self.current_window)
        
        drift_detected = p_value < self.p_value_threshold
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "drift_detected": bool(drift_detected),
            "ks_statistic": float(statistic),
            "p_value": float(p_value),
            "current_window_mean": float(np.mean(self.current_window)),
            "baseline_mean": float(np.mean(self.baseline))
        }

        if drift_detected:
            logger.critical(f"ALERT: Statistical Drift Detected! P-value: {p_value:.4f}")
            
        self.drift_history.append(report)
        if len(self.drift_history) > 100:
            self.drift_history.pop(0)
            
        return report

    def get_history(self) -> List[Dict[str, Any]]:
        return self.drift_history

# Reference baseline: typical prompt lengths
baseline_prompt_lengths = np.random.normal(loc=150, scale=30, size=500).tolist()
drift_detector = StatisticalDriftDetector(baseline_data=baseline_prompt_lengths)
