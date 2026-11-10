from sightloop.sim import Simulator
from sightloop.state import ground_truth_state
from sightloop.perception import perceive

with Simulator() as sim:
    sim.spawn_blocks(["red", "green", "yellow"], seed=0)
    truth = {s.color: s.position for s in ground_truth_state(sim)}
    seen = {s.color: s.position for s in perceive(sim)}
    print("detected colors:", sorted(seen))
    for color in truth:
        if color not in seen:
            print(f"{color:7} MISSED"); continue
        tx, ty, _ = truth[color]
        px, py, _ = seen[color]
        err = ((px - tx) ** 2 + (py - ty) ** 2) ** 0.5
        print(f"{color:7} truth=({tx:.3f},{ty:.3f}) seen=({px:.3f},{py:.3f}) err={err:.4f}")