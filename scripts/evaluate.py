"""One-command evaluation: run the batch on the validation set and report."""
from sightloop.batch import Condition, make_cached_llm, run_batch
from sightloop.faults import Fault
from sightloop.llm_groq import make_groq_llm
from sightloop.tasks import generate_tasks, split_tasks
from sightloop.metrics import (
    plan_validity_rate, success_by_condition, recovery_rate, failure_taxonomy)

CONDITIONS = [
    Condition("baseline"),
    Condition("oracle", use_oracle=True),
    Condition("fault_norecover", max_attempts=1, fault=Fault("mis_grasp", 0)),
    Condition("fault_recover",   max_attempts=2, fault=Fault("mis_grasp", 0)),
]


def main():
    llm = make_cached_llm(make_groq_llm(), "llm_cache.json", throttle=2.5)
    val, _ = split_tasks(generate_tasks(n=40, master_seed=0))
    rows = run_batch(val, CONDITIONS, llm, "results_val.jsonl")

    sc = success_by_condition(rows)
    nr, rec = recovery_rate(rows)
    print(f"plan validity:        {plan_validity_rate(rows):.0%}")
    for c in ["baseline", "oracle", "fault_norecover", "fault_recover"]:
        print(f"  {c:16} {sc[c]:.0%}")
    print(f"perception gap:       {sc['oracle'] - sc['baseline']:.0%}")
    print(f"recovery under fault: {nr:.0%} -> {rec:.0%}")
    print(f"failure taxonomy:     {failure_taxonomy(rows)}")


if __name__ == "__main__":
    main()