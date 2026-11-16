# Guia de conceitos básicos do marxismo

Página didática e interativa, em português, que explica 11 conceitos do marxismo em uma sequência em que cada um prepara o seguinte: do valor de uso e do valor de troca até a crise do capitalismo e a sua superação. Inclui 8 simuladores (valor, mais-valia, acumulação, exército industrial de reserva, oligopólios, classes e taxa de lucro) e casos reais com fontes.

## Estrutura

| Arquivo | Conteúdo |
|---|---|
| `index.html` | Página final, autocontida (abre direto no navegador) |
| `body.html` | Texto, diagramas e simuladores |
| `style.css` | Estilos e temas claro e escuro |
| `script.js` | Simuladores e alternância de tema |
| `logos/` | Logos usados na seção de oligopólios (miniaturas do Wikimedia Commons; origem e licença em `logos/_origem.json`) |
| `build.py` | Junta os arquivos acima em `index.html` e embute os logos |

## Como regenerar

```bash
python3 build.py
```

## Observações

- Os números dos simuladores são ilustrativos.
- Os fatos citados (moradia, alimento, roupa, Uber e crises) têm fonte ao final da página. Os números de São Paulo vêm de reportagens e não foram conferidos nas tabelas oficiais.
- A página carrega as fontes Inter e Newsreader do Google Fonts.
- As marcas e logos pertencem aos seus titulares e aparecem apenas para ilustrar o argumento.
