"use client";

import { motion, useReducedMotion } from "framer-motion";
import { Section, SectionHeader, Reveal } from "./primitives";
import AnimatedCounter from "./AnimatedCounter";
import {
  metrics,
  recovery,
  perceptionGap,
  failureTaxonomy,
} from "@/lib/data";

const toneText: Record<string, string> = {
  signal: "text-signal",
  alert: "text-alert",
  flux: "text-flux",
  neutral: "text-chalk",
};
const toneBar: Record<string, string> = {
  signal: "bg-signal",
  alert: "bg-alert",
  flux: "bg-flux",
};

const EASE = [0.16, 1, 0.3, 1] as const;

function GrowBar({
  pct,
  colorClass,
  delay = 0,
  vertical = false,
}: {
  pct: number;
  colorClass: string;
  delay?: number;
  vertical?: boolean;
}) {
  const reduce = useReducedMotion();
  const dim = vertical ? { height: `${pct}%` } : { width: `${pct}%` };
  return (
    <motion.div
      className={`${colorClass} rounded-full`}
      style={vertical ? { width: "100%" } : { height: "100%" }}
      initial={reduce ? dim : vertical ? { height: 0 } : { width: 0 }}
      whileInView={dim}
      viewport={{ once: true, margin: "-15%" }}
      transition={{ duration: 1.2, delay, ease: EASE }}
    />
  );
}

