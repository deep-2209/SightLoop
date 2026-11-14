"""Parameterized, reproducible evaluation tasks + a ground-truth goal checker."""
from dataclasses import dataclass

import numpy as np

from sightloop.faults import Fault
from sightloop.state import ground_truth_state

COLORS_ALL = ["red", "green", "yellow", "orange"]  # orange = clutter/distractor


@dataclass(frozen=True)
class Task:
    task_id: str
    instruction: str
    colors: tuple          # blocks to spawn
    seed: int              # placement seed
    goal: dict             # structured goal for check_goal; {} if ambiguous
    ambiguous: bool = False
    reference_clarification: str = ""   # gold answer for ambiguous tasks
    fault: Fault = None


def check_goal(sim, goal, initial=None) -> bool:
    """Ground-truth task success. `initial` = {color: (x, y)} at spawn, used to
    confirm the agent actually moved the block (not that it was already placed)."""
    if not goal:
        return False
    gt = {s.color: s.position for s in ground_truth_state(sim)}
    if goal["type"] == "stack":
        top, bottom = gt[goal["top"]], gt[goal["bottom"]]
        near = ((top[0] - bottom[0]) ** 2 + (top[1] - bottom[1]) ** 2) ** 0.5 < 0.03
        return near and top[2] > 0.05
    if goal["type"] == "relative":
        moved, ref = gt[goal["moved"]], gt[goal["reference"]]
        dx, dy = moved[0] - ref[0], moved[1] - ref[1]
        on_side = {"left": dy > 0.04, "right": dy < -0.04,
                   "back": dx > 0.04, "front": dx < -0.04}[goal["direction"]]
        if not on_side:
            return False
        if initial is not None:                       # require the agent moved it
            ix, iy = initial[goal["moved"]]
            if ((moved[0] - ix) ** 2 + (moved[1] - iy) ** 2) ** 0.5 < 0.03:
                return False
        return True
    return False


AMBIGUOUS = [
    ("move the block", "Which block should I move - red, green, or yellow?"),
    ("put it to the side", "Which block, and to which side?"),
    ("stack the blocks", "Which block on which, and in what order?"),
]


def generate_tasks(n=60, master_seed=0):
    """n executable tasks (stack + relative, varying placement & clutter),
    followed by the labeled ambiguous tasks."""
    rng = np.random.default_rng(master_seed)
    tasks, i = [], 0
    while len(tasks) < n:
        n_blocks = 4 if i % 3 == 0 else 3            # clutter: a 4th distractor
        colors = tuple(COLORS_ALL[:n_blocks])
        seed = int(rng.integers(0, 10_000))
        a, b = (str(c) for c in rng.permutation(colors[:3])[:2])  # referenced pair
        if i % 2 == 0:
            tasks.append(Task(f"stack-{i:03d}",
                f"stack the {a} block on the {b} block", colors, seed,
                {"type": "stack", "top": a, "bottom": b}))
        else:
            d = str(rng.choice(["left", "right", "front", "back"]))
            tasks.append(Task(f"rel-{i:03d}",
                f"put the {a} block to the {d} of the {b} block", colors, seed,
                {"type": "relative", "moved": a, "reference": b, "direction": d}))
        i += 1

    for j, (instr, clar) in enumerate(AMBIGUOUS):
        tasks.append(Task(f"amb-{j:03d}", instr, ("red", "green", "yellow"),
                          int(rng.integers(0, 10_000)), {},
                          ambiguous=True, reference_clarification=clar))
    return tasks


def split_tasks(tasks, val_fraction=0.4):
    """Deterministic validation/test split. Tune on val, read test once."""
    executable = [t for t in tasks if not t.ambiguous]
    k = int(len(executable) * val_fraction)
    return executable[:k], executable[k:]      # (validation, test)