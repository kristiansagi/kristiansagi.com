---
title: "Building a Secure Contact Form: My Kind of Weekend Project"
type: post
date: 2025-11-10
author: Kristian Sägi
description: "How I spent a weekend building an encrypted contact form with Hugo, Cloudflare Workers and OpenPGP.js."
tags: ["Hugo", "Cloudflare", "OpenPGP", "Resend", "Security", "Weekend Project", "Personal Site"]
cover:
  image: "cover.webp"
  alt: "Encrypted contact form running on kristiansagi.com"
  caption: "A weekend of building a secure contact form with Hugo, OpenPGP.js and Cloudflare Workers."
  relative: true
ShowToc: true
ShowReadingTime: true
TocOpen: false
draft: false
hidden: false
canonicalURL: ""
---

I love a good weekend project.
No meetings, no deadlines, just me and a problem to solve.

This time, it was about giving my homepage, kristiansagi.com, a private contact form I could actually trust.

---

## Why build it myself?

When I first created the site, I used [Mobirise](https://mobirise.com/), a nice and simple UI toolkit that gets things running fast. But over time, I noticed small quirks I couldn’t fully control.
Then, a few weeks ago, I stumbled upon a developer’s blog built with Hugo.
It was fast, minimal, and refreshingly transparent in how it worked.
One thing led to another. I rebuilt my site on Hugo and started tweaking everything myself.

And then came the classic question: how should people contact me?

---

## The trust problem

I’ve never fully trusted most “contact me” forms. Too often messages vanish into some backend, or worse, never reach the intended person at all.
I wanted messages to reach only me, with nobody able to read them on the way.

So I decided to build it from scratch.

## How it works

Messages are encrypted locally in the browser using [OpenPGP.js](https://openpgpjs.org/), before they ever leave the sender’s device.

+ The encrypted payload is then passed through [Cloudflare Workers](https://workers.cloudflare.com/), which act as a secure listener.
+ Once received, the Worker uses [Resend](https://resend.com/) to forward the message to my inbox.
+ Finally, the email is automatically decrypted using my private PGP key.

Nothing is stored on a server along the way, and nothing travels unencrypted.

## Keeping bots out

Of course, no system is safe from bad actors.
Initially, I wanted to integrate [Proton’s captcha](https://proton.me/blog/proton-captcha), but they haven’t released a public API yet.
So I went with [Cloudflare Turnstile](https://www.cloudflare.com/application-services/products/turnstile/) in invisible mode.
No “find all the traffic lights” riddles, just a quiet, invisible check.
It took some trial and error to implement, but I’m happy with the result. Visitors don’t have to do anything.

## What I learned

After years in leadership roles, writing code again felt almost meditative.
It reminded me why I got into tech in the first place: those small, satisfying moments when something finally works.

If you want to try it, the form is on my [contact page](/contact/).
