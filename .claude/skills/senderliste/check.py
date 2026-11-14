#!/usr/bin/env python3
"""Prüft die Standard-Senderliste sender.m3u.

Aufruf (aus dem Repo-Wurzelverzeichnis):
    python3 -I .claude/skills/senderliste/check.py            # Liste prüfen
    python3 -I .claude/skills/senderliste/check.py --compare  # zusätzlich mit Kodinerds abgleichen

Prüft je Eintrag: Pflichtattribute, doppelte URLs/Namen, ob die Master-Playlist
und eine Varianten-Playlist mit Segmenten erreichbar sind, höchste Auflösung,
Untertitel (UT) und ob das Logo lädt. Exit-Code 1, wenn etwas fehlschlägt.

Hinweis: Viele Streams sind auf Deutschland beschränkt (Geoblocking). Läuft das
Skript außerhalb Deutschlands, sind Fehler mit HTTP 403 kein Beweis für tote URLs.
"""
import concurrent.futures as cf
import pathlib
import re
import sys
import urllib.request
from urllib.parse import urljoin, urlparse

ROOT = pathlib.Path(__file__).resolve().parents[3]
M3U = ROOT / 'sender.m3u'
KODINERDS = 'https://raw.githubusercontent.com/jnk22/kodinerds-iptv/master/iptv/clean/clean_tv.m3u'
# Server der öffentlich-rechtlichen Sender (für den Abgleich mit Kodinerds)
OER_HOSTS = re.compile(r'ard-mcdn\.de|ard\.de|ndr\.de|br\.de|zdf-hls|kika|tagesschau|wdr|swr|mdr|rbb|hrhls|'
                       r'rbhlslive|srfs\.akamaized|artesimulcast')
# bewusst nicht aufgenommen (siehe SKILL.md): Event-Kanäle, Visual Radio, fremdsprachige Varianten
IGNORE = re.compile(r'Event|MDR\+|Visual\s*Radio|\(FR\)|\(EN\)', re.I)
HEADERS = {'User-Agent': 'Mozilla/5.0 (tv-senderliste-check)'}
REQUIRED = ('tvg-id', 'tvg-logo', 'group-title')


def get(url, limit=None):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=15) as r:
        return r.status, r.headers.get('Content-Type', ''), r.read(limit)


def parse(text):
    out, info = [], None
    for raw in text.splitlines():
        line = raw.strip()
        if line.startswith('#EXTINF'):
            attrs = dict(re.findall(r'([\w-]+)="([^"]*)"', line))
            attrs['name'] = re.sub(r'([\w-]+)="[^"]*"', '', line).split(',', 1)[1].strip()
            info = attrs
        elif line and not line.startswith('#') and info:
            info['url'] = line
            out.append(info)
            info = None
    return out


def probe(ch):
    res = {'ok': True, 'notes': []}
    try:
        _, _, body = get(ch['url'])
        master = body.decode('utf-8', 'replace')
        if '#EXTM3U' not in master:
            raise ValueError('keine M3U8-Playlist')
        heights = [int(h) for h in re.findall(r'RESOLUTION=\d+x(\d+)', master)]
        res['res'] = f'{max(heights)}p' if heights else '?'
        res['ut'] = 'TYPE=SUBTITLES' in master
        variants = [l for l in master.splitlines() if l and not l.startswith('#')]
        if variants:  # Master-Playlist: eine Variante muss Segmente liefern
            _, _, vbody = get(urljoin(ch['url'], variants[0]))
            if '#EXTINF' not in vbody.decode('utf-8', 'replace'):
                raise ValueError('Variante ohne Segmente')
        elif '#EXTINF' not in master:
            raise ValueError('Playlist ohne Segmente')
    except Exception as e:  # noqa: BLE001 – jeder Fehler ist ein Befund
        res['ok'] = False
        res['notes'].append(f'Stream: {getattr(e, "code", "")} {e}'.strip())
    try:
        _, ctype, _ = get(ch['tvg-logo'], 1024)
        if not ctype.startswith('image/'):
            res['notes'].append(f'Logo: kein Bild ({ctype})')
    except Exception as e:  # noqa: BLE001
        res['notes'].append(f'Logo: {e}')
    return res


def main():
    channels = parse(M3U.read_text(encoding='utf-8'))
    problems = 0
    if not M3U.read_text(encoding='utf-8').startswith('#EXTM3U'):
        print('FEHLER: sender.m3u beginnt nicht mit #EXTM3U'); problems += 1
    for key in ('url', 'name'):
        seen = {}
        for i, c in enumerate(channels, 1):
            if c[key] in seen:
                print(f'FEHLER: {key} doppelt: Nr. {seen[c[key]]} und Nr. {i} ({c[key]})'); problems += 1
            seen[c[key]] = i
    for i, c in enumerate(channels, 1):
        missing = [k for k in REQUIRED if not c.get(k)]
        if missing:
            print(f'FEHLER: Nr. {i} {c["name"]}: fehlt {", ".join(missing)}'); problems += 1

    with cf.ThreadPoolExecutor(12) as ex:
        results = list(ex.map(probe, channels))
    group = None
    for i, (c, r) in enumerate(zip(channels, results), 1):
        if c.get('group-title') != group:
            group = c.get('group-title')
            print(f'\n[{group}]')
        state = 'ok ' if r['ok'] else 'TOT'
        extra = f"{r.get('res', ''):>6} {'UT' if r.get('ut') else '  '}" if r['ok'] else ''
        print(f'{i:3} {state} {c["name"][:38]:38} {extra}  {"; ".join(r["notes"])}')
        problems += (not r['ok']) + len(r['notes'])

    if '--compare' in sys.argv:
        print('\nAbgleich mit Kodinerds (nur Server öffentlich-rechtlicher Sender):')
        kn = [c for c in parse(get(KODINERDS)[2].decode()) if OER_HOSTS.search(urlparse(c['url']).netloc + urlparse(c['url']).path)]
        ours = {c['url'] for c in channels}
        new = [c for c in kn if c['url'] not in ours and not IGNORE.search(c['name'])]
        for c in new:
            print(f'  nicht in sender.m3u: {c["name"]:34} {c["url"]}')
        if not new:
            print('  keine Abweichungen')

    print(f'\n{len(channels)} Sender, {problems} Befund(e)')
    sys.exit(1 if problems else 0)


if __name__ == '__main__':
    main()
