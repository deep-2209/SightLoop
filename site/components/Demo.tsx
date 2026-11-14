"use client";

import { Section, SectionHeader, Reveal } from "./primitives";
import { demo } from "@/lib/data";

const clips = [
  { ...demo.success, tone: "signal" as const, tag: "SUCCESS" },
  { ...demo.failure, tone: "alert" as const, tag: "FAILURE" },
];

export default function Demo() {
  return (
    <Section id="demo">
      <SectionHeader
        index="04"
        kicker="See it work, and fail"
        title="The same loop, two outcomes."
        intro="On the left, the loop runs clean. On the right, a mis-grasp is injected and recovery is switched off, so the run ends on the fault. Both are the real simulator, not a mockup."
      />

      <div className="mt-16 grid gap-6 lg:grid-cols-2">
        {clips.map((c, i) => {
          const accent =
            c.tone === "signal"
              ? "border-signal/30"
              : "border-alert/30";
          const dot = c.tone === "signal" ? "bg-signal" : "bg-alert";
          const text = c.tone === "signal" ? "text-signal" : "text-alert";
          return (
            <Reveal key={c.label} delay={i * 0.1}>
              <figure
                className={`group overflow-hidden rounded-2xl border ${accent} bg-panel`}
              >
                <div className="flex items-center justify-between border-b border-line px-5 py-3">
                  <div className="flex items-center gap-2.5">
                    <span className={`h-2 w-2 rounded-full ${dot}`} />
                    <span className="font-mono text-sm text-chalk">
                      {c.label}
                    </span>
                  </div>
                  <span className={`font-mono text-[0.65rem] tracking-label ${text}`}>
                    {c.tag}
                  </span>
                </div>

                <div className="relative aspect-video overflow-hidden bg-void">
                  {/* eslint-disable-next-line @next/next/no-img-element */}
                  <img
                    src={c.src}
                    alt={`${c.label}. ${c.caption}`}
                    loading="lazy"
                    className="h-full w-full object-contain"
                  />
                  <div className="pointer-events-none absolute inset-0 ring-1 ring-inset ring-white/5" />
                </div>

                <figcaption className="px-5 py-4 text-sm leading-relaxed text-fog">
                  {c.caption}
                </figcaption>
              </figure>
            </Reveal>
          );
        })}
      </div>
    </Section>
  );
}
