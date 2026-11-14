import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./app/**/*.{ts,tsx}",
    "./components/**/*.{ts,tsx}",
    "./lib/**/*.{ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // Core surfaces
        ink: "#06080A", // page background, near-black
        void: "#040506", // deepest wells
        panel: "#0C1014", // raised panels
        panel2: "#11161B", // hover / nested panels
        line: "#1C242B", // hairline borders
        // Text
        chalk: "#EAF0F3", // primary text
        fog: "#8B97A2", // secondary text
        ash: "#5A646D", // tertiary / captions
        // Accent (single strong accent)
        signal: "#BFFF3C", // acid-lime, the signal color
        "signal-dim": "#6F8F2A",
        // Semantic data colors
        alert: "#FF5A47", // failure / danger data
        flux: "#4BD6C4", // sparing cool accent for perception data
      },
      fontFamily: {
        sans: ["var(--font-sans)", "system-ui", "sans-serif"],
        mono: ["var(--font-mono)", "ui-monospace", "monospace"],
      },
      letterSpacing: {
        label: "0.22em",
      },
      maxWidth: {
        shell: "1200px",
      },
      keyframes: {
        "scan-y": {
          "0%": { transform: "translateY(-100%)" },
          "100%": { transform: "translateY(100%)" },
        },
        "pulse-soft": {
          "0%, 100%": { opacity: "0.35" },
          "50%": { opacity: "1" },
        },
        "dash-flow": {
          to: { strokeDashoffset: "-1000" },
        },
      },
      animation: {
        "scan-y": "scan-y 6s linear infinite",
        "pulse-soft": "pulse-soft 3s ease-in-out infinite",
        "dash-flow": "dash-flow 30s linear infinite",
      },
    },
  },
  plugins: [],
};

export default config;
