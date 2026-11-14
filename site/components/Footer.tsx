"use client";

import { Reveal } from "./primitives";
import { REPO_URL } from "@/lib/data";

export default function Footer() {
  return (
    <footer id="repo" className="relative overflow-hidden">
      <div className="pointer-events-none absolute inset-0 grid-floor opacity-60" />

      <div className="shell relative py-24 sm:py-32">
        <Reveal>
          <div className="label text-signal-dim">The source</div>
        </Reveal>

        <Reveal delay={0.05}>
          <h2 className="mt-5 max-w-3xl text-[clamp(2rem,5vw,3.4rem)] font-semibold leading-[1.02] tracking-tight">
            Read the harness, run the seeds, check the numbers.
          </h2>
        </Reveal>

        <Reveal delay={0.1}>
          <p className="mt-5 max-w-xl leading-relaxed text-fog">
            Everything on this page is reproducible. The simulator, the agent
            loop, the baselines, and the cached runs are all in the repository.
          </p>
        </Reveal>

        <Reveal delay={0.15}>
          <a
            href={REPO_URL}
            target="_blank"
            rel="noopener noreferrer"
            className="group mt-10 inline-flex items-center gap-3 rounded-full bg-signal px-7 py-4 font-mono text-sm font-semibold text-ink transition-transform duration-200 hover:scale-[1.02] focus-visible:scale-[1.02]"
          >
            <svg
              width="18"
              height="18"
              viewBox="0 0 24 24"
              fill="currentColor"
              aria-hidden="true"
            >
              <path d="M12 .5a12 12 0 0 0-3.8 23.4c.6.1.8-.3.8-.6v-2c-3.3.7-4-1.6-4-1.6-.6-1.4-1.3-1.8-1.3-1.8-1.1-.7 0-.7 0-.7 1.2 0 1.9 1.2 1.9 1.2 1 1.8 2.8 1.3 3.5 1 .1-.8.4-1.3.8-1.6-2.7-.3-5.5-1.3-5.5-5.9 0-1.3.5-2.4 1.2-3.2 0-.3-.5-1.5.2-3.2 0 0 1-.3 3.3 1.2a11.5 11.5 0 0 1 6 0C17 5 18 5.3 18 5.3c.7 1.7.2 2.9.1 3.2.8.8 1.2 1.9 1.2 3.2 0 4.6-2.8 5.6-5.5 5.9.4.4.8 1.1.8 2.2v3.3c0 .3.2.7.8.6A12 12 0 0 0 12 .5Z" />
            </svg>
            View SightLoop on GitHub
            <span className="transition-transform duration-200 group-hover:translate-x-0.5">
              ↗
            </span>
          </a>
        </Reveal>

        {/* bottom bar */}
        <div className="mt-20 flex flex-col items-start justify-between gap-6 border-t border-line pt-8 sm:flex-row sm:items-center">
          <div className="flex items-center gap-2.5">
            <span className="h-2.5 w-2.5 rounded-full bg-signal" />
            <span className="font-mono text-sm font-semibold">
              Sight<span className="text-signal">Loop</span>
            </span>
            <span className="ml-3 font-mono text-xs text-ash">
              A failure-aware evaluation harness
            </span>
          </div>
          <div className="font-mono text-xs text-ash">Built by Deep</div>
        </div>
      </div>
    </footer>
  );
}
