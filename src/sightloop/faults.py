"""Controlled, reproducible fault injection for evaluation."""
from dataclasses import dataclass
import pybullet as p

MISGRASP_OFFSET = 0.04  # meters sideways on the afflicted attempt -> grasp misses


@dataclass(frozen=True)
class Fault:
    kind: str = "none"   # "none" | "mis_grasp"  (occlusion, dropped come next)
    step: int = 0        # which plan-step index to afflict
    target: str = ""     # color to occlude (occlusion only) Occlusion: The camera cannot see the object.

def inject_scene_fault(sim, fault):
    """Scene-level faults, applied after spawn and before the episode runs.
    Only occlusion today: a fixed plate above the target blocks the camera."""
    if fault is None or fault.kind != "occlusion":
        return
    bid = sim.blocks.get(fault.target)
    if bid is None:
        return
    pos, _ = p.getBasePositionAndOrientation(bid, physicsClientId=sim.client)
    half = [0.05, 0.05, 0.002]                       # 10 cm plate over a 5 cm block
    col = p.createCollisionShape(p.GEOM_BOX, halfExtents=half, physicsClientId=sim.client)
    vis = p.createVisualShape(p.GEOM_BOX, halfExtents=half,
                              rgbaColor=[0.2, 0.2, 0.2, 1], physicsClientId=sim.client)
    p.createMultiBody(baseMass=0, baseCollisionShapeIndex=-1,     # mass 0 = static
                      baseVisualShapeIndex=vis,
                      basePosition=[pos[0], pos[1], 0.20],         # between camera and block
                      physicsClientId=sim.client)