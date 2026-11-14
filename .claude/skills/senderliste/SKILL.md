---
name: senderliste
description: Aufbau, Regeln und Pflege der Standard-Senderliste sender.m3u (deutsche öffentlich-rechtliche TV-Sender). Verwenden, wenn Sender hinzugefügt, entfernt, umsortiert oder Stream-URLs aktualisiert werden sollen, wenn ein Sender in der App nicht mehr läuft oder wenn die Liste geprüft werden soll.
---

# Standard-Senderliste `sender.m3u`

`sender.m3u` im Repo-Wurzelverzeichnis ist die Senderliste, die die App ohne eigene Liste lädt (`DEFAULT_URL` in `index.html`). Sie enthält **ausschließlich deutsche öffentlich-rechtliche Sender**.

## Prüfen

```sh
python3 -I .claude/skills/senderliste/check.py            # alle Einträge prüfen
python3 -I .claude/skills/senderliste/check.py --compare  # zusätzlich: Kodinerds nach neuen/geänderten URLs durchsuchen
```

Das Skript meldet je Sender `ok`/`TOT`, die höchste Auflösung, ob Untertitel (`UT`) vorhanden sind und ob das Logo lädt. Exit-Code 1 bei Befunden. Viele Streams sind auf Deutschland beschränkt: Ein HTTP 403 außerhalb Deutschlands heißt nicht, dass die URL tot ist.

## Was aufgenommen wird

- Nur deutsche öffentlich-rechtliche Fernsehsender (ARD-Anstalten, ZDF und Gemeinschaftsprogramme wie 3sat, ARTE, phoenix, KiKA).
- Nur **offizielle Stream-URLs von den Servern der Sender** (z. B. `*.ard-mcdn.de`, `mcdn.ndr.de`, `mcdn.br.de`, `zdf-hls-*.akamaized.net`, `*hls*.akamaized.net` der jeweiligen Anstalt).
- **Nicht** aufnehmen:
  - URLs mit Zugangsschlüsseln/Tokens (`?hdnts=`, `?token=`, `exp=` …): Sie laufen ab, und sie fest einzutragen wäre eine Umgehung von Zugangsbeschränkungen.
  - Weiterverbreitungen über fremde Server (z. B. `antik.sk`, `freem3u`, IP-Adressen, `amagi.tv`).
  - Event-Kanäle (ARD/ZDF/WDR/SWR/rbb Event, MDR+), Visual Radio, fremdsprachige Varianten (ARTE FR).
  - Ausländische Sender (ORF, SRF, BBC): rechtlich bewusst ausgeschlossen (Geoblocking, Login-Pflicht bei der BBC).
- Deutsche Welle: Derzeit gibt es keinen deutschsprachigen DW-Stream in den Quellen (102 = Englisch, 103 = Arabisch, 104 = Spanisch, 110 = Russisch). Aufnehmen, sobald eine offizielle deutsche URL auftaucht.

## Reihenfolge (= Sendernummer)

1. **Vollprogramme** (`group-title="Vollprogramme"`): Das Erste (1), ZDF (2), 3sat, ARTE.
2. **Spartenkanäle** (`group-title="Spartenkanäle"`): erst ARD (tagesschau24, ONE, ARD-alpha), dann ZDF (ZDFneo, ZDFinfo), dann gemeinsame (phoenix, KiKA).
3. **Dritte Programme**, `group-title` = Name der Anstalt.

### Sortierregel für die Dritten: lesen wie eine Landkarte

- Die **Sendegebiete** werden in **Reihen von Nord nach Süd** eingeteilt, **innerhalb einer Reihe von West nach Ost** gelesen, so wie man eine Karte zeilenweise liest.
- Das gilt zuerst für die **Anstalten** (nach ihrem gesamten Sendegebiet, nicht nach dem Sitz) und dann **innerhalb jeder Anstalt für die Regionalfenster**. Eine Anstalt bleibt immer zusammen.
- **Enklaven** folgen direkt auf das Gebiet, das sie umschließt: Radio Bremen nach dem NDR, Berlin nach Brandenburg.
- Bei den WDR-Lokalzeiten zählt der Studio-Standort als Lage des Sendegebiets.

Die Reihen sind eine Entscheidung nach Augenmaß auf der Karte, keine Rechenformel. Verbindlich ist diese Tabelle (`|` trennt die Reihen, `,` die Gebiete innerhalb einer Reihe):

