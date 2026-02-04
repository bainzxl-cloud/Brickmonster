LEGO Shop Page (static)

Files:
- index.html
- styles.css
- script.js
- listings.json

How to use:
1) Edit listings.json:
   - set config.instagramHandle to your IG handle (no @)
   - add/modify items
2) Run a tiny local server in this folder (recommended) so fetch() works:
   - If you have Python:   python -m http.server 5173
   - Or Node:             npx serve .
3) Open: http://localhost:5173

Images:
- Put a URL in each item.image.
- If empty, it uses a placeholder.

Status values: available | pending | sold
