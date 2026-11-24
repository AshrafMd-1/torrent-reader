# torrent-viewer

Turn a `.torrent` file into a single, self-contained HTML page — a clean file manager view of what's inside the torrent, without downloading anything or opening a BitTorrent client.

## Quick start

```bash
python3 torrent-to-html.py <file.torrent> <output.html>
open <output.html>
```

Example:

```bash
python3 torrent-to-html.py ~/Downloads/ubuntu.torrent ~/Downloads/ubuntu.html
```

## What the page shows

- **Summary** — total size, file count, folder count, largest file, piece count and piece size.
- **Info hash** — with copy-to-clipboard and a ready-made magnet link.
- **File tree** — expandable folders, per-file sizes, and a bar showing each item's share of the torrent.
- **Search** — flattens the tree to matching paths and highlights the matched text. Press `/` to focus, `Esc` to clear.
- **Extension filters** — one chip per file type with its count; combine with search.
- **Sortable columns** — name or size, ascending/descending. Folders always stay above files.
- **Trackers and metadata** — full tracker list, creator, creation date and comment.

Everything renders client-side. No network requests, no external fonts, no dependencies.

## Why the HTML is portable

The torrent metadata is embedded into the page as inline JSON. The generated file has no external `src` or `href` references and never reads the original `.torrent` again, so you can rename it, move it, archive it, or send it to someone else — it will keep working offline.

## Files

| File | Purpose |
| --- | --- |
| `torrent-to-html.py` | Reads the torrent, parses the bencode, writes the HTML. |
| `template.html` | The page template with `/*__DATA__*/null` as the data placeholder. Must stay next to the script. |
| `README.md` | This file. |

## Requirements

Python 3.8+. Standard library only — no installs.

## Notes

- Handles both multi-file and single-file torrents, deeply nested paths, and non-UTF-8 filenames (falls back from UTF-8 to cp1252 to latin-1).
- Output is UTF-8 and human-readable; names are HTML-escaped.
- Only the v1 (SHA-1) info hash is reported.
