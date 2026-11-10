"""Ground-truth world state. EVALUATION ONLY — perception must never read this."""
from dataclasses import dataclass

import pybullet as p


@dataclass(frozen=True)
class ObjectState:
    color: str
    position: tuple[float, float, float]


def ground_truth_state(sim) -> list[ObjectState]:
    """Exact block colors and positions from the simulator. The answer key
    for the oracle baseline, the perception metric, and verification."""
    states = []
    for color, body_id in sim.blocks.items():
        pos, _ = p.getBasePositionAndOrientation(body_id, physicsClientId=sim.client)
        states.append(ObjectState(color, tuple(round(v, 4) for v in pos)))
    return states