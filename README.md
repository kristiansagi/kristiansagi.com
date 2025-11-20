# kristiansagi.com

Personal site of **Kristian Sägi** — engineering & technology leader.  
The site combines a lightweight Hugo setup, custom typography, and a privacy-first contact flow.

Live: https://kristiansagi.com

---

## Overview

This repository contains the source for my personal website, built as a static site with **Hugo** and deployed via **Cloudflare Pages**.

The site is focused on:

- Clear presentation of my **story, experience, and track record**  
- Long-form **perspectives / reflections** on leadership and technology  
- A **secure contact form** that respects privacy and uses end-to-end encryption  
- Fast, minimal, and distraction-free reading experience

---

## Key Features

- **Static site with Hugo**
  - Uses Hugo (extended) and a customized variant of the **PaperMod** theme
  - Simple content-first structure: `content/`, `layouts/`, `assets/`, `static/`

- **Custom typography**
  - Self-hosted **Lexend** (primary) and **Inter** (supporting) fonts
  - Tuned line heights and font sizes for long-form reading
  - Consistent typography between the website and exported PDFs (e.g. résumé)

- **Perspectives / Blog**
  - Long-form essays and reflections under `/blog` (aka “Perspectives” / “Reflections”)
  - SEO-friendly URLs, e.g.:
    - `/blog/to-build-fast-you-need-to-be-slow/`

- **Executive résumé**
  - Dedicated résumé page
  - Buttons for **Print** and **Download PDF**, styled consistently with the front page

- **Secure contact form**
  - Client-side encryption using **OpenPGP.js**
  - Submissions sent through **Cloudflare Workers** to **Resend**
  - Messages are stored only in encrypted form and decrypted locally with a private key
  - Protected by **Cloudflare Turnstile** (CAPTCHA-like challenge)

- **Privacy & security**
  - No analytics, no tracking pixels
  - Strict security headers configured via Cloudflare
  - Fonts, JS, and CSS are self-hosted where possible

---

## Tech Stack

- **Static site generator:** [Hugo](https://gohugo.io/) (extended)
- **Theme base:** [PaperMod](https://github.com/adityatelange/hugo-PaperMod) (heavily customized)
- **Deployment:** [Cloudflare Pages](https://pages.cloudflare.com/)
- **Edge logic & secure form:** [Cloudflare Workers](https://developers.cloudflare.com/workers/)
- **Email delivery for contact form:** [Resend](https://resend.com/)
- **Client-side crypto:** [OpenPGP.js](https://github.com/openpgpjs/openpgpjs)
- **Bot protection:** [Cloudflare Turnstile](https://www.cloudflare.com/products/turnstile/)
