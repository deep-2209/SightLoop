"use client";

import { Section, SectionHeader, Reveal } from "./primitives";
import { limitations, futureWork } from "@/lib/data";

export default function Limitations() {
  return (
    <Section id="limitations">
      <SectionHeader
        index="08"
        kicker="Limitations & future work"
        title="What this harness cannot yet see."
        intro="The headline result is a perception ceiling, and the design that produced it is also its main constraint. Naming that honestly is part of the measurement."
      />

      <div className="mt-16 grid gap-8 lg:grid-cols-[1.1fr_0.9fr]">
        {/* Limitations */}
        <div className="space-y-5">
          {limitations.map((l, i) => (
            <Reveal key={l.title} delay={i * 0.08}>
              <div className="rounded-2xl border border-line bg-panel p-7">
                <div className="flex items-center gap-2.5">
                  <span className="h-2 w-2 rounded-full bg-alert" />
                  <h3 className="font-mono text-sm text-chalk">{l.title}</h3>
                </div>
                <p className="mt-3 leading-relaxed text-fog">{l.body}</p>
              </div>
            </Reveal>
          ))}
        </div>

        {/* Future work */}
        <Reveal delay={0.1}>
          <div className="h-full rounded-2xl border border-signal/20 bg-gradient-to-b from-signal/[0.04] to-transparent p-7">
            <div className="label text-signal-dim">Future work</div>
            <ul className="mt-5 space-y-5">
              {futureWork.map((w, i) => (
                <li key={i} className="flex gap-4">
                  <span className="mt-1 font-mono text-xs text-signal">
                    {String(i + 1).padStart(2, "0")}
                  </span>
                  <span className="leading-relaxed text-chalk/90">{w}</span>
                </li>
              ))}
            </ul>
          </div>
        </Reveal>
      </div>
    </Section>
  );
}
