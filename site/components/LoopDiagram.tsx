"use client";

import { AnimatePresence, motion, useReducedMotion } from "framer-motion";
import { useState } from "react";
import { Section, SectionHeader } from "./primitives";
import { loopStages } from "@/lib/data";

export default function LoopDiagram() {
  const [active, setActive] = useState(0);
  const reduce = useReducedMotion();
  const stage = loopStages[active];

  const onKey = (e: React.KeyboardEvent) => {
    if (e.key === "ArrowRight" || e.key === "ArrowDown") {
      e.preventDefault();
      setActive((a) => (a + 1) % loopStages.length);
    } else if (e.key === "ArrowLeft" || e.key === "ArrowUp") {
      e.preventDefault();
      setActive((a) => (a - 1 + loopStages.length) % loopStages.length);
    }
  };

  return (
    <Section id="loop">
      <SectionHeader
        index="03"
        kicker="The agent loop"
        title="Five stages, one closed loop."
        intro="Each stage does one job and has one characteristic way of failing. Hover, tap, or use the arrow keys to inspect a stage and the failure mode that lives there."
      />

      {/* Stepper */}
      <div
        role="tablist"
        aria-label="Agent loop stages"
        onKeyDown={onKey}
        className="relative mt-16"
      >
        {/* connecting line */}
        <div className="pointer-events-none absolute left-0 right-0 top-6 hidden h-px bg-line md:block" />
        <div className="pointer-events-none absolute left-0 top-6 hidden h-px bg-gradient-to-r from-signal to-signal/0 md:block"
          style={{ width: `${(active / (loopStages.length - 1)) * 100}%`, transition: "width .5s cubic-bezier(.16,1,.3,1)" }}
        />

        <div className="grid grid-cols-2 gap-y-8 sm:grid-cols-3 md:flex md:justify-between">
          {loopStages.map((s, i) => {
            const isActive = i === active;
            return (
              <button
                key={s.id}
                role="tab"
                aria-selected={isActive}
                aria-controls="loop-detail"
                tabIndex={isActive ? 0 : -1}
                onClick={() => setActive(i)}
                onMouseEnter={() => setActive(i)}
                onFocus={() => setActive(i)}
                className="group relative z-10 flex flex-col items-center gap-3 text-center outline-none md:w-24"
              >
                <span
                  className={`flex h-12 w-12 items-center justify-center rounded-full border font-mono text-sm transition-all duration-300 ${
                    isActive
                      ? "border-signal bg-signal text-ink shadow-[0_0_22px_rgba(191,255,60,0.35)]"
                      : "border-line bg-ink text-fog group-hover:border-signal/50 group-hover:text-chalk"
                  }`}
                >
                  {String(i + 1).padStart(2, "0")}
                </span>
                <span
                  className={`font-mono text-xs tracking-wide transition-colors ${
                    isActive ? "text-chalk" : "text-ash group-hover:text-fog"
                  }`}
                >
                  {s.name}
                </span>
              </button>
            );
          })}
        </div>

        {/* loop-back hint */}
        <div className="mt-6 flex items-center justify-center gap-2 font-mono text-[0.68rem] uppercase tracking-label text-ash">
          <span className="h-px w-6 bg-line" />
          Recover re-enters Perceive. The loop closes.
          <span className="h-px w-6 bg-line" />
        </div>
      </div>

      {/* Detail panel */}
      <div
        id="loop-detail"
        role="tabpanel"
        className="mt-10 overflow-hidden rounded-2xl border border-line bg-panel"
      >
        <AnimatePresence mode="wait">
          <motion.div
            key={stage.id}
            initial={reduce ? false : { opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            exit={reduce ? undefined : { opacity: 0, y: -12 }}
            transition={{ duration: 0.35, ease: [0.16, 1, 0.3, 1] }}
            className="grid gap-px bg-line md:grid-cols-2"
          >
            {/* what it does */}
            <div className="bg-panel p-8 sm:p-10">
              <div className="label text-signal-dim">
                Stage {String(active + 1).padStart(2, "0")} // {stage.verb}
              </div>
              <h3 className="mt-4 text-3xl font-semibold tracking-tight">
                {stage.name}
              </h3>
              <p className="mt-4 leading-relaxed text-fog">{stage.description}</p>
            </div>

            {/* failure mode */}
            <div className="relative bg-void p-8 sm:p-10">
              <div className="label flex items-center gap-2 text-alert">
                <span className="h-2 w-2 rounded-full bg-alert" />
                Characteristic failure mode
              </div>
              <p className="mt-4 leading-relaxed text-chalk/90">
                {stage.failureMode}
              </p>
            </div>
          </motion.div>
        </AnimatePresence>
      </div>
    </Section>
  );
}
