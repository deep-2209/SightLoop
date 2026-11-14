import os
from sightloop.sim import Simulator
from sightloop.perception import perceive
from sightloop.executor import execute
from sightloop.faults import Fault

os.makedirs("gifs", exist_ok=True)
PLAN = [{"tool": "pick", "args": {"color": "red"}},
        {"tool": "place_on", "args": {"color": "green"}}]

# Clean success
with Simulator() as sim:
    sim.spawn_blocks(["red", "green", "yellow"], seed=0)
    sim.start_recording(every=15)
    execute(sim, PLAN, perceive_fn=perceive)
    sim.save_gif("gifs/success.gif")
    print("success frames:", len(sim.frames))

# Injected mis-grasp, no recovery -> failure
with Simulator() as sim:
    sim.spawn_blocks(["red", "green", "yellow"], seed=0)
    sim.start_recording(every=15)
    execute(sim, PLAN, perceive_fn=perceive, max_attempts=1,
            fault=Fault("mis_grasp", 0))
    sim.save_gif("gifs/failure.gif")
    print("failure frames:", len(sim.frames))