---
title: "Building a Secure Contact Form — My Kind of Weekend Project"
type: post
date: 2025-11-10
author: Kristian Sägi
description: "A hands-on weekend building a fast, private, and encrypted contact form with Hugo, Cloudflare Workers, and OpenPGP.js."
tags: ["Hugo", "Cloudflare", "OpenPGP", "Resend", "Security", "Weekend Project", "Personal Site"]
cover:
  image: "cover.webp"
  alt: "Encrypted contact form running on kristiansagi.com"
  caption: "Weekend hacking — building a secure contact form with Hugo, OpenPGP.js, and Cloudflare Workers."
  relative: true
ShowToc: true
ShowReadingTime: true
TocOpen: false
draft: false
relative: true
---

There’s something deeply satisfying about a good weekend project.
No meetings, no deadlines — just focus, curiosity, and the quiet rhythm of making something work with your own hands.

This time, it was about giving my homepage, kristiansagi.com, a secure and private contact form — one I could actually trust.

---

## Why build it myself?

When I first created the site, I used [Mobirise](https://mobirise.com/) — a nice and simple UI toolkit that gets things running fast. But over time, I noticed small quirks I couldn’t fully control.
Then, a few weeks ago, I stumbled upon a developer’s blog built with Hugo.
It was fast, minimal, and refreshingly transparent in how it worked.
That discovery set off a chain reaction — I rebuilt my site on Hugo and started tweaking everything myself.

And then came the classic question: how should people contact me?

---

## The trust problem

I’ve never fully trusted most “contact me” forms. Too often messages vanish into some backend, or worse, never reach the intended person at all.
I wanted something that would guarantee privacy — where messages are delivered only to me and never readable by anyone else in transit.

So I decided to build it from scratch.

## How it works

Messages are encrypted locally in the browser using [OpenPGP.js](https://openpgpjs.org/), before they ever leave the sender’s device.

+ The encrypted payload is then passed through [Cloudflare Workers](https://workers.cloudflare.com/), which act as a secure listener.
+ Once received, the Worker uses [Resend](https://resend.com/) to forward the message to my inbox.
+ Finally, the email is automatically decrypted using my private PGP key.

No external backend, no unencrypted traffic, no middlemen.

## Keeping bots out

Of course, no system is safe from bad actors.
Initially, I wanted to integrate [Proton’s captcha](https://proton.me/blog/proton-captcha), but they haven’t released a public API yet.
So I went with [Cloudflare Turnstile](https://www.cloudflare.com/application-services/products/turnstile/) — hidden mode only.
No “find all the traffic lights” riddles, just a quiet, invisible check.
It took some trial and error to implement, but now I genuinely like the result — no friction, no noise, no distractions.

## What I learned

There’s something meditative about returning to raw development after years of leadership roles.
Building systems reminds me why I started in tech in the first place: the combination of logic, creativity, and small problem-solving moments that lead to something real.

> The end result?
> A fast, elegant, and private way to reach me —
>👉 https://kristiansagi.com/contact
