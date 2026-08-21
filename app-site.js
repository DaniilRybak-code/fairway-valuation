/* The website question.
 *
 * Loaded after app.js. It is a separate file because it is the input the peer
 * selection will lean on hardest: the model reads what the company actually
 * does from here, rather than inferring it from the sector box they ticked.
 *
 * It binds to the field itself rather than to the step's exit, so it works
 * whichever way the founder leaves step 2, including autofill, and it never
 * blocks: an empty or unparseable value costs a sharper comp set, not the reveal.
 */
(function () {
  const el = document.getElementById('site-url');
  if (!el) return;

  function captureSite() {
    let v = (el.value || '').trim();
    if (!v) { responses.website = null; return; }
    if (!/^https?:\/\//i.test(v)) v = 'https://' + v;
    /* A hostname with at least one dot and a plausible TLD. Anything else is
       stored as null rather than handed to a fetcher that will just fail. */
    responses.website = /^https?:\/\/[^\s.]+\.[^\s]{2,}$/i.test(v) ? v : null;
  }

  ['input', 'change', 'blur'].forEach(function (evt) {
    el.addEventListener(evt, captureSite);
  });

  /* Belt and braces. Some browsers autofill without firing an input event, so
     re-read the field on the way out of the step rather than trusting that one
     of the handlers above ran. Capture phase, so it lands before the click
     handler that advances the step. */
  ['sector-grid', 'sector-other-wrap'].forEach(function (id) {
    const wrap = document.getElementById(id);
    if (wrap) wrap.addEventListener('click', captureSite, true);
  });

  el.addEventListener('blur', function () {
    if (responses.website) track('website_given', { host: responses.website.replace(/^https?:\/\//i, '').split('/')[0] });
  });
})();
