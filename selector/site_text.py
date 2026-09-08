# -*- coding: utf-8 -*-
"""Fetch a founder's website and reduce it to plain text for the profiler.

WHY THIS EXISTS AND WHY IT DID NOT UNTIL NOW. docs/engine-architecture.md says the website is
"load-bearing, not optional": product tags are the heaviest weight in the matcher and they are close
to underivable from a dropdown. "Fintech" describes four hundred companies in our data; "card
payments and same-day payouts for independent restaurants" describes one.

selector/profiler.py was built on 7 September with `site_text` as a parameter, and NOTHING EVER
FILLED IT. The parameter has been defaulting to an empty string, so the profiler has been reading
the founder's dropdown answers and nothing else, which is the exact weakness the architecture note
warns about. That is a gap I left and this closes it.

WHAT A FOUNDER'S WEBSITE IS: text nobody controls, fetched from an address a stranger typed into a
form. So this is written as a fetcher of hostile input, and every rule below is a rail:

  * ONE REQUEST, no redirects followed to a different host, three seconds, 400 KB.
  * PUBLIC HOSTS ONLY. The address is resolved and every resulting IP checked before the socket is
    opened: no loopback, no private range, no link-local, no cloud metadata endpoint. A server that
    will fetch any URL a stranger gives it is a server that will read its own internals and hand
    them back, and this is the single most common way that happens.
  * http and https only. No file:, no ftp:, no data:, no gopher:.
  * Markup, scripts, styles and comments are stripped, so what reaches the model is the words on
    the page and not the page's code.
  * The result is CAPPED and the profiler caps it again. Two caps on purpose.

WHAT IT NEVER DOES. It does not follow links, it does not crawl, it does not fetch a second page,
and it does not store anything. The text is used for one model call and dropped.

IT FAILS QUIET AND EMPTY. Every failure returns ('', reason). A founder whose site is down, slow,
behind a login or blocking robots still gets a reveal, built from their answers alone, which is
exactly what happens today for everyone. The reason is carried so the page can say the site could
not be read rather than silently giving a thinner answer.
"""
import ipaddress
import re
import socket
import urllib.parse
import urllib.request

TIMEOUT_S = 3.0
MAX_BYTES = 400 * 1024
MAX_CHARS = 12000
UA = 'FairwayProfiler/1.0 (+https://fairway.example; reads the page you gave us, once)'

_SCRIPTISH = re.compile(r'(?is)<(script|style|noscript|svg|template)\b.*?</\1\s*>')
_COMMENT = re.compile(r'(?s)<!--.*?-->')
_TAG = re.compile(r'(?s)<[^>]+>')
_WS = re.compile(r'[ \t\r\f\v]+')
_NL = re.compile(r'\n{3,}')


def _public(host):
    """True only if every address this host resolves to is a public one."""
    try:
        infos = socket.getaddrinfo(host, None)
    except (socket.gaierror, UnicodeError):
        return False, 'the address does not resolve'
    if not infos:
        return False, 'the address does not resolve'
    for info in infos:
        ip = info[4][0]
        try:
            a = ipaddress.ip_address(ip)
        except ValueError:
            return False, 'the address does not resolve to an IP'
        # is_global is False for loopback, private, link-local, reserved and multicast, which is
        # the whole list we care about, including 169.254.169.254 (cloud metadata).
        if not a.is_global:
            return False, 'the address points inside a private network'
    return True, ''


def normalise(url):
    """A founder types acme.com. Make it a URL, or say why it is not one."""
    u = (url or '').strip()
    if not u:
        return None, 'no website given'
    if '://' not in u:
        u = 'https://' + u
    p = urllib.parse.urlsplit(u)
    if p.scheme not in ('http', 'https'):
        return None, 'only http and https are read'
    if not p.hostname or '.' not in p.hostname:
        return None, 'that does not look like a web address'
    return urllib.parse.urlunsplit((p.scheme, p.netloc, p.path or '/', '', '')), ''


def to_text(html):
    s = _SCRIPTISH.sub(' ', html or '')
    s = _COMMENT.sub(' ', s)
    s = _TAG.sub('\n', s)
    # The handful of entities a marketing page actually uses. Anything else stays as written
    # rather than being decoded by a table that would then need maintaining.
    for a, b in (('&amp;', '&'), ('&nbsp;', ' '), ('&mdash;', ' '), ('&ndash;', ' '),
                 ('&rsquo;', "'"), ('&lsquo;', "'"), ('&quot;', '"'), ('&#39;', "'"),
                 ('&lt;', '<'), ('&gt;', '>')):
        s = s.replace(a, b)
    s = _WS.sub(' ', s)
    s = '\n'.join(line.strip() for line in s.split('\n'))
    s = _NL.sub('\n\n', s)
    return s.strip()[:MAX_CHARS]


def fetch(url, opener=None):
    """(text, reason). text is '' on any failure and reason says which, in plain words."""
    target, why = normalise(url)
    if not target:
        return '', why
    host = urllib.parse.urlsplit(target).hostname
    ok, why = _public(host)
    if not ok:
        return '', why
    req = urllib.request.Request(target, headers={
        'user-agent': UA,
        'accept': 'text/html,application/xhtml+xml',
        'accept-language': 'en',
    })
    try:
        # NO REDIRECT OFF THE HOST WE CHECKED. urllib follows redirects by default, and a redirect
        # is how a checked public address becomes an unchecked private one. The final URL is
        # re-checked rather than trusted.
        with (opener or urllib.request.urlopen)(req, timeout=TIMEOUT_S) as r:
            final = getattr(r, 'url', target)
            fhost = urllib.parse.urlsplit(final).hostname
            if fhost and fhost != host:
                ok, why = _public(fhost)
                if not ok:
                    return '', 'the site redirected somewhere we will not follow'
            ctype = (r.headers.get('content-type') or '') if hasattr(r, 'headers') else ''
            if ctype and 'html' not in ctype.lower() and 'text' not in ctype.lower():
                return '', 'that address is not a web page'
            raw = r.read(MAX_BYTES)
    except Exception as exc:                                   # noqa: BLE001
        return '', 'the site could not be read (%s)' % type(exc).__name__
    try:
        text = raw.decode('utf-8', errors='replace')
    except Exception:                                          # noqa: BLE001
        return '', 'the page is not readable text'
    out = to_text(text)
    if len(out) < 40:
        return '', 'the page had almost no text on it'
    return out, ''
