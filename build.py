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


# Empresas (guarda-chuva): (slug do logo ou None, nome, ramo, total segundo a empresa, marcas, legenda).
# Cada marca: (slug do logo ou None, nome[, "pend" = venda/fusão anunciada | "oth" = bloco de outras]).
MARCAS = [
    ("nestle", "Nestlé", "alimentos e café", "mais de 2.000 marcas",
     [("nescafe", "Nescafé"), (None, "Nespresso"), ("purina", "Purina"), (None, "Starbucks"), ("kitkat", "KitKat"), (None, "Maggi"),
      (None, "Nido (Ninho)"), (None, "Gerber"), (None, "S.Pellegrino", "pend"), (None, "Milo"), (None, "Outras (+1.990)", "oth")],
     "A Nestlé não publica ranking de vendas: as 10 marcas são uma seleção a partir do que ela cita como maior (Nescafé, Nespresso e Starbucks são as \"bilionárias\" que ela nomeia; a Starbucks é licenciada). Tracejado: a venda de 50% do negócio de águas está anunciada e pendente. O negócio de vitaminas também está à venda."),
    ("pg", "Procter & Gamble", "higiene, beleza e limpeza", "61 marcas na lista da empresa",
     [(None, "Pampers"), (None, "Tide"), ("gillette", "Gillette"), ("oralb", "Oral-B"), (None, "Always"), ("pantene", "Pantene"),
      (None, "Ariel"), (None, "Charmin"), (None, "Head & Shoulders"), (None, "Olay"), (None, "Outras (51)", "oth")],
     "A P&G não publica vendas por marca: a ordem é uma estimativa a partir das categorias em que ela se declara líder. A lista de 61 marcas é a do site dos EUA e é incompleta (omite a Fairy, por exemplo). Em ago/2026 a empresa acertou a compra da Thorne e segue em uma reestruturação que não nomeou marcas."),
    ("cocacola", "Coca-Cola", "bebidas", "cerca de 200 marcas",
     [(None, "Coca-Cola"), (None, "Diet Coke"), (None, "Fanta"), ("sprite", "Sprite"), (None, "Coca-Cola Zero Sugar"), ("powerade", "Powerade"),
      (None, "Minute Maid"), (None, "Dasani"), (None, "fairlife"), (None, "Del Valle"), (None, "Outras (~190)", "oth")],
     "A empresa não publica ranking: as quatro primeiras seguem o valor de marca divulgado pela imprensa e as demais são uma seleção entre as 32 marcas \"bilionárias\" que ela diz ter. Variantes (Zero, Diet) entram na marca principal. A venda do controle da engarrafadora africana está pendente, mas ela não é uma marca."),
    ("mars", "Mars", "doces e ração para pets", "104 marcas no site da empresa",
     [("mms", "M&M's"), (None, "Snickers"), (None, "Royal Canin"), (None, "Pedigree"), (None, "Pringles"), (None, "Twix"),
      (None, "Skittles"), (None, "Whiskas"), (None, "Cheez-It"), (None, "Sheba"), (None, "Outras (94)", "oth")],
     "A Mars é privada e não publica vendas por marca: as 10 são uma seleção, por reconhecimento, entre as \"bilionárias\" do site. A lista de 104 inclui clínicas veterinárias e ainda não mostra toda a carteira da Kellanova, comprada em dez/2025 (Pringles, Cheez-It, Pop-Tarts)."),
    (None, "Kimberly-Clark", "papel, fraldas e saúde", "30 marcas na página da empresa",
     [(None, "Huggies"), ("listerine", "Listerine"), (None, "Cottonelle"), (None, "Neutrogena"), (None, "Depend"), (None, "Tylenol"),
      (None, "Kleenex"), (None, "Johnson's Baby"), (None, "Kotex"), (None, "Scott"), (None, "Outras (20)", "oth")],
     "As 10 são as marcas \"bilionárias\" que a empresa declarou em 2/11/2026, na ordem em que ela as escreveu (não é ranking de vendas). Este cartão substitui a Johnson & Johnson: ela separou o consumo na Kenvue (2023), que a Kimberly-Clark comprou em 2/11/2026. O total real é maior que 30: os documentos da empresa citam cerca de 44."),
]


def data_uri(slug):
    with open(os.path.join(HERE, "logos", slug + ".png"), "rb") as f:
        return "data:image/png;base64," + base64.b64encode(f.read()).decode()


def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;")


def brand_map():
    """Um cartão por empresa: a marca guarda-chuva grande no centro, as 10 maiores marcas ao redor e um bloco "Outras (N)"."""
    W, H, cx, cy, rx, ry, sw, sh = 720, 300, 360, 150, 290, 125, 104, 32
    cards = []
    for slug, name, ramo, total, sats, cap in MARCAS:
        n = len(sats)
        pts = []
        for i in range(n):
            a = math.radians(-90 + 360 * i / n)
            pts.append((cx + rx * math.cos(a), cy + ry * math.sin(a)))
        lines = "".join(f'<line class="bl" x1="{cx}" y1="{cy}" x2="{x:.1f}" y2="{y:.1f}"/>' for x, y in pts)
        sat_svg = ""
        chips = ""
        for sat, (x, y) in zip(sats, pts):
            sslug, sname = sat[0], sat[1]
            flag = sat[2] if len(sat) > 2 else ""
            cls = " pend" if flag == "pend" else (" oth" if flag == "oth" else "")
            if sslug:
                sat_svg += (f'<rect class="tile{cls}" x="{x - sw / 2:.1f}" y="{y - sh / 2:.1f}" width="{sw}" height="{sh}" rx="8"/>'
                            f'<image href="{data_uri(sslug)}" x="{x - sw / 2 + 8:.1f}" y="{y - sh / 2 + 4:.1f}" width="{sw - 16}" height="{sh - 8}" preserveAspectRatio="xMidYMid meet"/>')
            else:
                fs = ' style="font-size:%.1fpx"' % (11 if len(sname) <= 13 else 9.5 if len(sname) <= 17 else 8.5)
                sat_svg += (f'<rect class="pill{cls}" x="{x - sw / 2:.1f}" y="{y - sh / 2:.1f}" width="{sw}" height="{sh}" rx="16"/>'
                            f'<text class="pt"{fs} x="{x:.1f}" y="{y + 3.8:.1f}" text-anchor="middle">{esc(sname)}</text>')
            chips += f'<li class="{cls.strip()}">{esc(sname)}</li>'
        root = f'<rect class="root" x="{cx - 88}" y="{cy - 46}" width="176" height="92" rx="14"/>'
        if slug:
            root += f'<image href="{data_uri(slug)}" x="{cx - 74}" y="{cy - 40}" width="148" height="58" preserveAspectRatio="xMidYMid meet"/>'
        else:
            root += f'<text class="rn" x="{cx}" y="{cy - 2}" text-anchor="middle">{esc(name)}</text>'
        root += f'<text class="rl" x="{cx}" y="{cy + 34}" text-anchor="middle">{esc(ramo.upper())}</text>'
        label = f'{name} ({ramo}) controla ' + ", ".join(s[1] for s in sats)
        head = f'<div class="bmh"><b>{esc(name)}</b><span>{esc(ramo)} · {esc(total)}</span></div>'
        cards.append(f'<figure class="bm">{head}<svg viewBox="0 0 {W} {H}" role="img" aria-label="{esc(label)}">{lines}{sat_svg}{root}</svg>'
                     f'<ul class="bml">{chips}</ul><figcaption>{esc(cap)}</figcaption></figure>')
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
