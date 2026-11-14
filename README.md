# TV

Öffentlich frei empfangbare deutsche TV-Livestreams in einer Oberfläche, die sich wie ein Fernseher bedienen lässt: Sender mit den Pfeiltasten durchschalten, Nummer direkt eingeben, Senderliste, Lautstärke, Vollbild.

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
| I | Senderinfo anzeigen |
| F · Doppelklick | Vollbild an / aus |
| R | Stream neu laden |
| H · ? | Hilfe |

Der erste Tastendruck schaltet ins Vollbild und – falls der Browser Autoplay mit Ton blockiert – den Ton ein. Zuletzt gesehener Sender, Lautstärke und die Senderliste werden im Browser gespeichert.

## Als App installieren

1. <https://sigtec.github.io/tv/> in Chrome öffnen.
2. In der Adressleiste auf das Installieren-Symbol klicken (oder Menü ⋮ → *Streamen, speichern und teilen* → *Seite als App installieren*).

Die App startet danach in einem eigenen Fenster ohne Browserleiste.

## Eigene Senderliste

Über den Parameter `m3u` lässt sich jede andere M3U-Playlist laden, sofern ihr Server CORS erlaubt:

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
| `icons/` | App-Icons |

## Credits

- **Senderliste:** [josxha/german-tv-m3u](https://github.com/josxha/german-tv-m3u) – gepflegte M3U-Liste öffentlich frei empfangbarer deutscher TV-Sender. Die Liste wird bei jedem Start direkt aus diesem Repository geladen. Vielen Dank!
- **Wiedergabe:** [hls.js](https://github.com/video-dev/hls.js) (Apache-2.0), eingebunden über jsDelivr.

## Hinweis

Dieses Projekt hostet und verbreitet keine Streams. Es spielt ausschließlich die öffentlich zugänglichen Livestreams ab, die die Sender selbst anbieten und die in der oben genannten Liste verlinkt sind. Alle Rechte an Programm, Namen und Logos liegen bei den jeweiligen Sendern. Einige Streams sind nur aus Deutschland abrufbar (Geoblocking).
