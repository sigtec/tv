# TV

Die Livestreams der deutschen öffentlich-rechtlichen Sender in einer Oberfläche, die sich wie ein Fernseher bedienen lässt: Sender mit den Pfeiltasten durchschalten, Nummer direkt eingeben, Senderliste, Lautstärke, Vollbild.

**Live:** <https://sigtec.github.io/tv/>

Die Seite ist eine einzelne HTML-Datei ohne Build-Schritt und lässt sich in Chrome bzw. Edge als App (PWA) installieren.

## Bedienung

| Taste | Funktion |
|---|---|
| ↑ / ↓ · Bild↑ / Bild↓ | Sender weiter / zurück |
| 0 – 9 | Sendernummer direkt eingeben |
| Enter · Leertaste · Klick | Senderliste öffnen |
| Rücktaste | Zum vorherigen Sender |
| ← / → | Leiser / lauter |
| M | Ton aus / an |
| U | Untertitel an / aus |
| I | Senderinfo anzeigen |
| E | Senderliste bearbeiten |
| F · Doppelklick | Vollbild an / aus |
| R | Stream neu laden |
| H · ? | Hilfe |

Der erste Tastendruck schaltet ins Vollbild und – falls der Browser Autoplay mit Ton blockiert – den Ton ein. Zuletzt gesehener Sender, Lautstärke, Untertitel-Einstellung und die Senderliste werden im Browser gespeichert.

**Untertitel** bieten vor allem ARD, ZDF, 3sat, phoenix, KiKA und die Dritten an. Ob ein Sender welche hat, zeigt die Senderinfo mit „UT“ an.

## Als App installieren

1. <https://sigtec.github.io/tv/> in Chrome öffnen.
2. In der Adressleiste auf das Installieren-Symbol klicken (oder Menü ⋮ → *Streamen, speichern und teilen* → *Seite als App installieren*).

Die App startet danach in einem eigenen Fenster ohne Browserleiste.

## Standardliste

Ohne eigene Liste lädt die App [`sender.m3u`](sender.m3u) aus diesem Repository. Sie enthält ausschließlich deutsche öffentlich-rechtliche Sender, alle mit den offiziellen Stream-Adressen der Sender:

| Nr. | Sender |
|---|---|
| 1–4 | Das Erste, ZDF, 3sat, ARTE |
| 5–11 | tagesschau24, ONE, ARD-alpha, ZDFneo, ZDFinfo, phoenix, KiKA |
| 12–15 | NDR Schleswig-Holstein, Hamburg, Mecklenburg-Vorpommern, Niedersachsen |
| 16 | Radio Bremen TV |
| 17–27 | WDR mit allen Lokalzeit-Regionen: Münsterland, Ostwestfalen, Duisburg, Ruhr, Dortmund, Düsseldorf, Bergisches Land, Aachen, Köln, Bonn, Südwestfalen |
| 28 | hr-fernsehen |
| 29–31 | MDR Sachsen-Anhalt, Thüringen, Sachsen |
| 32–33 | rbb Brandenburg, Berlin |
| 34 | SR Fernsehen |
| 35–36 | SWR Rheinland-Pfalz, Baden-Württemberg |
| 37–38 | BR Fernsehen Nord, Süd |

Die Dritten sind gelesen wie eine Landkarte: Sendegebiete in Reihen von Nord nach Süd, in jeder Reihe von West nach Ost. Das gilt für die Anstalten und ebenso für die Regionalfenster innerhalb einer Anstalt. Enklaven wie Bremen und Berlin folgen direkt auf das umschließende Gebiet. Die Regeln für Aufbau und Pflege stehen in [`.claude/skills/senderliste/SKILL.md`](.claude/skills/senderliste/SKILL.md), geprüft wird die Liste mit:

```sh
python3 -I .claude/skills/senderliste/check.py --compare
```

## Eigene Senderliste

