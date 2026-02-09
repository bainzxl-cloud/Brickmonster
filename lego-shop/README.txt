LEGO Shop (static)

What this is
- A fast static listing page (no checkout)
- Edit listings.json and deploy anywhere

Files
- index.html
- styles.css
- script.js
- listings.json

Local preview (so fetch() works)
- Python:   python -m http.server 5173
- Node:     npx serve .
Open: http://localhost:5173

Deep links
- The modal writes a shareable URL like:
  /?p=10283
Filters also persist in the URL:
  /?category=Star%20Wars&sort=price_asc

Inventory fields (recommended)
- id (string) unique
- name (string)
- setNumber (string)
- category (string)
- condition (string) e.g. Sealed | Open box | Built (complete)
- availability (string): in_stock | reserved | out_of_stock
- price (number) optional
- addedAt (YYYY-MM-DD or ISO string) used for "Newest"
- images (array of URLs) for gallery
- tags (array of strings)
- description (string)

Hosting
- Cloudflare Pages / Netlify / GitHub Pages: just deploy this folder.
