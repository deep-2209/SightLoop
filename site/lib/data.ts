// Single source of truth for every number and claim on the page.
// Only real project data lives here. Do not invent values.

export const REPO_URL = "https://github.com/deep-2209/SightLoop";

export const thesis =
  "A vision-grounded LLM agent for tabletop manipulation, built so the deliverable is not the demo. It is the measurement.";

export const researchQuestion =
  "In LLM-driven robot manipulation, where do failures come from (perception, planning, or control), and does fault-aware recovery improve task completion over a no-recovery baseline?";

export type LoopStage = {
  id: string;
  index: number;
  name: string;
  verb: string;
  description: string;
  failureMode: string;
};

export const loopStages: LoopStage[] = [
  {
    id: "perceive",
    index: 0,
    name: "Perceive",
    verb: "camera to world",
    description:
      "A top-down camera image is turned into block colors and positions through color segmentation and depth un-projection.",
    failureMode:
      "The arm occludes its own top-down view mid-task, so a block that was seen cleanly becomes invisible exactly when it matters.",
  },
  {
    id: "plan",
    index: 1,
    name: "Plan",
    verb: "LLM reasons",
    description:
      "The LLM reads the scene and the natural-language instruction, then emits structured tool calls rather than free-form text.",
    failureMode:
      "Malformed or invalid plans. In practice this did not happen: plan validity was 100 percent across every model tested.",
  },
  {
    id: "act",
    index: 2,
    name: "Act",
    verb: "controllers move",
    description:
      "Inverse-kinematics controllers execute the plan as low-level pick and place primitives on the Franka Panda arm.",
    failureMode:
      "Slipped grasps and failed descents. The most common fault class by count, though not always the true root cause.",
  },
  {
    id: "verify",
    index: 3,
    name: "Verify",
    verb: "measure, not assume",
    description:
      "The outcome is measured against the ground-truth goal state rather than assumed from the plan having run.",
    failureMode:
      "A silent success that never checks reality. Verification is what makes every other number on this page trustworthy.",
  },
  {
    id: "recover",
    index: 4,
    name: "Recover",
    verb: "re-perceive, retry",
    description:
      "On a transient failure the agent re-perceives the scene and retries, closing the loop instead of ending on the first fault.",
    failureMode:
      "Recovery rescues transient control faults but cannot fix a block that stays occluded. It is not a cure for perception.",
  },
];

export type Metric = {
  id: string;
  label: string;
  value: number;
  suffix: string;
  decimals?: number;
  note: string;
  tone?: "signal" | "alert" | "flux" | "neutral";
};

export const metrics: Metric[] = [
  {
    id: "plan-validity",
    label: "Plan validity",
    value: 100,
    suffix: "%",
    note: "Identical across gpt-oss-20b, qwen3.8-27b, and gpt-oss-120b. Planning is not the bottleneck.",
    tone: "signal",
  },
  {
    id: "success-real",
    label: "Task success, real perception",
    value: 81,
    suffix: "%",
    note: "End-to-end completion with the real perception stack in the loop.",
    tone: "neutral",
  },
  {
    id: "success-oracle",
    label: "Task success, perfect-perception oracle",
    value: 100,
    suffix: "%",
    note: "With a perfect-perception oracle, every task completes. The ceiling is perception.",
    tone: "flux",
  },
  {
    id: "perception-gap",
    label: "Perception gap",
    value: 19,
    suffix: " pts",
    note: "The distance between real perception and the oracle. This is the number the project is about.",
    tone: "alert",
  },
  {
    id: "detection",
    label: "Block detection",
    value: 100,
    suffix: "%",
    note: "Every block detected on a clear table.",
    tone: "signal",
  },
  {
    id: "pos-error",
    label: "Mean position error",
    value: 2.8,
    suffix: " mm",
    decimals: 1,
    note: "Accurate to millimeters in isolation, before the arm enters the frame.",
    tone: "flux",
  },
  {
    id: "ambiguity",
    label: "Ambiguity detection",
    value: 100,
    suffix: "%",
    note: "With 0 percent false alarms on clear commands.",
    tone: "signal",
  },
];

