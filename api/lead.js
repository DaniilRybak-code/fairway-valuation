// Receives the completed check and puts it somewhere durable.
//
// Right now it always logs (visible in the Vercel runtime logs) and forwards to
// LEAD_WEBHOOK_URL if that env var is set — a Zapier/Make/Sheets webhook, or
// anything that accepts a JSON POST. Set it in Vercel → Project → Settings →
// Environment Variables. Until it's set, leads exist only in the logs, which is
// not a store — wire the destination before you send real traffic.
export default async function handler(req, res) {
  if (req.method !== 'POST') {
    res.status(405).json({ error: 'method_not_allowed' });
    return;
  }

  const lead = typeof req.body === 'string' ? safeParse(req.body) : (req.body || {});
  const record = { received_at: new Date().toISOString(), ...lead };

  console.log('[fairway-lead]', JSON.stringify(record));

  let forwarded = false;
  const hook = process.env.LEAD_WEBHOOK_URL;
  if (hook) {
    try {
      const r = await fetch(hook, {
        method: 'POST',
        headers: { 'content-type': 'application/json' },
        body: JSON.stringify(record)
      });
      forwarded = r.ok;
      if (!r.ok) console.error('[fairway-lead] webhook returned', r.status);
    } catch (err) {
      console.error('[fairway-lead] forward failed:', err && err.message);
    }
  }

  // Always 200: a storage failure must not cost the founder their result screen.
  res.status(200).json({ ok: true, forwarded });
}

function safeParse(s) {
  try { return JSON.parse(s); } catch (e) { return { raw: s }; }
}
