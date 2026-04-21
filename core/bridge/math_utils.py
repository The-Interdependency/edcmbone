# core/bridge/math_utils.py
from __future__ import annotations

from typing import List
from math import sqrt

def l1(a: List[float], b: List[float]) -> float:
    return sum(abs(x-y) for x, y in zip(a, b))

def pearson(x: List[float], y: List[float]) -> float:
    n = len(x)
    if n < 2 or n != len(y):
        return 0.0
    mx = sum(x)/n
    my = sum(y)/n
    num = sum((xi-mx)*(yi-my) for xi, yi in zip(x, y))
    denx = sqrt(sum((xi-mx)**2 for xi in x))
    deny = sqrt(sum((yi-my)**2 for yi in y))
    if denx == 0 or deny == 0:
        return 0.0
    return max(-1.0, min(1.0, num/(denx*deny)))
