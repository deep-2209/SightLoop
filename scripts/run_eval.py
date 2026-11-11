from sightloop.batch import Condition, make_cached_llm, run_batch
from sightloop.faults import Fault
from sightloop.llm_groq import make_groq_llm
from sightloop.tasks import generate_tasks, split_tasks
# print("running")

CONDITIONS = [
    Condition("baseline"),                                        # real perception
    Condition("oracle", use_oracle=True),                         # isolate perception
    Condition("fault_norecover", max_attempts=1, fault=Fault("mis_grasp", 0)),
    Condition("fault_recover",   max_attempts=2, fault=Fault("mis_grasp", 0)),
]

llm = make_cached_llm(make_groq_llm(), "llm_cache.json", throttle=2.5)  # ~30 req/min
val, test = split_tasks(generate_tasks(n=40, master_seed=0))

print(f"running {len(val)} validation tasks x {len(CONDITIONS)} conditions...")
rows = run_batch(val, CONDITIONS, llm, "results_val.jsonl")
print(f"wrote {len(rows)} rows to results_val.jsonl")