export default function Results() {
  return (
    <Section id="results">
      <SectionHeader
        index="05"
        kicker="Results"
        title="What the harness measured."
        intro="Every number here is read from a deterministic, seeded run with cached model calls. Nothing is averaged across a demo reel."
      />

      {/* Metric tiles */}
      <div className="mt-16 grid gap-px overflow-hidden rounded-2xl border border-line bg-line sm:grid-cols-2 lg:grid-cols-3">
        {metrics.map((m, i) => (
          <Reveal key={m.id} delay={(i % 3) * 0.06}>
            <div className="h-full bg-panel p-7 transition-colors hover:bg-panel2">
              <div className="label text-ash">{m.label}</div>
              <div
                className={`mt-4 font-mono text-5xl font-semibold tracking-tight ${
                  toneText[m.tone ?? "neutral"]
                }`}
              >
                <AnimatedCounter value={m.value} decimals={m.decimals ?? 0} />
                <span className="text-3xl">{m.suffix}</span>
              </div>
              <p className="mt-4 text-sm leading-relaxed text-fog">{m.note}</p>
            </div>
          </Reveal>
        ))}
      </div>

      {/* Recovery before / after */}
      <Reveal>
        <div className="mt-8 overflow-hidden rounded-2xl border border-line bg-panel">
          <div className="flex flex-wrap items-center justify-between gap-2 border-b border-line px-7 py-4">
            <h3 className="font-mono text-sm text-chalk">
              Recovery under an injected mis-grasp
            </h3>
            <span className="label text-ash">{recovery.context}</span>
          </div>

          <div className="grid gap-px bg-line md:grid-cols-[1fr_auto_1fr]">
            {/* without */}
            <div className="bg-void p-8 sm:p-10">
              <div className="label text-alert">Without recovery</div>
              <div className="mt-3 font-mono text-6xl font-semibold text-alert">
                <AnimatedCounter value={recovery.without} />%
              </div>
              <div className="mt-6 h-3 w-full overflow-hidden rounded-full bg-ink">
                <GrowBar pct={recovery.without} colorClass={toneBar.alert} />
              </div>
              <p className="mt-4 text-sm text-fog">
                The loop ends on the first fault. Nothing retries.
              </p>
            </div>

            {/* arrow */}
            <div className="flex items-center justify-center bg-panel px-6 py-4">
              <div className="text-center">
                <div className="font-mono text-2xl text-signal">+88</div>
                <div className="label mt-1 text-ash">points</div>
              </div>
            </div>

            {/* with */}
            <div className="bg-void p-8 sm:p-10">
              <div className="label text-signal">With recovery</div>
              <div className="mt-3 font-mono text-6xl font-semibold text-signal">
                <AnimatedCounter value={recovery.with} />%
              </div>
              <div className="mt-6 h-3 w-full overflow-hidden rounded-full bg-ink">
                <GrowBar pct={recovery.with} colorClass={toneBar.signal} delay={0.15} />
              </div>
              <p className="mt-4 text-sm text-fog">
                Re-perceive and retry rescues the transient mis-grasp.
              </p>
            </div>
          </div>
        </div>
      </Reveal>

      {/* Two charts */}
      <div className="mt-8 grid gap-8 lg:grid-cols-2">
        {/* Perception gap */}
        <Reveal>
          <div className="h-full rounded-2xl border border-line bg-panel p-7">
            <h3 className="font-mono text-sm text-chalk">
              The perception gap
            </h3>
            <p className="mt-2 text-sm text-fog">
              Real perception versus a perfect-perception oracle. The distance is
              the whole project.
            </p>

            <div className="mt-8 flex items-end gap-8">
              <div className="flex flex-1 items-end gap-6" style={{ height: 180 }}>
                {/* real */}
                <div className="flex h-full flex-1 flex-col items-center justify-end">
                  <span className="mb-2 font-mono text-xl text-chalk">
                    <AnimatedCounter value={perceptionGap.real} />%
                  </span>
                  <div className="flex w-full items-end" style={{ height: "100%" }}>
                    <div className="w-full self-end" style={{ height: `${perceptionGap.real}%` }}>
                      <GrowBar pct={100} colorClass="bg-chalk/80" vertical />
                    </div>
                  </div>
                  <span className="mt-3 text-center font-mono text-[0.65rem] tracking-label text-ash">
                    REAL
                  </span>
                </div>
                {/* oracle */}
                <div className="flex h-full flex-1 flex-col items-center justify-end">
                  <span className="mb-2 font-mono text-xl text-flux">
                    <AnimatedCounter value={perceptionGap.oracle} />%
                  </span>
                  <div className="flex w-full items-end" style={{ height: "100%" }}>
                    <div className="w-full self-end" style={{ height: `${perceptionGap.oracle}%` }}>
                      <GrowBar pct={100} colorClass="bg-flux" vertical delay={0.15} />
                    </div>
                  </div>
                  <span className="mt-3 text-center font-mono text-[0.65rem] tracking-label text-ash">
                    ORACLE
                  </span>
                </div>
              </div>

              <div className="flex flex-col items-center justify-center rounded-xl border border-alert/30 bg-alert/5 px-5 py-6">
                <span className="font-mono text-4xl font-semibold text-alert">
                  <AnimatedCounter value={perceptionGap.gap} />
                </span>
                <span className="label mt-1 text-center text-alert/80">
                  point gap
                </span>
              </div>
            </div>
          </div>
        </Reveal>

        {/* Failure taxonomy */}
        <Reveal delay={0.08}>
          <div className="h-full rounded-2xl border border-line bg-panel p-7">
            <h3 className="font-mono text-sm text-chalk">
              Failure taxonomy, by count
            </h3>
            <p className="mt-2 text-sm text-fog">
              Where faults land by label. Note: the label is not always the root
              cause.
            </p>

            <div className="mt-8 space-y-5">
              {failureTaxonomy.map((f, i) => {
                const max = 18;
                const pct = f.count === 0 ? 0 : (f.count / max) * 100;
                return (
                  <div key={f.stage}>
                    <div className="mb-2 flex items-baseline justify-between">
                      <span className="font-mono text-sm text-chalk">
                        {f.stage}
                      </span>
                      <span className={`font-mono text-sm ${toneText[f.tone]}`}>
                        {f.count}
                      </span>
                    </div>
                    <div className="h-3 w-full overflow-hidden rounded-full bg-ink">
                      {f.count === 0 ? (
                        <div className="flex h-full items-center pl-2 font-mono text-[0.6rem] text-ash">
                          none observed
                        </div>
                      ) : (
                        <GrowBar
                          pct={pct}
                          colorClass={toneBar[f.tone]}
                          delay={i * 0.1}
                        />
                      )}
                    </div>
                    <p className="mt-1.5 text-xs text-ash">{f.note}</p>
                  </div>
                );
              })}
            </div>
          </div>
        </Reveal>
      </div>
    </Section>
  );
}
