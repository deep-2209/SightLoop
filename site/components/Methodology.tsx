"use client";

import { Section, SectionHeader, Reveal } from "./primitives";
import { methodology, models } from "@/lib/data";

export default function Methodology() {
  return (
    <Section id="method">
      <SectionHeader
        index="07"
        kicker="Methodology"
        title="How each number is made trustworthy."
        intro="The design goal is attribution. Every choice below exists so a change in one number can be traced to one cause."
      />

      <div className="mt-16 grid gap-px overflow-hidden rounded-2xl border border-line bg-line md:grid-cols-2">
        {methodology.map((m, i) => (
          <Reveal key={m.k} delay={(i % 2) * 0.08}>
            <div className="h-full bg-panel p-8">
              <div className="flex items-center gap-3">
                <span className="font-mono text-sm text-signal">
                  {String(i + 1).padStart(2, "0")}
                </span>
                <span className="h-px flex-1 bg-line" />
              </div>
              <h3 className="mt-4 text-lg font-semibold">{m.k}</h3>
              <p className="mt-3 text-sm leading-relaxed text-fog">{m.v}</p>
            </div>
          </Reveal>
        ))}
      </div>

      <Reveal delay={0.1}>
        <div className="mt-8 flex flex-wrap items-center gap-x-6 gap-y-3 rounded-2xl border border-line bg-panel px-7 py-5">
          <span className="label text-ash">Models evaluated</span>
          {models.map((m) => (
            <span
              key={m}
              className="rounded-full border border-line px-3 py-1 font-mono text-xs text-chalk"
            >
              {m}
            </span>
          ))}
          <span className="font-mono text-xs text-signal-dim">
            100% plan validity, identical across all three
          </span>
        </div>
      </Reveal>
    </Section>
  );
}
