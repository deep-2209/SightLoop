from sightloop.sim import Simulator
from sightloop.state import ground_truth_state
from sightloop.perception import perceive


def test_perception_detects_all_blocks_near_truth():
    for seed in range(3):
        with Simulator() as sim:
            sim.spawn_blocks(["red", "green", "yellow"], seed=seed)
            truth = {s.color: s.position for s in ground_truth_state(sim)}
            seen = {s.color: s.position for s in perceive(sim)}
            assert set(seen) == set(truth)  # all found, none invented
            for color in truth:
                tx, ty, _ = truth[color]
                px, py, _ = seen[color]
                assert ((px - tx) ** 2 + (py - ty) ** 2) ** 0.5 < 0.02