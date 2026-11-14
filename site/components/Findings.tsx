"use client";

import { motion, useReducedMotion } from "framer-motion";
import { Section, SectionHeader } from "./primitives";
import { findings } from "@/lib/data";

const EASE = [0.16, 1, 0.3, 1] as const;

export default function Findings() {
  const reduce = useReducedMotion();

  return (
    <Section id="findings">
      <SectionHeader
        index="06"
        kicker="Three findings"
        title="What the gaps actually tell us."
      />

      <div className="mt-16 space-y-5">
        {findings.map((f, i) => (
          <motion.article
            key={f.n}
            initial={reduce ? false : { opacity: 0, y: 28 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true, margin: "-15%" }}
            transition={{ duration: 0.7, ease: EASE }}
            className="group grid gap-8 rounded-2xl border border-line bg-panel p-8 transition-colors hover:border-signal/30 sm:p-10 md:grid-cols-[auto_1fr]"
          >
            <div className="flex items-start gap-5 md:flex-col md:gap-4">
              <span className="font-mono text-6xl font-semibold leading-none text-line transition-colors group-hover:text-signal/40 sm:text-7xl">
                {f.n}
              </span>
            </div>

            <div>
              <h3 className="text-2xl font-semibold leading-snug tracking-tight sm:text-3xl">
                {f.title}
              </h3>
              <p className="mt-5 max-w-2xl leading-relaxed text-fog">{f.body}</p>
              <div className="mt-6 inline-flex items-center gap-3 border-l-2 border-signal pl-4">
                <span className="font-mono text-sm text-signal">{f.pull}</span>
              </div>
            </div>
          </motion.article>
        ))}
      </div>
    </Section>
  );
}
