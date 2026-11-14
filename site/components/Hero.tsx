"use client";

import { motion, useReducedMotion, useScroll, useTransform } from "framer-motion";
import { useRef } from "react";
import LoopRing from "./LoopRing";
import { researchQuestion } from "@/lib/data";

const thesisWords =
  "A vision-grounded LLM agent whose deliverable is not the demo. It is the measurement.".split(
    " "
  );

export default function Hero() {
  const reduce = useReducedMotion();
  const ref = useRef<HTMLElement>(null);
  const { scrollYProgress } = useScroll({
    target: ref,
    offset: ["start start", "end start"],
  });
  const yText = useTransform(scrollYProgress, [0, 1], [0, reduce ? 0 : -60]);
  const yRing = useTransform(scrollYProgress, [0, 1], [0, reduce ? 0 : 80]);
  const fade = useTransform(scrollYProgress, [0, 0.8], [1, reduce ? 1 : 0]);

  return (
    <section
      ref={ref}
      className="relative overflow-hidden border-b border-line"
      aria-label="Introduction"
    >
      {/* Background grid + scan line */}
      <div className="pointer-events-none absolute inset-0 grid-floor" />
      {!reduce && (
        <div className="pointer-events-none absolute inset-0 overflow-hidden">
          <div className="absolute left-0 right-0 h-px bg-gradient-to-r from-transparent via-signal/40 to-transparent animate-scan-y" />
        </div>
      )}

      <div className="shell relative grid min-h-[92vh] grid-cols-1 items-center gap-12 py-24 lg:grid-cols-[1.25fr_1fr] lg:py-28">
        {/* Text column */}
        <motion.div style={{ y: yText, opacity: fade }}>
          <motion.div
            initial={reduce ? false : { opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            className="flex items-center gap-3"
          >
            <span className="h-2 w-2 rounded-full bg-signal shadow-[0_0_14px_2px_rgba(191,255,60,0.6)]" />
            <span className="label">
              Vision-grounded manipulation // failure-aware harness
            </span>
          </motion.div>

          <motion.h1
            initial={reduce ? false : { opacity: 0, y: 16 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.7, delay: 0.05 }}
            className="mt-7 font-sans text-[clamp(3.4rem,11vw,7.5rem)] font-semibold leading-[0.92] tracking-tight"
          >
            Sight
            <span className="relative text-signal">
              Loop
              <span className="absolute -right-1 bottom-2 hidden h-[0.12em] w-[0.12em] rounded-full bg-signal sm:block" />
            </span>
          </motion.h1>

          {/* Animated one-line thesis, word by word */}
          <p className="mt-7 max-w-xl text-lg leading-relaxed text-fog sm:text-xl">
            {thesisWords.map((w, i) => {
              const strong =
                w.startsWith("measurement") || w === "measurement.";
              return (
                <motion.span
                  key={i}
                  initial={reduce ? false : { opacity: 0, y: 8 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.4, delay: 0.5 + i * 0.05 }}
                  className={strong ? "text-chalk" : undefined}
                >
                  {w}{" "}
                </motion.span>
              );
            })}
          </p>

          {/* Research question callout */}
          <motion.div
            initial={reduce ? false : { opacity: 0, y: 16 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 1.1 }}
            className="mt-10 max-w-xl rounded-lg border border-line bg-panel/60 p-5 backdrop-blur-sm"
          >
            <div className="label mb-2 text-signal-dim">Research question</div>
            <p className="font-mono text-[0.92rem] leading-relaxed text-chalk">
              {researchQuestion}
            </p>
          </motion.div>
        </motion.div>

        {/* Ring column */}
        <motion.div
          style={{ y: yRing, opacity: fade }}
          initial={reduce ? false : { opacity: 0, scale: 0.92 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.9, delay: 0.3 }}
          className="order-first lg:order-none"
        >
          <LoopRing />
        </motion.div>
      </div>

      {/* Scroll hint */}
      <motion.div
        style={{ opacity: fade }}
        className="pointer-events-none absolute bottom-6 left-1/2 flex -translate-x-1/2 flex-col items-center gap-2"
      >
        <span className="label text-ash">Scroll</span>
        <motion.span
          animate={reduce ? undefined : { y: [0, 7, 0] }}
          transition={{ duration: 1.8, repeat: Infinity, ease: "easeInOut" }}
          className="block h-6 w-px bg-gradient-to-b from-signal to-transparent"
        />
      </motion.div>
    </section>
  );
}
