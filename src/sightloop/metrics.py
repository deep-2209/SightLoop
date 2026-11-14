"""Compute reported metrics and the failure taxonomy from batch result rows."""
import json

FAILURE_CATEGORY = {
    "target_not_perceived": "perception",
    "invalid_plan": "planning",
    "unknown_tool": "planning",
    "gripper_empty": "control", "slipped": "control", "dropped": "control",
    "descend_failed": "control", "approach_failed": "control",
    "not_reached": "control", "ik_out_of_limits": "control",
    "retreat_failed": "control", "release_failed": "control",
    "not_holding": "control",
}


def load_rows(path):
    with open(path, encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def _mean(xs):
    xs = list(xs)
    return sum(xs) / len(xs) if xs else 0.0


def plan_validity_rate(rows):
    return _mean(r["plan_valid"] for r in rows)


def success_by_condition(rows):
    out = {}
    for r in rows:
        out.setdefault(r["condition"], []).append(r["goal_success"])
    return {c: _mean(v) for c, v in out.items()}


def recovery_rate(rows):
    byc = success_by_condition(rows)
    return byc.get("fault_norecover", 0.0), byc.get("fault_recover", 0.0)


def failure_taxonomy(rows, condition=None):
    counts = {"perception": 0, "planning": 0, "control": 0, "other": 0}
    for r in rows:
        if condition and r["condition"] != condition:
            continue
        if r["goal_success"]:
            continue
        reason = next((x for x in reversed(r["reasons"]) if x != "ok"), None)
        if reason is None:                      # executed as planned, goal not met
            counts["planning"] += 1
            continue
        counts[FAILURE_CATEGORY.get(reason, "other")] += 1
    return counts

def ambiguity_scores(records):
    """records: [{ambiguous: bool, clarified: bool}]. Returns (detection, false_alarm)."""
    amb = [r for r in records if r["ambiguous"]]
    clear = [r for r in records if not r["ambiguous"]]
    detection = _mean(r["clarified"] for r in amb) if amb else 0.0
    false_alarm = _mean(r["clarified"] for r in clear) if clear else 0.0
    return detection, false_alarm