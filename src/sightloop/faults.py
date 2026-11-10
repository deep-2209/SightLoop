"""Controlled, reproducible fault injection for evaluation."""
from dataclasses import dataclass

MISGRASP_OFFSET = 0.04  # meters sideways on the afflicted attempt -> grasp misses


@dataclass(frozen=True)
class Fault:
    kind: str = "none"   # "none" | "mis_grasp"  (occlusion, dropped come next)
    step: int = 0        # which plan-step index to afflict