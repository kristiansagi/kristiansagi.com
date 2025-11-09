// Cloudflare Pages Function (JavaScript) with CORS + Turnstile + Resend

// Env vars (Pages → Settings → Environment variables):
// TURNSTILE_SECRET_KEY, RESEND_API_KEY
// Optional: RESEND_FROM, RESEND_TO

const corsHeaders = (request) => {
  const origin = request.headers.get('Origin');
  // Echo the origin for dev/prod; tighten if you want only your domains.
  return {
    'Access-Control-Allow-Origin': origin || '*',
    'Access-Control-Allow-Methods': 'POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type, Authorization',
    'Access-Control-Max-Age': '86400',
    'Vary': 'Origin',
  };
};

const json = (request, obj, status = 200, extra = {}) =>
  new Response(JSON.stringify(obj), {
    status,
    headers: {
      'content-type': 'application/json; charset=utf-8',
      ...corsHeaders(request),
      ...extra,
    },
  });

const text = (request, body, status = 200, extra = {}) =>
  new Response(body, { status, headers: { ...corsHeaders(request), ...extra } });

// Handle CORS preflight
export const onRequestOptions = async ({ request }) =>
  new Response(null, { status: 204, headers: corsHeaders(request) });

// Main POST
export const onRequestPost = async ({ request, env }) => {
  try {
    if (!(request.headers.get('content-type') || '').includes('application/json')) {
      return text(request, 'Unsupported Media Type', 415);
    }

    const { subject, ciphertext, cfToken } = await request.json();
    if (!subject || typeof subject !== 'string')  return json(request, { error: 'invalid_subject' }, 400);
    if (!ciphertext || typeof ciphertext !== 'string') return json(request, { error: 'invalid_ciphertext' }, 400);
    if (!cfToken || typeof cfToken !== 'string') return json(request, { error: 'missing_captcha' }, 400);

    // Verify Turnstile
    const ip = request.headers.get('CF-Connecting-IP') || '';
    const verifyForm = new URLSearchParams();
    verifyForm.append('secret', env.TURNSTILE_SECRET_KEY);
    verifyForm.append('response', cfToken);
    if (ip) verifyForm.append('remoteip', ip);

    const verifyRes = await fetch('https://challenges.cloudflare.com/turnstile/v0/siteverify', {
      method: 'POST',
      body: verifyForm,
      headers: { 'content-type': 'application/x-www-form-urlencoded' },
    });
    if (!verifyRes.ok) return json(request, { error: 'captcha_verify_http_error' }, 502);

    const verify = await verifyRes.json();
    if (!verify.success) return json(request, { error: 'captcha_failed', details: verify }, 400);

    // Send email via Resend
    const RESEND_API = 'https://api.resend.com/emails';
    const from = env.RESEND_FROM || 'Secure Form <secure@kristiansagi.com>';
    const to = (env.RESEND_TO || 'kristian@kristiansagi.com').split(/\s*,\s*/);

    const mailRes = await fetch(RESEND_API, {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${env.RESEND_API_KEY}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        from,
        to,
        subject,
        text:
`You received an encrypted message.

-----BEGIN PGP MESSAGE-----
${ciphertext}
-----END PGP MESSAGE-----`,
      }),
    });

    if (!mailRes.ok) {
      const err = await mailRes.text().catch(() => '');
      return json(request, { error: 'send_failed', details: err || null }, 502);
    }

    const payload = await mailRes.json().catch(() => ({}));
    return json(request, { ok: true, id: payload?.id || null }, 200);
  } catch (e) {
    return json(request, { error: 'server_error' }, 500);
  }
};
