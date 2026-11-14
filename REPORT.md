# SightLoop: A Failure-Aware Evaluation Harness for LLM-Driven Robot Manipulation

## Abstract
Large language models are increasingly used to drive robot manipulation: a model
reads a camera image, interprets a natural-language instruction, and calls
low-level controllers to move an arm. Such systems are usually reported with a
single task-success number, which conceals where the system actually fails.
SightLoop is a simulated tabletop pick-and-place environment built in PyBullet
with a Franka Panda arm, together with an evaluation harness whose purpose is to
attribute every failure to one of three stages (perception, planning, or control)
and to measure whether fault-aware recovery improves task completion over a
baseline that stops on the first failure. On a seeded set of stacking and
relative-placement tasks, task success is 81 percent under real perception and 100
percent under a perfect-perception oracle, a gap of 19 percentage points that
localizes most failures to perception. Planning is effectively solved, with 100
percent plan validity that is identical across three open models of different
sizes. Recovery raises completion under an injected mis-grasp from 0 percent to 88
percent. A central and initially counter-intuitive finding is that perception is
highly accurate in isolation, detecting every object with a mean position error of
2.8 mm, yet becomes fragile during manipulation because the arm occludes its own
camera.

## 1. Introduction
As language models are placed in control of physical systems, evaluation has not
kept pace with capability. A model that completes 80 percent of tasks may be
failing for entirely different reasons across that remaining 20 percent, and the
remedy for a perception failure (better sensing) is unrelated to the remedy for a
control failure (better grasping) or a planning failure (better instruction
following). Aggregate success rates and curated demonstrations do not separate
these causes, so they offer little engineering guidance about what to fix next.

SightLoop takes the position that the measurement, rather than the agent, is the
contribution. The system implements a complete but deliberately simple
manipulation agent, and surrounds it with a harness that isolates each stage
against an explicit baseline. The aim is not to maximize a success number but to
produce an honest, reproducible account of where and why an LLM-driven
manipulation agent breaks.

## 2. Method
### 2.1 Environment and agent
The environment is a Franka Panda arm positioned over a table holding three to
four colored blocks. The agent runs a five-stage loop. In Perceive, a rendered
camera image is converted to object identities and positions using color
segmentation followed by un-projection of image pixels to world coordinates
through the camera depth buffer. In Plan, a language model maps the instruction to
a list of structured tool calls drawn from a fixed interface (pick, place_on,
place_relative). In Act, each tool call is executed by driving the arm with inverse
kinematics. In Verify, every primitive returns a measured outcome, for example the
gripper finger width after a grasp or the achieved end-effector position, rather
than assuming the commanded action succeeded. In Recover, a failed step triggers
re-perception and a bounded retry.

### 2.2 Baselines
Two baselines make causal attribution possible. The oracle baseline replaces
perception with ground-truth object positions taken directly from the simulator,
so any improvement over the real-perception run is attributable to perception
error. The no-recovery baseline attempts each step exactly once and halts on the
first failure, so any improvement in the recovery condition is attributable to
recovery itself. Because perception is supplied to the agent through a single
injected function, switching between real perception and the oracle is a one-line
change that leaves every other part of the pipeline identical.

### 2.3 Fault injection
To study recovery, the harness injects controlled, reproducible faults. A
mis-grasp perturbs the grasp target laterally on a single attempt, so the gripper
closes beside the block and the fault is transient. An occlusion places a
visual-only plate between the camera and a target block, blinding perception while
leaving the physics untouched, so the fault is persistent and perception-specific.
A dropped-object fault releases the block after a successful grasp. Each fault is
pinned to a specific step and attempt so that runs remain deterministic.

### 2.4 Metrics
The harness reports plan validity (the fraction of plans that are syntactically
well formed and reference only existing objects and tools), task success (a
ground-truth goal check that is independent of what the agent believes it
achieved), perception accuracy against ground truth, recovery rate relative to the
no-recovery baseline, ambiguity detection together with a false-alarm rate on
unambiguous commands, and a failure taxonomy that counts perception, planning, and
control errors separately.

## 3. Experimental setup
A seeded generator produces stacking and relative-placement tasks with controlled
variation in object placement and clutter, along with a set of labeled ambiguous
commands paired with reference clarifications. Every episode is deterministic given
its seed, and the language model is queried at temperature zero with an on-disk
cache of prompt-to-reply pairs, so the complete evaluation is reproducible and
inexpensive to re-run. Development used a validation split, with a held-out split
reserved for a single final read. The default planner is the Groq free-tier model
openai/gpt-oss-20b, with qwen3.8-27b and openai/gpt-oss-120b used as cross-model
checks.

## 4. Results
| Condition or metric | Result |
|---|---|
| Plan validity | 100 percent |
| Task success, real perception | 81 percent |
| Task success, oracle | 100 percent |
| Perception gap | 19 points |
| Recovery under mis-grasp (none to recovery) | 0 to 88 percent |
| Perception detection rate and mean position error | 100 percent, 2.8 mm |
| Ambiguity detection and over-clarification | 100 percent, 0 percent |
| Failure taxonomy (perception, planning, control) | 3, 0, 18 |

Plan validity is perfect and, more tellingly, identical across all three models
regardless of size. Because the simulator, perception, and control are
deterministic given a plan, the only quantity a model can change is the plan
itself, so the identical downstream numbers show that for this task family
planning is not a limiting factor. Task success under real perception is 81
percent, while the oracle reaches 100 percent, locating the majority of failures
in perception. Under the injected mis-grasp, the no-recovery baseline never
completes the task, whereas the recovery condition completes 88 percent of
episodes, a direct demonstration that bounded retry with re-perception rescues
transient control faults.

## 5. Failure analysis
Three observations emerge from the raw logs.

First, perception is accurate in isolation but fragile during manipulation.
Measured on a clear table, perception detects every block with a mean position
error of 2.8 mm, yet the 19-point task gap is produced almost entirely by the arm
occluding its own top-down camera while reaching to place a block. The static
accuracy and the in-task gap are not contradictory, because they measure perception
at different moments, one before the arm enters the scene and one during active
manipulation.

Second, recovery addresses control faults but not perception faults. Retry with
re-perception resolves the transient mis-grasp, but it cannot resolve a persistent
occlusion, because looking again returns the same blocked view. The two residual
recovery failures are precisely the self-occlusion case, in which the arm cannot
clear the camera without releasing the block it is carrying.

Third, a failure's symptom is not its root cause. Several failures are reported
with control-stage reasons such as a slipped grasp or a failed descent, yet the
oracle, using identical control, succeeds on exactly those cases. The true origin
is a small perception error that shifted the target position enough to spoil the
grasp. This distinction is visible only because the harness compares against ground
truth rather than trusting the reported reason.

## 6. Limitations
The study uses a single top-down camera, which is the source of the self-occlusion
effect, and a second viewpoint or an active-perception policy would likely reduce
the perception gap. Perception is a classical color method rather than a learned
model, which is sufficient for solid colored blocks but would not transfer to
cluttered or textured scenes. The task family and object set are fixed, and the
evaluation set is modest in size. These constraints bound the generality of the
specific numbers, but not the evaluation method, which transfers to richer
environments.

## 7. Conclusion and future work
SightLoop shows that attributing failures to specific stages surfaces
engineering-relevant causes that a single success rate hides, including the
non-obvious result that a near-perfect perception module can still dominate
end-to-end failure once the manipulator enters its field of view. Planned
extensions include a second camera or active perception to address self-occlusion,
a learned or vision-language perception module evaluated against the classical
baseline, lighting-variation tasks, and parallel evaluation on cloud infrastructure
with cost and speedup reported.