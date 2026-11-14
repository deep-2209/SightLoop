"""Batch runner: sweep tasks x conditions, record raw rows, cache LLM calls."""
import hashlib
import json
import os
import time
from dataclasses import dataclass

from sightloop.executor import execute
from sightloop.faults import Fault, inject_scene_fault
from sightloop.perception import perceive
from sightloop.planner import plan
from sightloop.sim import Simulator
from sightloop.state import ground_truth_state
from sightloop.tasks import check_goal


@dataclass(frozen=True)
class Condition:
    name: str
    use_oracle: bool = False
    max_attempts: int = 1
    fault: Fault = None


def make_cached_llm(llm_fn, cache_path, throttle=0.0):
    """Wrap an llm_fn with an on-disk prompt->reply cache. Only uncached calls
    hit the network (and wait `throttle` seconds, for rate limits)."""
    cache = {}
    if os.path.exists(cache_path):
        with open(cache_path, encoding="utf-8") as f:
            cache = json.load(f)

    def wrapped(prompt: str) -> str:
        key = hashlib.sha256(prompt.encode("utf-8")).hexdigest()
        if key in cache:
            return cache[key]
        reply = llm_fn(prompt)
        cache[key] = reply
        with open(cache_path, "w", encoding="utf-8") as f:
            json.dump(cache, f)
        if throttle:
            time.sleep(throttle)
        return reply

    return wrapped


def _primary_color(task):
    return task.goal.get("top") or task.goal.get("moved") or "red"


def run_batch(tasks, conditions, llm_fn, out_path):
    """Run every executable task under every condition; write JSONL rows."""
    rows = []
    for task in tasks:
        if task.ambiguous:
            continue  # ambiguous tasks are scored by the ambiguity metric, not run
        for cond in conditions:
            fault = cond.fault
            if fault is not None:   # resolve the per-task occlusion target
                fault = Fault(fault.kind, fault.step, _primary_color(task))
            with Simulator() as sim:
                sim.spawn_blocks(list(task.colors), seed=task.seed)
                initial = {s.color: (s.position[0], s.position[1])
                           for s in ground_truth_state(sim)}
                inject_scene_fault(sim, fault)
                perceive_fn = ground_truth_state if cond.use_oracle else perceive
                colors = {o.color for o in perceive_fn(sim)}
                parsed, validation = plan(task.instruction, colors, llm_fn)

                row = {"task_id": task.task_id, "condition": cond.name,
                       "plan_valid": validation.valid}
                if validation.valid:
                    log = execute(sim, parsed, perceive_fn=perceive_fn,
                                  max_attempts=cond.max_attempts, fault=fault)
                    row["episode_success"] = log.success
                    row["goal_success"] = check_goal(sim, task.goal, initial)
                    row["reasons"] = [s.reason for s in log.steps]
                    row["attempts"] = [s.attempts for s in log.steps]
                else:
                    row.update(episode_success=False, goal_success=False,
                               reasons=["invalid_plan"], attempts=[])
                rows.append(row)

    with open(out_path, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r) + "\n")
    return rows