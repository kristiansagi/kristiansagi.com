// worker.js — Cloudflare Worker (Modules) with Turnstile + Resend + CORS

function corsHeaders(request) {
  const origin = request.headers.get("Origin");
  return {
    "Access-Control-Allow-Origin": origin || "*",
    "Access-Control-Allow-Methods": "POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type, Authorization",
    "Access-Control-Max-Age": "86400",
    "Vary": "Origin",
  };
}

function json(request, obj, status = 200, extra = {}) {
  return new Response(JSON.stringify(obj), {
    status,
    headers: {
      "content-type": "application/json; charset=utf-8",
      ...corsHeaders(request),
      ...extra,
    },
  });
}
function text(request, body, status = 200, extra = {}) {
  return new Response(body, { status, headers: { ...corsHeaders(request), ...extra } });
}

// -- helpers ---------------------------------------------------------------

function normalizeArmor(s) {
  // Trim BOM/whitespace and normalize newlines to \n
  let t = (s || "").replace(/^\uFEFF/, "").replace(/\r\n?/g, "\n").trim();

  const hasArmor = /-----BEGIN PGP MESSAGE-----/.test(t);
  if (hasArmor) {
    // Ensure exactly one BEGIN/END pair by extracting the first full block
    const m = t.match(/-----BEGIN PGP MESSAGE-----[\s\S]*?-----END PGP MESSAGE-----/);
    if (m) t = m[0];
  } else {
    // Wrap once if frontend sent only the base64 body
    t = `-----BEGIN PGP MESSAGE-----\n${t}\n-----END PGP MESSAGE-----`;
  }
  // Proton is fine with a trailing newline
  return t.endsWith("\n") ? t : t + "\n";
}

// -- main handler ----------------------------------------------------------

async function handleSendEncrypted(request, env) {
  if ((request.headers.get("content-type") || "").indexOf("application/json") === -1) {
    return text(request, "Unsupported Media Type", 415);
  }

  const { subject, ciphertext, cfToken } = await request.json().catch(() => ({}));

  if (!subject || typeof subject !== "string") return json(request, { error: "invalid_subject" }, 400);
  if (!ciphertext || typeof ciphertext !== "string") return json(request, { error: "invalid_ciphertext" }, 400);
  if (!cfToken || typeof cfToken !== "string") return json(request, { error: "missing_captcha" }, 400);

  // Verify Turnstile
  const ip = request.headers.get("CF-Connecting-IP") || "";
  const form = new URLSearchParams();
  form.append("secret", env.TURNSTILE_SECRET_KEY || "");
  form.append("response", cfToken);
  if (ip) form.append("remoteip", ip);

  const verifyRes = await fetch("https://challenges.cloudflare.com/turnstile/v0/siteverify", {
    method: "POST",
    body: form,
    headers: { "content-type": "application/x-www-form-urlencoded" },
  });
  if (!verifyRes.ok) {
    const body = await verifyRes.text().catch(() => "");
    return json(request, { error: "captcha_verify_http_error", status: verifyRes.status, body }, 502);
  }
  const verify = await verifyRes.json().catch(() => ({}));
  if (!verify.success) return json(request, { error: "captcha_failed", details: verify }, 400);

  // Prepare clean plaintext with ONE PGP block
  const armored = normalizeArmor(ciphertext);

  // Send via Resend
  const RESEND_API = "https://api.resend.com/emails";
  const from = env.MAIL_FROM || "Secure Form <no-reply@kristiansagi.com>";
  const to = (env.MAIL_TO || "kristian@kristiansagi.com").split(/\s*,\s*/);

  const mailBody = {
    from,
    to,
    subject,
    // Plaintext must contain ONLY the armored block
    text: armored,
    // Optional HTML for humans (safe to keep)
    html: armored,
    // Optional: still attach it for fallback
    // attachments: [{ filename: "message.asc", content: armored }],
    headers: {
      "Content-Transfer-Encoding": "7bit",
    },
  };
  

  const mailRes = await fetch(RESEND_API, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${env.RESEND_API_KEY}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify(mailBody),
  });

  if (!mailRes.ok) {
    const err = await mailRes.text().catch(() => "");
    return json(request, { error: "send_failed", details: err || null }, 502);
  }
  const payload = await mailRes.json().catch(() => ({}));
  return json(request, { ok: true, id: payload?.id || null }, 200);
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (request.method === "OPTIONS") {
      return new Response(null, { status: 204, headers: corsHeaders(request) });
    }
    if (url.pathname === "/api/send-encrypted" && request.method === "POST") {
      try {
        return await handleSendEncrypted(request, env);
      } catch (e) {
        console.error("Server error:", e);
        return json(request, { error: "server_error" }, 500);
      }
    }
    return text(request, "Not found", 404);
  },
};
