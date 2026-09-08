/* Draws every fork question with the page's own renderer, so check 20 can assert the markup
   exists rather than assuming it. quiz-fork.js is a browser script, so the handful of globals it
   touches are stubbed; nothing else about it is changed. */
import { createRequire } from 'module';
import { readFileSync } from 'fs';
const require = createRequire(import.meta.url);
const ROOT = new URL('..', import.meta.url).pathname.replace(/\/$/, '');

global.responses = {};
global.track = function () {};
global.document = { getElementById: () => null, querySelectorAll: () => [], querySelector: () => null };
global.curSymbol = () => '$';

const QF = require(ROOT + '/quiz-fork.js');
const cases = JSON.parse(readFileSync(process.argv[2], 'utf8'));
console.log(JSON.stringify(cases.map(function (q) {
  let html = '';
  try { html = QF.qfQuestion(q); } catch (e) { html = ''; }
  return {
    key: q.key,
    ok: typeof html === 'string' && html.length > 40 && html.indexOf(q.key) > -1,
    has_id: q.kind === 'choice' ? html.indexOf('data-q="' + q.key + '"') > -1
                                : html.indexOf('id="qf-' + q.key + '"') > -1
  };
})));
