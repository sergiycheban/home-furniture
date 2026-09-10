"""Prepare exported furniture previews for standalone use and index.html.

Run after replacing a *-preview.html with a fresh visualization export.
Only the page wrapper changes; furniture markup, dimensions and interactions stay.
"""
from html import escape
from html.parser import HTMLParser
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
PREVIEWS = {
    "wardrobe-preview.html": "Шкаф в спальне",
    "hallway-preview.html": "Шкаф в прихожей",
    "laundry-preview.html": "Шкаф в постирочной",
    "bathroom-preview.html": "Тумба в ванной",
    "kitchen-preview.html": "Г-образная кухня",
}
START = "<!-- furniture-preview:start -->"
END = "<!-- furniture-preview:end -->"


class ExportParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.inner = None

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if tag == "iframe" and "srcdoc" in values:
            self.inner = values["srcdoc"]


def prepare(filename, title):
    path = ROOT / filename
    document = path.read_text(encoding="utf-8")
    parser = ExportParser()
    parser.feed(document)
    if parser.inner:
        document = parser.inner
    document = re.sub(re.escape(START) + r".*?" + re.escape(END) + r"\n?", "", document, flags=re.S)
    document = re.sub(r'<html\b[^>]*>', '<html lang="ru" data-furniture-preview>', document, count=1)
    document = re.sub(r'<title>.*?</title>', '<title>' + escape(title) + ' — Мебель для дома</title>', document, count=1, flags=re.S)
    # These schemes use neither tooltip triggers nor Lucide icons.
    # Remove the unused CDN runtime so the album works without internet access.
    if not re.search(r'<[^>]+\bdata-(?:tooltip|lucide)\b', document):
        document = re.sub(r'<script\b[^>]*\bsrc="https://unpkg\.com/[^"]*"[^>]*>\s*</script>', '', document)
        document = re.sub(r'<script>(?:(?!</script>).)*?(?:window\.FloatingUIDOM|const initialize = \(\) =>)(?:(?!</script>).)*?</script>', '', document, flags=re.S)
    host_css = """:root{color-scheme:light!important;--background:#fff;background:#fff!important}
html{margin:0;min-height:0}html>body{display:flow-root;margin:0;padding:0;min-height:0;background:#fff}
body>div[id]{max-width:960px;margin-inline:auto}"""
    bridge = (ROOT / "assets" / "preview.js").read_text(encoding="utf-8")
    managed = f'{START}\n<style>{host_css}</style>\n<script>\n{bridge}\n</script>\n{END}'
    document = document.replace('</body>', managed + '\n</body>')
    path.write_text(document, encoding="utf-8", newline="\n")
    print(filename)


if __name__ == "__main__":
    for filename, title in PREVIEWS.items():
        prepare(filename, title)
