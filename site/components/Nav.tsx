"use client";

import { useEffect, useState } from "react";
import { REPO_URL } from "@/lib/data";

const links = [
  { href: "#loop", label: "The loop" },
  { href: "#demo", label: "Demo" },
  { href: "#results", label: "Results" },
  { href: "#findings", label: "Findings" },
  { href: "#method", label: "Method" },
];

export default function Nav() {
  const [scrolled, setScrolled] = useState(false);

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 24);
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  return (
    <header
      className={`fixed inset-x-0 top-0 z-40 transition-colors duration-300 ${
        scrolled
          ? "border-b border-line bg-ink/80 backdrop-blur-md"
          : "border-b border-transparent"
      }`}
    >
      <nav className="shell flex h-14 items-center justify-between">
        <a href="#main" className="group flex items-center gap-2">
          <span className="relative flex h-2.5 w-2.5">
            <span className="absolute inline-flex h-full w-full rounded-full bg-signal opacity-60 group-hover:animate-ping" />
            <span className="relative inline-flex h-2.5 w-2.5 rounded-full bg-signal" />
          </span>
          <span className="font-mono text-sm font-semibold tracking-tight">
            Sight<span className="text-signal">Loop</span>
          </span>
        </a>

        <div className="hidden items-center gap-7 md:flex">
          {links.map((l) => (
            <a
              key={l.href}
              href={l.href}
              className="font-mono text-xs text-fog transition-colors hover:text-chalk"
            >
              {l.label}
            </a>
          ))}
        </div>

        <a
          href={REPO_URL}
          target="_blank"
          rel="noopener noreferrer"
          className="rounded-full border border-line px-4 py-1.5 font-mono text-xs text-chalk transition-colors hover:border-signal hover:text-signal"
        >
          GitHub ↗
        </a>
      </nav>
    </header>
  );
}
