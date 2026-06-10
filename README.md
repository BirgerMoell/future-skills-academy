# Future Skills Academy

Static course platform for Future Skills Academy — the skills that compound in an AI-native world.

## The five tracks

1. **Member of Technical Staff** — technical craft: AI-native engineering, context engineering, agents, evals, eternal fundamentals.
2. **High Agency** — leadership: ownership, decisions under uncertainty, leverage, leading AI-augmented teams.
3. **Taste** — design and UX: training the eye, eternal rules of craft, directing AI tools, editing.
4. **Relationships** — sales and customers: trust, listening, founder-led sales, long games.
5. **Communication** — clarity: thinking in writing, memos, speaking, audience, feedback, and being worth reading in the flood.

Each track is six modules and eighteen lessons with practice assignments and a capstone. Lesson progress is saved in the visitor's browser via `localStorage` (no backend).

## Structure

- `index.html` — landing page (thesis, tracks, method, principles)
- `tracks/*.html` — one page per track with the full curriculum
- `styles.css` / `script.js` — shared design system and platform behavior

Plain HTML/CSS/JS, served from the repository root (GitHub Pages, `.nojekyll`). To preview locally: `python3 -m http.server` and open `http://localhost:8000`.
