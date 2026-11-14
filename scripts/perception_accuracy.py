import numpy as np
from sightloop.sim import Simulator
from sightloop.perception import perceive
from sightloop.state import ground_truth_state
from sightloop.tasks import generate_tasks

detected = total = 0
errs = []
for t in generate_tasks(40, 0)[:20]:
    with Simulator() as sim:
        sim.spawn_blocks(list(t.colors), seed=t.seed)
        truth = {s.color: s.position for s in ground_truth_state(sim)}
        seen = {s.color: s.position for s in perceive(sim)}
        for c, pos in truth.items():
            total += 1
            if c in seen:
                detected += 1
                errs.append(((seen[c][0]-pos[0])**2 + (seen[c][1]-pos[1])**2) ** 0.5)
print(f"detection rate: {detected}/{total} = {detected/total:.1%}")
print(f"mean xy error (detected): {np.mean(errs)*1000:.1f} mm")