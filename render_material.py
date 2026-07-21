#!/usr/bin/env python3
# ==========================================================================
# render_material.py  —  markdown -> pagina de material com a cara do site
# --------------------------------------------------------------------------
# Para cada guia em content/guias.yaml que tenha o campo `fonte` (um .md em
# materials/), gera o HTML apontado por `link`. Guias sem `fonte` (ex.: o
# guia rico feito a mao) sao deixados como estao.
#
# Rodar:  python render_material.py   (precisa de pyyaml e markdown)
# ==========================================================================
from __future__ import annotations

import html
import re
from pathlib import Path

import markdown
import yaml

ROOT = Path(__file__).resolve().parent
MATERIALS = ROOT / "materials"


def strip_first_h1(md: str) -> str:
    """Remove o primeiro '# Titulo' (o titulo ja aparece no cabecalho da pagina)."""
    lines = md.splitlines()
    for i, ln in enumerate(lines):
        if ln.strip().startswith("# "):
            del lines[i]
            # remove uma linha em branco imediatamente seguinte
            if i < len(lines) and not lines[i].strip():
                del lines[i]
            break
    return "\n".join(lines)


def render_one(md_path: Path, out_path: Path, numero: str, titulo: str) -> None:
    md_text = strip_first_h1(md_path.read_text(encoding="utf-8"))
    body = markdown.markdown(
        md_text, extensions=["extra", "sane_lists", "toc"], output_format="html5"
    )
    page = TEMPLATE.format(
        title=html.escape(titulo),
        numero=html.escape(numero),
        body=body,
        css=CSS,
    )
    out_path.write_text(page, encoding="utf-8")
    print(f"  render: {out_path.name}  (Guia {numero})")


def main() -> None:
    guias = (yaml.safe_load((ROOT / "content" / "guias.yaml").read_text("utf-8")) or {}).get("guias") or []
    n = 0
    for g in guias:
        fonte = g.get("fonte")
        if not fonte:
            continue
        render_one(MATERIALS / fonte, ROOT / g["link"], str(g.get("numero", "")), g.get("titulo", ""))
        n += 1
    print(f"{n} material(is) renderizado(s).")