Mit **E** (oder *✎ Bearbeiten* in der Senderliste) öffnet sich der Listen-Editor:

- **Links** wählst du eine Quelle und fügst Sender mit **+** oder per Doppelklick hinzu. Suchen und nach Gruppen filtern ist möglich. Eigene Quellen kommen über **+ Quelle** dazu (beliebige M3U-URL), einzelne Streams über **+ Eigenen Stream eintragen**.
- **Rechts** steht deine Liste. Die Reihenfolge ergibt die Sendernummern. Sortieren geht per Ziehen oder mit ↑ ↓, außerdem lassen sich Sender umbenennen (✎) und entfernen (✕).
- **Übernehmen** speichert die Liste im Browser. **M3U exportieren** und **M3U importieren** übertragen sie auf andere Geräte oder Browser.
- **Liste leeren** und Übernehmen schaltet zurück auf die Standardliste.

Vorhandene Quellen:

| Quelle | Inhalt |
|---|---|
| Öffentlich-rechtlich (Standard) | Die Standardliste `sender.m3u` aus diesem Repository |
| [josxha/german-tv-m3u](https://github.com/josxha/german-tv-m3u) | Kompakte Liste deutscher Free-TV-Sender inkl. Privat- und Lokalsender |
| [Kodinerds IPTV](https://github.com/jnk22/kodinerds-iptv) | Umfangreich, mit allen Regionalvarianten der Dritten (z. B. WDR Lokalzeit Bergisches Land, NDR Hamburg, MDR Thüringen) |
| [iptv-org](https://github.com/iptv-org/iptv) | Große Sammlung, Qualität gemischt |
| [Free-TV/IPTV](https://github.com/Free-TV/IPTV) | Kleine kuratierte Auswahl |

Über den Parameter `m3u` lässt sich außerdem einmalig eine andere M3U-Playlist laden, sofern ihr Server CORS erlaubt. Sie hat Vorrang vor der eigenen Liste:

```
https://sigtec.github.io/tv/?m3u=https://example.org/meine-liste.m3u
```

## Lokal ausprobieren

Der Service Worker braucht `http://localhost` oder HTTPS, also einen kleinen Webserver statt `file://`:

```sh
python3 -m http.server 8000
# dann http://localhost:8000 öffnen
```

## Dateien

| Datei | Zweck |
|---|---|
| `index.html` | Die komplette App (HTML, CSS, JavaScript) |
| `manifest.webmanifest` | App-Name, Icons und Anzeigemodus für die Installation |
| `sw.js` | Service Worker; hält die App-Hülle offline bereit, Streams laufen direkt |
| `sender.m3u` | Standard-Senderliste |
| `icons/` | App-Icons |
| `.claude/skills/senderliste/` | Regeln und Prüfskript für die Standardliste |

## Credits

- **Senderlisten:** Die Stream-Adressen und Logos der Standardliste stammen aus [Kodinerds IPTV](https://github.com/jnk22/kodinerds-iptv) und [josxha/german-tv-m3u](https://github.com/josxha/german-tv-m3u); die Logos werden direkt aus dem Kodinerds-Repository geladen. Im Editor stehen außerdem [iptv-org](https://github.com/iptv-org/iptv) und [Free-TV/IPTV](https://github.com/Free-TV/IPTV) als Quellen bereit. Vielen Dank an alle, die diese Listen pflegen!
- **Wiedergabe:** [hls.js](https://github.com/video-dev/hls.js) (Apache-2.0), eingebunden über jsDelivr.

## Hinweis

Dieses Projekt hostet und verbreitet keine Streams. Es spielt ausschließlich die öffentlich zugänglichen Livestreams ab, die die Sender selbst anbieten und die in den genannten Listen verlinkt sind. Alle Rechte an Programm, Namen und Logos liegen bei den jeweiligen Sendern. Einige Streams sind nur aus Deutschland abrufbar (Geoblocking).
