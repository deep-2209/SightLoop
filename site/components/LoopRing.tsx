"use client";

import { motion, useReducedMotion } from "framer-motion";
import { loopStages } from "@/lib/data";

const SIZE = 320;
const C = SIZE / 2;
const R = 118;

function nodePos(i: number, total: number) {
  // Start at top (-90deg), go clockwise
  const angle = (-90 + (360 / total) * i) * (Math.PI / 180);
  return { x: C + R * Math.cos(angle), y: C + R * Math.sin(angle) };
}

export default function LoopRing() {
  const reduce = useReducedMotion();

  return (
    <div
      className="relative mx-auto aspect-square w-full max-w-[360px]"
      aria-hidden="true"
    >
      <svg
        viewBox={`0 0 ${SIZE} ${SIZE}`}
        className="h-full w-full overflow-visible"
      >
        {/* Outer faint ring */}
        <circle cx={C} cy={C} r={R + 26} fill="none" stroke="#1C242B" strokeWidth={1} />

        {/* Flow ring */}
        <circle
          cx={C}
          cy={C}
          r={R}
          fill="none"
          stroke="#1C242B"
          strokeWidth={1.5}
        />
        <circle
          cx={C}
          cy={C}
          r={R}
          fill="none"
          stroke="#BFFF3C"
          strokeWidth={1.5}
          strokeDasharray="4 10"
          strokeLinecap="round"
          opacity={0.55}
          className={reduce ? "" : "animate-dash-flow"}
        />

        {/* Traveling signal dot */}
        {!reduce && (
          <motion.g
            style={{ originX: `${C}px`, originY: `${C}px` }}
            animate={{ rotate: 360 }}
            transition={{ duration: 9, ease: "linear", repeat: Infinity }}
          >
            <circle cx={C} cy={C - R} r={5.5} fill="#BFFF3C" />
            <circle cx={C} cy={C - R} r={11} fill="#BFFF3C" opacity={0.18} />
          </motion.g>
        )}

        {/* Stage nodes */}
        {loopStages.map((s, i) => {
          const { x, y } = nodePos(i, loopStages.length);
          return (
            <g key={s.id}>
              <circle cx={x} cy={y} r={15} fill="#06080A" stroke="#1C242B" strokeWidth={1} />
              <motion.circle
                cx={x}
                cy={y}
                r={4.5}
                fill="#BFFF3C"
                initial={{ opacity: 0.35 }}
                animate={reduce ? { opacity: 0.8 } : { opacity: [0.3, 1, 0.3] }}
                transition={
                  reduce
                    ? undefined
                    : { duration: 9, times: [0, 0.1, 0.25], delay: (9 / loopStages.length) * i, repeat: Infinity }
                }
              />
              <text
                x={x}
                y={y + 30}
                textAnchor="middle"
                className="fill-fog font-mono"
                style={{ fontSize: 10, letterSpacing: "0.12em" }}
              >
                {s.name.toUpperCase()}
              </text>
            </g>
          );
        })}

        {/* Center label */}
        <text
          x={C}
          y={C - 6}
          textAnchor="middle"
          className="fill-chalk font-mono"
          style={{ fontSize: 13, letterSpacing: "0.18em" }}
        >
          THE
        </text>
        <text
          x={C}
          y={C + 14}
          textAnchor="middle"
          className="fill-signal font-mono"
          style={{ fontSize: 15, letterSpacing: "0.1em", fontWeight: 600 }}
        >
          LOOP
        </text>
      </svg>
    </div>
  );
}
