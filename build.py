"""Gera index.html a partir de body.html + style.css + script.js + logos/*.png.

Uso:
    python3 build.py
"""
import base64
import math
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TITLE = "Marxismo, passo a passo"
DATE = "16/11/2026"
FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">\n'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,600;1,6..72,400&display=swap">')
MOON = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" '
        'stroke-linejoin="round" aria-hidden="true"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/></svg>')


def read(name):
    with open(os.path.join(HERE, name), encoding="utf-8") as f:
        return f.read()


def toc(content):
    items = []
    for m in re.finditer(r'<(p class="part-label"|h2|h3 data-toc) id="([^"]+)"[^>]*>(.*?)</(?:p|h2|h3)>', content, re.S):
        cls = {"p": "l1", "h2": "l2", "h3": "l3"}[m.group(1)[:2].rstrip(" ")]
        text = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", m.group(3))).strip()
        items.append(f'<li><a class="{cls}" href="#{m.group(2)}">{text}</a></li>')
    return "".join(items)


def embed_logos(content):
    """Troca {{logo:slug}} pelo PNG de logos/slug.png embutido como data URI."""
    def one(m):
        with open(os.path.join(HERE, "logos", m.group(1) + ".png"), "rb") as f:
            return "data:image/png;base64," + base64.b64encode(f.read()).decode()
    return re.sub(r"\{\{logo:([a-z0-9]+)\}\}", one, content)


# Empresas (guarda-chuva) e as marcas ao redor: (slug do logo ou None, nome)
MARCAS = [
    ("nestle", "Nestlé", [("nescafe", "Nescafé"), ("kitkat", "KitKat"), ("purina", "Purina"), (None, "Ninho"), (None, "Nescau")]),
    ("pg", "Procter & Gamble", [("gillette", "Gillette"), ("oralb", "Oral-B"), ("pantene", "Pantene"), (None, "Pampers"), (None, "Ariel")]),
    ("unilever", "Unilever", [("dove", "Dove"), ("knorr", "Knorr"), (None, "Hellmann's"), (None, "Omo"), (None, "Rexona")]),
    ("jnj", "Johnson & Johnson", [("bandaid", "Band-Aid"), ("listerine", "Listerine"), (None, "Neutrogena")]),
    ("cocacola", "Coca-Cola", [("sprite", "Sprite"), ("powerade", "Powerade"), (None, "Fanta"), (None, "Del Valle")]),
    ("pepsico", "PepsiCo", [("lays", "Lay's"), ("gatorade", "Gatorade"), (None, "Doritos"), (None, "Quaker")]),
    ("mars", "Mars", [("mms", "M&M's"), (None, "Snickers"), (None, "Twix"), (None, "Pedigree")]),
    ("kelloggs", "Kellogg's", [(None, "Corn Flakes"), (None, "Pringles"), (None, "Pop-Tarts")]),
    ("generalmills", "General Mills", [("cheerios", "Cheerios"), (None, "Nature Valley"), (None, "Betty Crocker")]),
    ("kraftheinz", "Kraft Heinz", [(None, "Heinz"), (None, "Oscar Mayer"), (None, "Philadelphia"), (None, "Kool-Aid")]),
]


def data_uri(slug):
    with open(os.path.join(HERE, "logos", slug + ".png"), "rb") as f:
        return "data:image/png;base64," + base64.b64encode(f.read()).decode()


def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;")


def brand_map():
    """Um cartão por empresa: a marca guarda-chuva grande no centro, as marcas ao redor, ligadas por linhas."""
    cx, cy, rx, ry, sw, sh = 180, 132, 132, 92, 84, 36
    cards = []
    for slug, name, sats in MARCAS:
        n = len(sats)
        pts = []
        for i in range(n):
            a = math.radians(-90 + 360 * i / n)
            pts.append((cx + rx * math.cos(a), cy + ry * math.sin(a)))
        lines = "".join(f'<line class="bl" x1="{cx}" y1="{cy}" x2="{x:.1f}" y2="{y:.1f}"/>' for x, y in pts)
        sat_svg = ""
        for (sslug, sname), (x, y) in zip(sats, pts):
            if sslug:
                sat_svg += (f'<rect class="tile" x="{x - sw / 2:.1f}" y="{y - sh / 2:.1f}" width="{sw}" height="{sh}" rx="8"/>'
                            f'<image href="{data_uri(sslug)}" x="{x - sw / 2 + 8:.1f}" y="{y - sh / 2 + 4:.1f}" width="{sw - 16}" height="{sh - 8}" preserveAspectRatio="xMidYMid meet"/>')
            else:
                sat_svg += (f'<rect class="pill" x="{x - sw / 2:.1f}" y="{y - sh / 2:.1f}" width="{sw}" height="{sh}" rx="18"/>'
                            f'<text class="pt" x="{x:.1f}" y="{y + 4:.1f}" text-anchor="middle">{esc(sname)}</text>')
        root = (f'<rect class="root" x="{cx - 75}" y="{cy - 40}" width="150" height="80" rx="12"/>'
                f'<image href="{data_uri(slug)}" x="{cx - 64}" y="{cy - 34}" width="128" height="50" preserveAspectRatio="xMidYMid meet"/>'
                f'<text class="rl" x="{cx}" y="{cy + 31}" text-anchor="middle">MARCA GUARDA-CHUVA</text>')
        label = f'{name} controla ' + ", ".join(s[1] for s in sats)
        cards.append(f'<figure class="bm"><svg viewBox="0 0 360 256" role="img" aria-label="{esc(label)}">{lines}{sat_svg}{root}</svg></figure>')
    return '<div class="bmap">' + "".join(cards) + "</div>"


def page_body(content):
    hero = f"""<section class="hero">
      <span class="eyebrow">Guia didático · atualizado em {DATE}</span>
      <h1>{TITLE}</h1>
      <div class="people"><span class="at">@Magnum Queiroz Dos Santos</span></div>
      <p class="lead">Da mercadoria à crise do capitalismo e à sua superação, em uma sequência em que cada conceito explica o seguinte.</p>
      <div class="facts"><span class="fact"><b>11</b> conceitos</span><span class="fact"><b>4</b> partes</span><span class="fact"><b>8</b> simuladores</span></div>
      <div class="legend"><span><i class="k-uso"></i>azul: valor de uso, trabalho necessário</span><span><i class="k-troca"></i>laranja: valor de troca, capital, excedente</span></div>
    </section>"""
    return f"""<header class="topbar">
  <span class="crumb"><b>Marxismo</b> · guia didático</span>
  <button class="theme-btn" id="theme-btn" type="button" aria-label="Alternar tema"><span id="theme-ico">{MOON}</span><span id="theme-txt">Modo escuro</span></button>
</header>
<div class="shell">
  <nav class="toc" aria-label="Sumário">
    <details open id="toc-details"><summary>Sumário</summary>
      <ol>{toc(content)}</ol>
    </details>
  </nav>
  <main>
    {hero}
    {content}
  </main>
</div>
<script>
{read("script.js")}
</script>"""


def main():
    content = embed_logos(read("body.html").strip().replace("{{brandmap}}", brand_map()))
    css = read("style.css")
    body = page_body(content)

    local = f"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{TITLE}</title>
{FONTS}
<style>
{css}
</style>
</head>
<body>
{body}
</body>
</html>
"""
    with open(os.path.join(HERE, "index.html"), "w", encoding="utf-8") as f:
        f.write(local)

    print("ok: index.html", len(local), "bytes")

if __name__ == "__main__":
    main()