| Reihe | Anstalten West → Ost | Regionalfenster |
|---|---|---|
| Nord | **NDR** | Schleswig-Holstein \| Hamburg, Mecklenburg-Vorpommern \| Niedersachsen |
| Nord | **Radio Bremen** (Enklave im NDR-Gebiet) | – |
| Mitte | **WDR** | Münsterland, Ostwestfalen \| Duisburg, Ruhr (Essen), Dortmund \| Düsseldorf, Bergisches Land (Wuppertal) \| Aachen, Köln, Bonn, Südwestfalen (Siegen) |
| Mitte | **hr** | – |
| Mitte | **MDR** | Sachsen-Anhalt \| Thüringen, Sachsen |
| Mitte | **rbb** | Brandenburg, Berlin (Enklave) |
| Süd | **SR** | – |
| Süd | **SWR** | Rheinland-Pfalz \| Baden-Württemberg |
| Süd | **BR** | Nord (Franken) \| Süd (Altbayern/Schwaben) |

Ein neues Regionalfenster wird nach demselben Prinzip in die passende Reihe eingeordnet. Danach diese Tabelle, den Kommentar über dem Block in `sender.m3u` und die Tabelle in `README.md` anpassen. Der WDR-Hauptstream (`/wdr/live/`) ist das Kölner Fenster und heißt in der Liste „WDR Köln“.

## Format eines Eintrags

```
#EXTINF:-1 tvg-id="WDRFernsehenWuppertal.de" tvg-logo="https://raw.githubusercontent.com/jnk22/kodinerds-iptv/master/logos/tv/wdrhd.png" group-title="WDR",WDR Bergisches Land (Wuppertal)
https://wdr-live.ard-mcdn.de/wdr/wuppertal/hls/de/master.m3u8
```

- Pflicht: `tvg-id`, `tvg-logo`, `group-title`, Name nach dem Komma, URL in der nächsten Zeile.
- Name ohne „HD“. Bei Regionalfenstern, deren Name nicht die Stadt nennt, die Stadt in Klammern ergänzen.
- `tvg-id`: wenn vorhanden die ID aus Kodinerds/iptv-org, sonst nach dem Muster `<Sender><Region>.de`. Muss nicht eindeutig gültig sein, wird derzeit nur mitgeführt.
- Logos werden aus dem Kodinerds-Repo verlinkt (`logos/tv/*.png`), nicht ins Repo kopiert.
- `#`-Kommentarzeilen sind erlaubt und werden von der App ignoriert. Die Kopfkommentare und die `# Reihe … – <Anstalt>: …`-Trenner beibehalten.

## Wo neue URLs zu finden sind

1. [Kodinerds IPTV](https://github.com/jnk22/kodinerds-iptv), Datei `iptv/clean/clean_tv.m3u`, Gruppe `IPTV-DE`: beste Quelle für deutsche Sender und Regionalvarianten. Achtung, die Namen dort sind nicht immer korrekt: Die DW-Einträge zeigen z. B. auf den englischen bzw. russischen Stream.
2. [iptv-org](https://github.com/iptv-org/iptv): `https://iptv-org.github.io/api/streams.json` (Feld `channel`, `url`) bzw. `countries/de.m3u`. Nur Einträge von offiziellen Sender-Servern übernehmen.
3. Die Livestream-Seiten der Sender selbst (ARD Mediathek, ZDF-Livestream, Seiten der Dritten). Im Browser unter Netzwerk nach `master.m3u8` filtern.

Vor dem Übernehmen einer URL prüfen: Master-Playlist enthält bei mehrsprachigen Sendern die richtige Sprache (`LANGUAGE=` in `#EXT-X-MEDIA`), kein Token in der URL, offizielle Domain.

## Ablauf bei Änderungen

1. `sender.m3u` bearbeiten und die Reihenfolge-Regeln einhalten.
2. `check.py` ausführen, Befunde beheben. Mit `--compare` nach neuen oder geänderten URLs suchen.
3. Lokal testen: `python3 -m http.server 8000` → `http://localhost:8000`. Gilt nur, wenn im Browser keine eigene Liste gespeichert ist (Editor → Liste leeren → Übernehmen).
4. Die Tabelle „Standardliste“ in `README.md` anpassen, falls sich Sender ändern.
5. Commit mit einer Nachricht, die nennt, welche Sender sich geändert haben.
