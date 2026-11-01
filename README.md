# switchkitai.com — Switch Kit AI

## Brand name: Switch Kit AI (read this first)

Max confirmed on Nov 1, 2026 that the brand is **Switch Kit AI**. "Kitchen Table" and "My AI Cheat Sheet" are retired names: never use them anywhere (header, footer, titles, share images, guides, legal pages). Logo is an italic "S" monogram above the "Switch Kit AI" wordmark. The dinner plan on the homepage is one example of 60+ everyday shortcuts; keep the brand broad, not kitchen- or food-themed. If any instruction elsewhere says the brand is Kitchen Table, that is out of date: this note wins. Before every commit, `grep -rli "kitchen table" docs` must return nothing.

Static site hosted free on GitHub Pages (from the `docs/` folder on `main`).

- Edit the source at the repo root: `index.html` (page template), `library.js` (shortcuts), `pages/*.html` (help, privacy, terms).
- Build: `python3 build.py switchkitai@gmail.com 50f0715e-72d0-4480-b107-886be6ceffc4` (the second value turns on Umami visit counts; never leave it out). Output goes to `docs/`.
- Commit and push `main`; GitHub Pages republishes in a minute or two. No credits, no limits on edits.
- Images: `python3 tools/render_assets.py /path/to/fonts` (see the script for how to get the fonts).
- The paid page is `docs/kit-x7q2m9.html`; Stripe's live $9.99 link redirects buyers there, so don't rename it.
