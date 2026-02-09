# LEGO Shop - Enhanced Version

## Overview
Enhanced version of the LEGO shop with modern design, animations, and mobile optimizations.

## What's New (v2.0)

### Visual Enhancements
- ✨ **Modern Gradient Background** - Subtle animated gradients
- 💫 **Glowing Accents** - Pink glow effects on interactive elements
- 🎨 **Smooth Animations** - Fade-in cards, hover transitions
- 📱 **Better Typography** - Inter font family
- 🎯 **Improved Shadows** - Multi-layer depth effects

### UX Improvements
- ⚡ **Faster Filtering** - Debounced search (150ms)
- 🔔 **Toast Notifications** - User feedback on actions
- ⌨️ **Keyboard Navigation** - Tab through cards, Enter to open
- ♿ **Better Accessibility** - ARIA labels, semantic HTML
- 🖼️ **Lazy Loading Images** - Performance optimized

### Mobile Optimizations
- 📱 **Responsive Breakpoints** - 1024px, 768px, 480px
- 🔄 **Touch-friendly** - Larger touch targets
- 📐 **Fluid Grid** - Adapts to any screen size

## Files

### Enhanced Files
- `styles-enhanced.css` - New modern styling
- `script-enhanced.js` - Better JavaScript with toast notifications

### Original Files (Preserved)
- `styles.css` - Original styles
- `script.js` - Original JavaScript

## How to Use

### Use Enhanced Version
```html
<!-- In index.html -->
<link rel="stylesheet" href="styles-enhanced.css" />
<script src="script-enhanced.js" defer></script>
```

### Switch Back to Original
```html
<!-- In index.html -->
<link rel="stylesheet" href="styles.css" />
<script src="script.js" defer></script>
```

## Features

### New CSS Features
- CSS Variables for theming
- Smooth transitions (fast/normal/slow)
- Loading skeleton animation
- Toast notification styles
- Responsive breakpoints:
  - Desktop: 4 columns
  - Tablet: 3 columns
  - Small tablet: 2 columns
  - Mobile: 1 column

### New JavaScript Features
- Toast notification system
- Performance timing
- Better error handling
- Keyboard accessibility
- Smooth click animations

## Color Scheme

### CSS Variables
```css
--bg: #0f0f14           /* Background */
--card: #171824         /* Card background */
--accent: #ff4d8d       /* Pink accent */
--accent2: #ff2d55      /* Darker pink */
--success: #00ffa3      /* Green */
--warning: #ffd400      /* Yellow */
--danger: #ff005a       /* Red */
```

## Browser Support

- Chrome 80+
- Firefox 75+
- Safari 13+
- Edge 80+

## Performance

- Lazy image loading
- Debounced filtering (150ms)
- CSS animations (GPU accelerated)
- Minimal reflows

## Credits

Created: 2026-02-08
Skills: Frontend Design Ultimate
