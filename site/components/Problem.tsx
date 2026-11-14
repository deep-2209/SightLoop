"use client";

import { Section, SectionHeader, Reveal } from "./primitives";

const contrasts = [
  {
    k: "A demo",
    v: "tells you it worked once.",
    d: "A single successful run is an existence proof, not a measurement. It says nothing about how often, or why the other times fail.",
  },
  {
    k: "A score",
    v: "tells you how often.",
    d: "An aggregate success rate is honest but blunt. 81 percent means 19 percent fails, and the number alone cannot say which stage broke.",
  },
  {
    k: "Attribution",
    v: "tells you which stage broke.",
    d: "Holding perception, planning, and control apart turns a single number into a diagnosis you can act on.",
  },
];

export default function Problem() {
  return (
    <Section id="problem">
      <SectionHeader
        index="02"
        kicker="The problem"
        title="A success rate is a symptom. Attribution is a diagnosis."
        intro="An LLM reads a camera image, interprets an instruction like stack the red block on the green block, and drives a simulated Franka Panda arm. When the whole pipeline is scored end to end, a failure could live anywhere in it. Stage-attributed evaluation is the difference between knowing that the agent failed and knowing where."
      />

      <div className="mt-16 grid gap-px overflow-hidden rounded-xl border border-line bg-line sm:grid-cols-3">
        {contrasts.map((c, i) => (
          <Reveal key={c.k} delay={i * 0.08}>
            <div className="h-full bg-panel p-7 transition-colors hover:bg-panel2">
              <div className="font-mono text-sm text-signal">{String(i + 1).padStart(2, "0")}</div>
              <p className="mt-4 text-xl font-medium leading-snug">
                <span className="text-chalk">{c.k}</span>{" "}
                <span className="text-fog">{c.v}</span>
              </p>
              <p className="mt-3 text-sm leading-relaxed text-ash">{c.d}</p>
            </div>
          </Reveal>
        ))}
      </div>

      <Reveal delay={0.1}>
        <p className="mx-auto mt-16 max-w-2xl text-center font-mono text-sm leading-relaxed text-fog">
          So SightLoop is built as a harness first and a demo second. Every stage
          is instrumented, every outcome is checked against ground truth, and
          every failure is traced back to the stage that actually caused it, not
          the stage where it surfaced.
        </p>
      </Reveal>
    </Section>
  );
}
