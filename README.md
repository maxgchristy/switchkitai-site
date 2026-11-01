# switchkitai.com — Switch Kit AI

Static site hosted free on GitHub Pages (from the `docs/` folder on `main`).

- Edit the source at the repo root: `index.html` (page template), `library.js` (shortcuts), `pages/*.html` (help, privacy, terms).
- Build: `python3 build.py switchkitai@gmail.com 50f0715e-72d0-4480-b107-886be6ceffc4` (the second value turns on Umami visit counts; never leave it out). Output goes to `docs/`.
- Commit and push `main`; GitHub Pages republishes in a minute or two. No credits, no limits on edits.
- Images: `python3 tools/render_assets.py /path/to/fonts` (see the script for how to get the fonts).
- The paid page is `docs/kit-x7q2m9.html`; Stripe's live $9.99 link redirects buyers there, so don't rename it.
