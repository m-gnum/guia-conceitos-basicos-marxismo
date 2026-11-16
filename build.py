"""Gera index.html a partir de body.html + style.css + script.js.

Uso:
    python3 build.py
"""
import os
import re

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
    for m in re.finditer(r'<(p class="part-label"|h2) id="([^"]+)"[^>]*>(.*?)</(?:p|h2)>', content, re.S):
        cls = "l1" if m.group(1).startswith("p") else "l2"
        text = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", m.group(3))).strip()
        items.append(f'<li><a class="{cls}" href="#{m.group(2)}">{text}</a></li>')
    return "".join(items)


def page_body(content):
    hero = f"""<section class="hero">
      <span class="eyebrow">Guia didático · atualizado em {DATE}</span>
      <h1>{TITLE}</h1>
      <div class="people"><span class="at">@Magnum Queiroz Dos Santos</span></div>
      <p class="lead">Da mercadoria à crise do capitalismo e à sua superação, em uma sequência em que cada conceito explica o seguinte.</p>
      <div class="facts"><span class="fact"><b>11</b> conceitos</span><span class="fact"><b>4</b> partes</span><span class="fact"><b>7</b> simuladores</span></div>
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
    content = read("body.html").strip()
    css = read("style.css")
    page = f"""<!doctype html>
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
{page_body(content)}
</body>
</html>
"""
    with open(os.path.join(HERE, "index.html"), "w", encoding="utf-8") as f:
        f.write(page)
    print("ok: index.html", len(page), "bytes")


if __name__ == "__main__":
    main()
