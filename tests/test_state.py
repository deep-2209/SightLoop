import pybullet as p

from sightloop.sim import Simulator
from sightloop.state import ground_truth_state


def test_ground_truth_matches_simulator():
    with Simulator() as sim:
        sim.spawn_blocks(["red", "green", "yellow"], seed=0)
        states = ground_truth_state(sim)
        assert {s.color for s in states} == {"red", "green", "yellow"}
        for s in states:
            pos, _ = p.getBasePositionAndOrientation(
                sim.blocks[s.color], physicsClientId=sim.client
            )
            assert abs(s.position[0] - round(pos[0], 4)) < 1e-6