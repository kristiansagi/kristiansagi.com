// Cloudflare Pages Function / Worker
// File: /functions/api/send-encrypted.js
// Purpose: receive encrypted message from the form and send it via Resend

export default {
  async fetch(request, env) {
    // --- CORS configuration ---
    const cors = {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type, Authorization'
    };

    // --- Handle CORS preflight (OPTIONS request) ---
    if (request.method === 'OPTIONS') {
      return new Response(null, { headers: cors });
    }

    if (request.method !== 'POST') {
      return new Response('Only POST allowed', {
        status: 405,
        headers: cors
      });
    }

    try {
      const { subject, ciphertext } = await request.json();
      if (!ciphertext || !subject) {
        return new Response('Missing ciphertext or subject', {
          status: 400,
          headers: cors
        });
      }

      // Prepare plain text email (Proton auto-decrypts inline)
      const bodyText = ciphertext.trim();

      // --- Send via Resend API ---
      const r = await fetch('https://api.resend.com/emails', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${env.RESEND_API_KEY}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          from: 'Kristian <no-reply@kristiansagi.com>',
          to: ['kristian@kristiansagi.com'],
          subject,
          text: bodyText,
          html: null
        })
      });

      if (!r.ok) {
        const t = await r.text().catch(() => '');
        throw new Error(`Resend failed: ${r.status} ${t}`);
      }

      return new Response(JSON.stringify({ ok: true }), {
        headers: { 'Content-Type': 'application/json', ...cors }
      });
    } catch (err) {
      return new Response(
        JSON.stringify({ ok: false, error: err.message || String(err) }),
        { status: 500, headers: { 'Content-Type': 'application/json', ...cors } }
      );
    }
  }
};
