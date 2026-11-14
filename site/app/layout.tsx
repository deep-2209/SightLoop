import type { Metadata } from "next";
import { Inter, JetBrains_Mono } from "next/font/google";
import "./globals.css";

const sans = Inter({
  subsets: ["latin"],
  variable: "--font-sans",
  display: "swap",
});

const mono = JetBrains_Mono({
  subsets: ["latin"],
  variable: "--font-mono",
  display: "swap",
});

export const metadata: Metadata = {
  title: "SightLoop // A failure-aware evaluation harness for LLM robot manipulation",
  description:
    "SightLoop is a vision-grounded LLM agent for tabletop robot manipulation, built to measure where manipulation fails: perception, planning, or control, and whether fault-aware recovery helps.",
  metadataBase: new URL("https://sightloop.vercel.app"),
  openGraph: {
    title: "SightLoop",
    description:
      "Where do failures come from in LLM-driven robot manipulation, and does fault-aware recovery help?",
    type: "website",
  },
  robots: { index: true, follow: true },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className={`${sans.variable} ${mono.variable}`}>
      <body>
        <a
          href="#main"
          className="sr-only focus:not-sr-only focus:fixed focus:left-4 focus:top-4 focus:z-50 focus:rounded focus:bg-signal focus:px-4 focus:py-2 focus:font-mono focus:text-sm focus:text-ink"
        >
          Skip to content
        </a>
        {children}
      </body>
    </html>
  );
}
