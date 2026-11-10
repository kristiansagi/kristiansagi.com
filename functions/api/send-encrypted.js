// send-encrypted.js — receives a client-side PGP-encrypted message, verifies Cloudflare
// Turnstile, and forwards the ciphertext by email via Resend.
//
// Works both as a Cloudflare Pages Function (onRequestPost / onRequestOptions) and as a
// standalone Worker (default export), which local development posts to.
//
// Env: TURNSTILE_SECRET_KEY, RESEND_API_KEY (secrets); MAIL_FROM, MAIL_TO,
//      ALLOWED_ORIGINS (comma-separated, optional), ALLOWED_HOSTNAMES (comma-separated, optional)

const DEFAULT_ORIGINS = [
  "https://kristiansagi.com",
  "https://www.kristiansagi.com",
  "https://staging.kristiansagi.com",
  "http://localhost:1313",
];
const DEFAULT_SUBJECT = "Encrypted message via contact page";
const MAX_SUBJECT_LEN = 120;
const MAX_CIPHERTEXT_LEN = 64 * 1024; // armored text; a long message is a few KB

const ARMOR_RE =
  /^-----BEGIN PGP MESSAGE-----\n(?:[A-Za-z0-9-]+: [^\n]*\n)*\n[A-Za-z0-9+/=\n]+\n(?:=[A-Za-z0-9+/]{4}\n)?-----END PGP MESSAGE-----\n?$/;

// -- helpers ---------------------------------------------------------------

function list(value, fallback) {
  const items = (value || "").split(",").map((s) => s.trim()).filter(Boolean);
  return items.length ? items : fallback;
}

function allowedOrigins(env) {
  return list(env.ALLOWED_ORIGINS, DEFAULT_ORIGINS);
}

function allowedHostnames(env) {
  return list(
    env.ALLOWED_HOSTNAMES,
    allowedOrigins(env).map((o) => new URL(o).hostname),
  );
}

function corsHeaders(request, env) {
  const origin = request.headers.get("Origin");
  const headers = {
    "Access-Control-Allow-Methods": "POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type",
    "Access-Control-Max-Age": "86400",
    Vary: "Origin",
  };
  if (origin && allowedOrigins(env).includes(origin)) {
    headers["Access-Control-Allow-Origin"] = origin;
  }
  return headers;
}

function json(request, env, obj, status = 200) {
  return new Response(JSON.stringify(obj), {
    status,
    headers: {
      "content-type": "application/json; charset=utf-8",
      "cache-control": "no-store",
      ...corsHeaders(request, env),
    },
  });
}

/** Returns a normalized armored PGP message, or null if the input is not one. */
function parseArmor(input) {
  const t = input.replace(/^﻿/, "").replace(/\r\n?/g, "\n").trim() + "\n";
  return ARMOR_RE.test(t) ? t : null;
}

function cleanSubject(input) {
  if (typeof input !== "string") return DEFAULT_SUBJECT;
  // Strip control characters (incl. CR/LF) and collapse whitespace
  const s = input.replace(/[\u0000-\u001F\u007F]+/g, " ").replace(/\s+/g, " ").trim();
  return (s || DEFAULT_SUBJECT).slice(0, MAX_SUBJECT_LEN);
}

// -- main handler ----------------------------------------------------------

async function handleSendEncrypted(request, env) {
  const origin = request.headers.get("Origin");
  if (origin && !allowedOrigins(env).includes(origin)) {
    return json(request, env, { error: "forbidden_origin" }, 403);
  }
  if (!(request.headers.get("content-type") || "").includes("application/json")) {
    return json(request, env, { error: "unsupported_media_type" }, 415);
  }

  const raw = await request.text();
  if (raw.length > MAX_CIPHERTEXT_LEN + 4096) {
    return json(request, env, { error: "payload_too_large" }, 413);
  }
  let body;
  try {
    body = JSON.parse(raw);
  } catch {
    return json(request, env, { error: "invalid_json" }, 400);
  }
  const { subject, ciphertext, cfToken } = body || {};

  if (typeof ciphertext !== "string" || ciphertext.length > MAX_CIPHERTEXT_LEN) {
    return json(request, env, { error: "invalid_ciphertext" }, 400);
  }
  const armored = parseArmor(ciphertext);
  if (!armored) return json(request, env, { error: "invalid_ciphertext" }, 400);
  if (typeof cfToken !== "string" || !cfToken) {
    return json(request, env, { error: "missing_captcha" }, 400);
  }

  // Verify Turnstile
  const form = new URLSearchParams();
  form.append("secret", env.TURNSTILE_SECRET_KEY || "");
  form.append("response", cfToken);
  const ip = request.headers.get("CF-Connecting-IP");
  if (ip) form.append("remoteip", ip);

  const verifyRes = await fetch("https://challenges.cloudflare.com/turnstile/v0/siteverify", {
    method: "POST",
    body: form,
  });
  const verify = verifyRes.ok ? await verifyRes.json().catch(() => ({})) : {};
  if (!verify.success) {
    console.error("Turnstile verification failed", verifyRes.status, JSON.stringify(verify));
    return json(request, env, { error: "captcha_failed" }, 400);
  }
  const testKey = verify.hostname === "example.com"; // Cloudflare test keys report example.com
  if (!testKey && !allowedHostnames(env).includes(verify.hostname)) {
    console.error("Turnstile hostname not allowed:", verify.hostname);
    return json(request, env, { error: "captcha_failed" }, 400);
  }

  // Send via Resend: plaintext only, containing exactly one armored block
  const mailRes = await fetch("https://api.resend.com/emails", {
    method: "POST",
    headers: {
      Authorization: `Bearer ${env.RESEND_API_KEY}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      from: env.MAIL_FROM || "Secure Form <no-reply@kristiansagi.com>",
      to: (env.MAIL_TO || "kristian@kristiansagi.com").split(/\s*,\s*/),
      subject: cleanSubject(subject),
      text: armored,
    }),
  });

  if (!mailRes.ok) {
    console.error("Resend error", mailRes.status, await mailRes.text().catch(() => ""));
    return json(request, env, { error: "send_failed" }, 502);
  }
  return json(request, env, { ok: true }, 200);
}

async function safeHandle(request, env) {
  try {
    return await handleSendEncrypted(request, env);
  } catch (e) {
    console.error("Server error:", e);
    return json(request, env, { error: "server_error" }, 500);
  }
}

function preflight(request, env) {
  return new Response(null, { status: 204, headers: corsHeaders(request, env) });
}

// -- Cloudflare Pages Function entry points ---------------------------------

export const onRequestPost = ({ request, env }) => safeHandle(request, env);
export const onRequestOptions = ({ request, env }) => preflight(request, env);

// -- Standalone Worker entry point ------------------------------------------

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (request.method === "OPTIONS") return preflight(request, env);
    if (url.pathname === "/api/send-encrypted" && request.method === "POST") {
      return safeHandle(request, env);
    }
    return new Response("Not found", { status: 404 });
  },
};
