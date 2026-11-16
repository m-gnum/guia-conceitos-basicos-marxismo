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
    ("nestle", "Nestlé", [("nescafe", "Nescafé"), ("kitkat", "KitKat"), ("purina", "Purina"), (None, "Nespresso"), (None, "Nescau")],
     "Em venda, ainda pendente: 50% do negócio de águas (com a Platinum Equity) e a divisão de vitaminas (Nature's Bounty). Nos EUA, o KitKat é da Hershey."),
    ("pg", "Procter & Gamble", [("gillette", "Gillette"), ("oralb", "Oral-B"), ("pantene", "Pantene"), (None, "Pampers"), (None, "Ariel")],
     "Sem mudança nas marcas mostradas. A empresa corta até 7 mil vagas em uma reestruturação e não disse quais marcas ou países sairão."),
    ("unilever", "Unilever", [("dove", "Dove"), ("knorr", "Knorr", True), (None, "Hellmann's", True), (None, "Omo"), (None, "Rexona")],
     "O sorvete (Kibon, Magnum) saiu em dez/2025. Knorr e Hellmann's devem passar à McCormick, em acordo anunciado em mar/2026 e previsto para até meados de 2027."),
    (None, "Kimberly-Clark", [("bandaid", "Band-Aid"), ("listerine", "Listerine"), (None, "Neutrogena"), (None, "Huggies"), (None, "Kleenex")],
     "Este cartão substitui a Johnson & Johnson: ela separou os produtos de consumo na Kenvue (2023), que tinha Band-Aid, Listerine e Neutrogena. Em 2/11/2026 a Kimberly-Clark concluiu a compra da Kenvue."),
    ("cocacola", "Coca-Cola", [("sprite", "Sprite"), ("powerade", "Powerade"), (None, "Fanta"), (None, "Del Valle"), (None, "fairlife")],
     "Sem mudança nas quatro marcas originais. A fairlife foi comprada por completo em 2020. A venda do controle da engarrafadora africana (CCBA) está pendente."),
    ("pepsico", "PepsiCo", [("lays", "Lay's"), ("gatorade", "Gatorade"), (None, "Doritos"), (None, "Quaker"), (None, "poppi")],
     "A Tropicana foi vendida em 2022 (a PepsiCo ficou com 39%). A Siete (jan/2025) e a poppi (mai/2025) foram compradas. A Rockstar nos EUA e Canadá foi para a Celsius em 2025."),
    ("mars", "Mars", [("mms", "M&M's"), (None, "Snickers"), (None, "Twix"), (None, "Pedigree"), (None, "Pringles")],
     "Em dez/2025 a Mars concluiu a compra da Kellanova (ex-Kellogg's), o que trouxe Pringles, Cheez-It e Pop-Tarts."),
    (None, "Ferrero", [(None, "Nutella"), (None, "Kinder"), (None, "Ferrero Rocher"), (None, "Frosted Flakes"), (None, "Froot Loops")],
     "Este cartão substitui a Kellogg's, que deixou de existir como empresa: os salgadinhos foram para a Mars (Kellanova) e os cereais de EUA, Canadá e Caribe para a Ferrero (WK Kellogg, set/2025). Nos demais países, os cereais Kellogg's ficaram com a Mars."),
    ("generalmills", "General Mills", [("cheerios", "Cheerios"), (None, "Nature Valley"), (None, "Betty Crocker"), (None, "Blue Buffalo"), (None, "Häagen-Dazs")],
     "Vendeu o iogurte nos EUA e no Canadá e, em set/2026, o negócio brasileiro (Yoki e Kitano) à 3corações. Fora da América do Norte, o Cheerios costuma ser vendido pela Cereal Partners Worldwide, sociedade com a Nestlé."),
    ("kraftheinz", "Kraft Heinz", [(None, "Heinz"), (None, "Philadelphia"), (None, "Oscar Mayer"), (None, "Capri Sun"), (None, "Kool-Aid")],
     "A divisão em duas empresas, anunciada em set/2025, foi pausada em fev/2026. Em nov/2026 acertou a venda do café norte-americano (Maxwell House) à One Rock, prevista para meados de 2027."),
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
    for slug, name, sats, cap in MARCAS:
        n = len(sats)
        pts = []
        for i in range(n):
            a = math.radians(-90 + 360 * i / n)
            pts.append((cx + rx * math.cos(a), cy + ry * math.sin(a)))
        lines = "".join(f'<line class="bl" x1="{cx}" y1="{cy}" x2="{x:.1f}" y2="{y:.1f}"/>' for x, y in pts)
        sat_svg = ""
        for sat, (x, y) in zip(sats, pts):
            sslug, sname = sat[0], sat[1]
            pend = " pend" if len(sat) > 2 else ""
            if sslug:
                sat_svg += (f'<rect class="tile{pend}" x="{x - sw / 2:.1f}" y="{y - sh / 2:.1f}" width="{sw}" height="{sh}" rx="8"/>'
                            f'<image href="{data_uri(sslug)}" x="{x - sw / 2 + 8:.1f}" y="{y - sh / 2 + 4:.1f}" width="{sw - 16}" height="{sh - 8}" preserveAspectRatio="xMidYMid meet"/>')
            else:
                fs = ' style="font-size:10.5px"' if len(sname) > 11 else ""
                sat_svg += (f'<rect class="pill{pend}" x="{x - sw / 2:.1f}" y="{y - sh / 2:.1f}" width="{sw}" height="{sh}" rx="18"/>'
                            f'<text class="pt"{fs} x="{x:.1f}" y="{y + 4:.1f}" text-anchor="middle">{esc(sname)}</text>')
        root = f'<rect class="root" x="{cx - 75}" y="{cy - 40}" width="150" height="80" rx="12"/>'
        if slug:
            root += f'<image href="{data_uri(slug)}" x="{cx - 64}" y="{cy - 34}" width="128" height="50" preserveAspectRatio="xMidYMid meet"/>'
        else:
            root += f'<text class="rn" x="{cx}" y="{cy - 2}" text-anchor="middle">{esc(name)}</text>'
        root += f'<text class="rl" x="{cx}" y="{cy + 31}" text-anchor="middle">MARCA GUARDA-CHUVA</text>'
        label = f'{name} controla ' + ", ".join(s[1] for s in sats)
        cards.append(f'<figure class="bm"><svg viewBox="0 0 360 256" role="img" aria-label="{esc(label)}">{lines}{sat_svg}{root}</svg>'
                     f'<figcaption>{esc(cap)}</figcaption></figure>')
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
