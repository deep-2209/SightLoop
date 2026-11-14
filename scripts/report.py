from sightloop.metrics import (
    load_rows, plan_validity_rate, success_by_condition,
    recovery_rate, failure_taxonomy)

rows = load_rows("results_val.jsonl")
sc = success_by_condition(rows)

print("plan validity:", f"{plan_validity_rate(rows):.1%}")
print("task success by condition:")
for c, s in sc.items():
    print(f"  {c:16} {s:.1%}")
print("perception gap (oracle - baseline):", f"{sc['oracle'] - sc['baseline']:.1%}")
nr, rec = recovery_rate(rows)
print(f"recovery under fault: {nr:.1%} (none) -> {rec:.1%} (recovery)")
print("failure taxonomy (per condition):")
for c in ["baseline", "oracle", "fault_norecover", "fault_recover"]:
    print(f"  {c:16}", failure_taxonomy(rows, c))