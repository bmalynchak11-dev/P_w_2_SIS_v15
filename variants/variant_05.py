"""Варіант 15 (Задача 5, набір 3).

Фронт Парето та пояснення домінування альтернатив.
"""
from typing import Any, Dict, List


def _dominates(a_metrics: Dict[str, Any], b_metrics: Dict[str, Any], directions: Dict[str, str]) -> bool:
    """Перевіряє, чи варіант A домінує варіант B.

    Варіант A домінує B, якщо за кожним критерієм A не гірший за B,
    і хоча б за одним критерієм A строго кращий за B.
    """
    strictly_better = False

    for crit, direction in directions.items():
        val_a = a_metrics[crit]
        val_b = b_metrics[crit]

        if direction == "min":
            if val_a > val_b:  # A гірший за B
                return False
            if val_a < val_b:  # A строго кращий за B
                strictly_better = True
        elif direction == "max":
            if val_a < val_b:  # A гірший за B
                return False
            if val_a > val_b:  # A строго кращий за B
                strictly_better = True

    return strictly_better


def explain(options: Dict[str, Dict[str, Any]], directions: Dict[str, str]) -> Dict[str, List[str]]:
    """Повертає словник {домінований_варіант: [ті, хто його домінують]}.

    Ключі та списки зберігають вихідний порядок options.
    """
    if not options or not directions:
        return {}

    result: Dict[str, List[str]] = {}
    option_names = list(options.keys())

    for target_name in option_names:
        dominators: List[str] = []
        target_metrics = options[target_name]

        for other_name in option_names:
            if target_name == other_name:
                continue
            other_metrics = options[other_name]
            if _dominates(other_metrics, target_metrics, directions):
                dominators.append(other_name)

        if dominators:
            result[target_name] = dominators

    return result


def pareto_front(options: Dict[str, Dict[str, Any]], directions: Dict[str, str]) -> List[str]:
    """Повертає назви недомінованих варіантів у порядку options."""
    if not options:
        return []

    dominated_dict = explain(options, directions)
    return [name for name in options.keys() if name not in dominated_dict]