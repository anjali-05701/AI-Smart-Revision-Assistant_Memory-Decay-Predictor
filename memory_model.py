"""
Memory Prediction Model — exponential forgetting curve.
R(t) = e^(-k * t)  (retention after t days)
Higher k = faster forgetting (harder concepts).
"""
import math

# Forgetting rate k by difficulty (tune for demo: retention ~60% after a few days for Medium)
K_BY_DIFFICULTY = {
    "Easy": 0.20,
    "Medium": 0.30,
    "Hard": 0.45,
}


def forgetting_rate(difficulty: str) -> float:
    return K_BY_DIFFICULTY.get(difficulty.strip().title(), 0.30)


def memory_retention(days: float, difficulty: str = "Medium") -> float:
    """Retention in [0, 1] after `days` since last review/study."""
    if days < 0:
        days = 0.0
    k = forgetting_rate(difficulty)
    return math.exp(-k * days)


def retention_percent(days: float, difficulty: str = "Medium") -> float:
    return memory_retention(days, difficulty) * 100.0