CSS = """
:root{--paper:#f5f7f3;--surface:#fff;--surface-2:#eef2ec;--ink:#1a231e;--muted:#586a60;
--faint:#7d8c82;--line:#d8e0d6;--pine:#1f6f5c;--pine-strong:#164b3f;--pine-soft:#e4efe9;
--ochre:#9a6614;--ochre-bg:#f6ecd8;--code-bg:#f0f3ee;
--title-face:"Iowan Old Style","Palatino Linotype",Palatino,"Book Antiqua",Georgia,serif;
--body-face:system-ui,-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
--mono-face:ui-monospace,"SF Mono","JetBrains Mono",Menlo,Consolas,monospace;
--shadow:0 1px 2px rgba(20,40,30,.05),0 6px 22px -12px rgba(20,50,38,.18);}
@media (prefers-color-scheme:dark){:root{--paper:#0f1512;--surface:#161d19;--surface-2:#1a231e;
--ink:#e7ece7;--muted:#9ca99f;--faint:#7d8c82;--line:#2a352f;--pine:#5cc2a4;--pine-strong:#8bd6c1;
--pine-soft:#16241f;--ochre:#d9a94a;--ochre-bg:#211a0f;--code-bg:#121915;
--shadow:0 1px 2px rgba(0,0,0,.3),0 10px 30px -16px rgba(0,0,0,.6);}}
:root[data-theme="light"]{--paper:#f5f7f3;--surface:#fff;--surface-2:#eef2ec;--ink:#1a231e;--muted:#586a60;--faint:#7d8c82;--line:#d8e0d6;--pine:#1f6f5c;--pine-strong:#164b3f;--pine-soft:#e4efe9;--ochre:#9a6614;--ochre-bg:#f6ecd8;--code-bg:#f0f3ee;}
:root[data-theme="dark"]{--paper:#0f1512;--surface:#161d19;--surface-2:#1a231e;--ink:#e7ece7;--muted:#9ca99f;--faint:#7d8c82;--line:#2a352f;--pine:#5cc2a4;--pine-strong:#8bd6c1;--pine-soft:#16241f;--ochre:#d9a94a;--ochre-bg:#211a0f;--code-bg:#121915;}
*{box-sizing:border-box;}
html{scroll-behavior:smooth;}@media (prefers-reduced-motion:reduce){html{scroll-behavior:auto;}}
body{margin:0;background:var(--paper);color:var(--ink);font-family:var(--body-face);
font-size:1.0625rem;line-height:1.68;-webkit-font-smoothing:antialiased;}
a{color:var(--pine);text-underline-offset:2px;}a:hover{color:var(--pine-strong);}
:focus-visible{outline:2px solid var(--pine);outline-offset:2px;border-radius:3px;}
.masthead{border-bottom:1px solid var(--line);background:
radial-gradient(120% 100% at 88% -10%,var(--pine-soft),transparent 60%),var(--surface);}
.masthead-in{max-width:46rem;margin:0 auto;padding:2.6rem 1.6rem 1.4rem;}
.eyebrow{font-family:var(--mono-face);font-size:.8rem;letter-spacing:.12em;text-transform:uppercase;
color:var(--pine);font-weight:600;margin:0 0 .8rem;}
.eyebrow a{color:inherit;text-decoration:none;}
h1.title{font-family:var(--title-face);font-weight:600;font-size:2.2rem;line-height:1.08;
letter-spacing:-.01em;margin:0;text-wrap:balance;}
article{max-width:46rem;margin:0 auto;padding:2rem 1.6rem 5rem;}
article h1{font-family:var(--title-face);font-weight:600;font-size:1.85rem;margin:2.4rem 0 .8rem;letter-spacing:-.01em;}
article h2{font-family:var(--title-face);font-weight:600;font-size:1.5rem;margin:2.2rem 0 .7rem;
letter-spacing:-.005em;padding-bottom:.3rem;border-bottom:1px solid var(--line);}
article h3{font-family:var(--title-face);font-weight:600;font-size:1.22rem;margin:1.7rem 0 .5rem;}
article h4{font-family:var(--body-face);font-weight:650;font-size:1rem;margin:1.3rem 0 .4rem;
text-transform:uppercase;letter-spacing:.04em;color:var(--muted);}
article p{margin:.85rem 0;}
article strong{font-weight:650;}
article a{font-weight:500;}
article ul,article ol{margin:.7rem 0;padding-left:1.3rem;}
article li{margin:.4rem 0;}
article li>ul,article li>ol{margin:.3rem 0;}
article hr{border:none;border-top:1px solid var(--line);margin:2rem 0;}
article img{max-width:100%;height:auto;}
:not(pre)>code{background:var(--code-bg);border:1px solid var(--line);border-radius:5px;
padding:.06em .38em;font-size:.86em;font-family:var(--mono-face);}
pre{background:var(--code-bg);border:1px solid var(--line);border-radius:12px;padding:1rem 1.1rem;
overflow-x:auto;font-family:var(--mono-face);font-size:.85rem;line-height:1.6;margin:1.1rem 0;}
pre code{white-space:pre;background:none;border:none;padding:0;font-size:1em;}
blockquote{margin:1.3rem 0;padding:.8rem 1.15rem;border:1px solid var(--line);border-left:3px solid var(--pine);
background:var(--surface);border-radius:0 12px 12px 0;color:var(--ink);box-shadow:var(--shadow);}
blockquote p{margin:.3rem 0;}
.tw,.table-wrap{overflow-x:auto;}
table{border-collapse:collapse;width:100%;font-size:.92rem;margin:1.2rem 0;display:block;overflow-x:auto;}
th,td{text-align:left;padding:.55rem .8rem;border-bottom:1px solid var(--line);vertical-align:top;}
thead th{background:var(--surface-2);font-weight:650;font-size:.82rem;}
tbody tr:hover{background:var(--surface-2);}
footer{border-top:1px solid var(--line);background:var(--surface);}
.foot-in{max-width:46rem;margin:0 auto;padding:1.6rem 1.6rem 2.4rem;color:var(--muted);font-size:.88rem;
display:flex;flex-wrap:wrap;gap:.4rem 1.2rem;justify-content:space-between;}
"""

TEMPLATE = """<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Guia {numero} — {title} · BIIA</title>
<meta name="color-scheme" content="light dark">
<style>{css}</style>
</head>
<body>
<header class="masthead">
  <div class="masthead-in">
    <p class="eyebrow"><a href="index.html">&#8592; Materiais BIIA</a> &nbsp;·&nbsp; Guia de estudo {numero}</p>
    <h1 class="title">{title}</h1>
  </div>
</header>
<article>{body}</article>
<footer><div class="foot-in"><span>BIIA · Laboratório de Bioinformática e Inteligência Agrícola</span><span>IFSP · Campus Miracatu</span></div></footer>
</body>
</html>
"""


if __name__ == "__main__":
    main()