export const recovery = {
  without: 0,
  with: 88,
  context: "Under an identical injected mis-grasp.",
};

export const perceptionGap = {
  real: 81,
  oracle: 100,
  gap: 19,
};

export type FailureClass = {
  stage: string;
  count: number;
  tone: "signal" | "alert" | "flux";
  note: string;
};

export const failureTaxonomy: FailureClass[] = [
  { stage: "Perception", count: 3, tone: "flux", note: "Occlusion and small position errors." },
  { stage: "Planning", count: 0, tone: "signal", note: "No planning faults observed." },
  { stage: "Control", count: 18, tone: "alert", note: "Slips and failed descents, by label." },
];

export const models = ["gpt-oss-20b", "qwen3.8-27b", "gpt-oss-120b"];

export type Finding = {
  n: string;
  title: string;
  body: string;
  pull: string;
};

export const findings: Finding[] = [
  {
    n: "01",
    title: "Perception is accurate in isolation, fragile during manipulation.",
    body:
      "On a clear table the perception stack detects every block to within 2.8 mm. Yet the 19-point task gap comes from the arm occluding its own top-down camera mid-task. The same sensor that is near-perfect at rest is blinded by the very motion it exists to guide.",
    pull: "2.8 mm at rest, 19 points lost in motion.",
  },
  {
    n: "02",
    title: "Recovery fixes control faults, not perception faults.",
    body:
      "Retry-with-re-perception rescues a transient mis-grasp, lifting success from 0 to 88 percent. But it cannot fix a block that stays hidden behind the arm. Recovery closes the loop on transient control faults and leaves persistent occlusion untouched.",
    pull: "0 to 88 percent on transient faults. Zero help for occlusion.",
  },
  {
    n: "03",
    title: "A failure's symptom is not its root cause.",
    body:
      "Some failures labeled as control errors, a slipped grasp or a failed descent, are fixed by the perfect-perception oracle. That reveals a small perception error as the true cause. Attributing failure by symptom would have blamed the controllers for a sensing problem.",
    pull: "The oracle fixes faults that looked like control.",
  },
];

export const methodology = [
  {
    k: "Baselines that isolate one stage",
    v: "A perfect-perception oracle isolates perception; a no-recovery condition isolates recovery. Each baseline changes exactly one thing so a gap can be attributed.",
  },
  {
    k: "Controlled fault injection",
    v: "Faults such as the mis-grasp are injected deliberately and identically across conditions, so the only variable is whether recovery is allowed to run.",
  },
  {
    k: "Ground-truth goal checks",
    v: "Every task is scored against the true simulator state, not against the plan or the agent's own report. Verification is measured, never assumed.",
  },
  {
    k: "Deterministic, reproducible runs",
    v: "Tasks are seeded and deterministic, and LLM calls are cached, so a run reproduces exactly rather than drifting with sampling.",
  },
];

export const limitations = [
  {
    title: "Single top-down camera",
    body:
      "One overhead viewpoint is the structural cause of self-occlusion. When the arm is over the workspace, it is between the camera and the blocks.",
  },
  {
    title: "Classical color perception",
    body:
      "Perception is color segmentation plus depth un-projection. It is precise on clear scenes but has no notion of objects it cannot currently see.",
  },
];

export const futureWork = [
  "Learned or VLM-based perception that reasons about occluded objects",
  "A second camera to remove the single-viewpoint blind spot",
  "Cloud-parallel evaluation to scale the harness across many more seeds",
];

export const demo = {
  success: {
    src: "/success.gif",
    label: "Clean pick-and-place",
    caption: "The loop runs start to finish. Perceive, plan, act, verify, done.",
  },
  failure: {
    src: "/failure.gif",
    label: "Injected mis-grasp, no recovery",
    caption: "A deliberate mis-grasp with recovery disabled. The loop ends on the fault.",
  },
};
