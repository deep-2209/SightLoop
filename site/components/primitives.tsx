"use client";

import { motion, useReducedMotion, type Variants } from "framer-motion";
import type { ReactNode } from "react";

const EASE = [0.16, 1, 0.3, 1] as const;

export function Reveal({
  children,
  delay = 0,
  y = 18,
  className,
}: {
  children: ReactNode;
  delay?: number;
  y?: number;
  className?: string;
}) {
  const reduce = useReducedMotion();
  return (
    <motion.div
      className={className}
      initial={reduce ? false : { opacity: 0, y }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, margin: "-12%" }}
      transition={{ duration: 0.6, delay, ease: EASE }}
    >
      {children}
    </motion.div>
  );
}

export const staggerParent: Variants = {
  hidden: {},
  show: { transition: { staggerChildren: 0.08 } },
};

export const staggerChild: Variants = {
  hidden: { opacity: 0, y: 16 },
  show: { opacity: 1, y: 0, transition: { duration: 0.55, ease: EASE } },
};

export function SectionHeader({
  index,
  kicker,
  title,
  intro,
}: {
  index: string;
  kicker: string;
  title: ReactNode;
  intro?: ReactNode;
}) {
  return (
    <div className="max-w-3xl">
      <Reveal>
        <div className="label flex items-center gap-3">
          <span className="text-signal">{index}</span>
          <span className="h-px w-8 bg-line" />
          <span>{kicker}</span>
        </div>
      </Reveal>
      <Reveal delay={0.05}>
        <h2 className="mt-5 text-[clamp(1.9rem,4.5vw,3rem)] font-semibold leading-[1.05] tracking-tight">
          {title}
        </h2>
      </Reveal>
      {intro && (
        <Reveal delay={0.1}>
          <p className="mt-5 text-lg leading-relaxed text-fog">{intro}</p>
        </Reveal>
      )}
    </div>
  );
}

export function Section({
  id,
  children,
  className = "",
}: {
  id?: string;
  children: ReactNode;
  className?: string;
}) {
  return (
    <section
      id={id}
      className={`relative border-b border-line py-24 sm:py-32 ${className}`}
    >
      <div className="shell">{children}</div>
    </section>
  );
}
