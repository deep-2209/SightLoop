from sightloop.sim import Simulator
from sightloop.state import ground_truth_state
from sightloop.executor import execute
from sightloop.tasks import generate_tasks, check_goal, split_tasks


def test_generation_is_reproducible():
    a = generate_tasks(n=10, master_seed=0)
    b = generate_tasks(n=10, master_seed=0)
    assert [t.instruction for t in a] == [t.instruction for t in b]
    assert [t.seed for t in a] == [t.seed for t in b]


def test_val_and_test_sets_do_not_overlap():
    val, test = split_tasks(generate_tasks(n=20, master_seed=0))
    assert set(t.task_id for t in val).isdisjoint(t.task_id for t in test)


def test_goal_checker_confirms_a_real_stack():
    task = next(t for t in generate_tasks(60, 0) if t.goal.get("type") == "stack")
    plan = [{"tool": "pick", "args": {"color": task.goal["top"]}},
            {"tool": "place_on", "args": {"color": task.goal["bottom"]}}]
    with Simulator() as sim:
        sim.spawn_blocks(list(task.colors), seed=task.seed)
        log = execute(sim, plan, perceive_fn=ground_truth_state)
        assert log.success
        assert check_goal(sim, task.goal)