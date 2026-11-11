from sightloop.batch import Condition, run_batch
from sightloop.tasks import Task


def test_run_batch_writes_rows(tmp_path):
    task = Task("t0", "stack the red block on the green block",
                ("red", "green", "yellow"), 0,
                {"type": "stack", "top": "red", "bottom": "green"})
    plan_json = ('[{"tool":"pick","args":{"color":"red"}},'
                 '{"tool":"place_on","args":{"color":"green"}}]')
    fake = lambda prompt: plan_json
    out = tmp_path / "res.jsonl"

    rows = run_batch([task], [Condition("oracle", use_oracle=True)], fake, str(out))
    assert len(rows) == 1
    assert rows[0]["plan_valid"] and rows[0]["goal_success"] is True
    assert out.exists()