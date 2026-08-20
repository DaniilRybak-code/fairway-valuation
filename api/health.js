/* Deployment fingerprint. Open <your-url>/api/health in a browser.
 *
 * If this 404s you are looking at an old deployment that predates Git, not at
 * the current build. If `build` is not the value below, the same applies.
 *
 * Only booleans are returned for env vars. No values, ever.
 */
export default function handler(req, res) {
  res.setHeader('cache-control', 'no-store');
  res.status(200).json({
    ok: true,
    build: 'nine-step-v5',
    commit: process.env.VERCEL_GIT_COMMIT_SHA || null,
    branch: process.env.VERCEL_GIT_COMMIT_REF || null,
    deployed_at: process.env.VERCEL_DEPLOYMENT_ID || null,
    env_present: {
      LEAD_WEBHOOK_URL: !!process.env.LEAD_WEBHOOK_URL,
      LEAD_SHARED_SECRET: !!process.env.LEAD_SHARED_SECRET,
      ANTHROPIC_API_KEY: !!process.env.ANTHROPIC_API_KEY
    },
    expected: {
      quiz_steps: 9,
      hook_variants: ['frustration', 'readiness', 'reveal'],
      note: 'If the site logs hook_variant "combo" or 8 steps, it is an older deployment.'
    }
  });
}
