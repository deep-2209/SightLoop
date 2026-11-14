# SightLoop — project website

The official project page for SightLoop, a vision-grounded LLM agent for
tabletop robot manipulation built as a failure-aware evaluation harness.

Stack: Next.js (App Router) + TypeScript + Tailwind CSS + Framer Motion.

## Local development

```bash
cd site
npm install
npm run dev        # http://localhost:3000
```

## Production build

```bash
npm run build
npm run start
```

## Deploy on Vercel

1. Import this GitHub repo into Vercel.
2. Set **Root Directory** to `site`.
3. Leave everything else as default. Framework preset is detected as Next.js.

That Root Directory setting is the only configuration needed; the build is
otherwise zero-config.

## Content

Every number and claim shown on the page lives in one file, `lib/data.ts`, so
the site cannot drift from the real results. The two demo clips are served from
`public/success.gif` and `public/failure.gif`.

## Accessibility

- Keyboard focus is visible throughout, and the agent-loop diagram is operable
  with the arrow keys.
- `prefers-reduced-motion` is respected in JavaScript (every animation is gated)
  and as a CSS safety net.
