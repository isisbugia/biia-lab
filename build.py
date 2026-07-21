#!/usr/bin/env python3
# ==========================================================================
# build.py  —  gerador do site biia-lab
# --------------------------------------------------------------------------
# Le os arquivos de content/*.yaml e monta o index.html (pagina unica com
# abas). Voce edita o CONTEUDO em content/; este script cuida da APARENCIA.
#
# Rodar:  python build.py     (precisa de pyyaml)
#         mamba run -n biia-csordidus python build.py
# ==========================================================================
from __future__ import annotations

import html
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent
CONTENT = ROOT / "content"

# Abas do site: (id, rótulo). A ordem é a ordem de exibição.
TABS = [
    ("guias", "Guias de estudo"),
    ("ferramentas", "Ferramentas de Bioinfo"),
    ("videoaulas", "Vídeoaulas e Tutoriais"),
    ("recursos", "Recursos educativos"),
    ("avisos", "Quadro de avisos"),
    ("eventos", "Eventos importantes"),
]


def load(name: str) -> dict:
    p = CONTENT / f"{name}.yaml"
    return yaml.safe_load(p.read_text(encoding="utf-8")) or {}


def esc(x) -> str:
    return html.escape(str(x).strip()) if x is not None else ""


def _link_attrs(link: str) -> str:
    if link and (link.startswith("http://") or link.startswith("https://")):
        return f' href="{esc(link)}" target="_blank" rel="noopener"'
    return f' href="{esc(link)}"' if link else ""


def empty(msg: str) -> str:
    return f'<p class="empty">{esc(msg)}</p>'


def panel_guias(data) -> str:
    itens = (data or {}).get("guias") or []
    if not itens:
        return empty("Nenhum guia publicado ainda.")
    cards = []
    for g in itens:
        link = g.get("link", "")
        cards.append(
            f'<a class="card guia"{_link_attrs(link)}>'
            f'<span class="gnum">{esc(g.get("numero"))}</span>'
            f'<div class="gbody"><span class="kind">Guia de estudo</span>'
            f'<h3>{esc(g.get("titulo"))}</h3>'
            f'<p>{esc(g.get("descricao"))}</p>'
            f'<span class="go">Estudar</span></div></a>'
        )
    return f'<div class="grid">{"".join(cards)}</div>'


def panel_cards(data, key, empty_msg) -> str:
    itens = (data or {}).get(key) or []
    if not itens:
        return empty(empty_msg)
    cards = []
    for it in itens:
        link = it.get("link", "")
        go = ('<span class="go">Abrir</span>' if link else "")
        tag = "a" if link else "div"
        cards.append(
            f'<{tag} class="card"{_link_attrs(link)}>'
            f'<h3>{esc(it.get("titulo"))}</h3>'
            f'<p>{esc(it.get("descricao"))}</p>{go}</{tag}>'
        )
    return f'<div class="grid">{"".join(cards)}</div>'


def panel_avisos(data) -> str:
    itens = (data or {}).get("avisos") or []
    if not itens:
        return empty("Sem avisos no momento.")
    rows = []
    for a in itens:
        rows.append(
            f'<article class="note"><span class="date">{esc(a.get("data"))}</span>'
            f'<div><h3>{esc(a.get("titulo"))}</h3>'
            f'<p>{esc(a.get("texto"))}</p></div></article>'
        )
    return f'<div class="stack">{"".join(rows)}</div>'


def panel_eventos(data) -> str:
    itens = (data or {}).get("eventos") or []
    if not itens:
        return empty("Nenhum evento agendado ainda.")
    rows = []
    for e in itens:
        link = e.get("link", "")
        more = (f'<a class="go"{_link_attrs(link)}>Mais</a>' if link else "")
        rows.append(
            f'<article class="note event"><span class="date">{esc(e.get("data"))}</span>'
            f'<div><h3>{esc(e.get("titulo"))}</h3>'
            f'<p>{esc(e.get("descricao"))}</p>{more}</div></article>'
        )
    return f'<div class="stack">{"".join(rows)}</div>'


def build() -> None:
    site = load("site")
    panels = {
        "guias": panel_guias(load("guias")),
        "ferramentas": panel_cards(load("ferramentas"), "itens",
                                   "Ferramentas serão listadas aqui em breve."),
        "videoaulas": panel_cards(load("videoaulas"), "itens",
                                  "Vídeoaulas e tutoriais em breve."),
        "recursos": panel_cards(load("recursos"), "itens",
                                "Recursos educativos em breve."),
        "avisos": panel_avisos(load("avisos")),
        "eventos": panel_eventos(load("eventos")),
    }

    nav = "".join(
        f'<a class="tab" href="#{tid}" data-tab="{tid}">{esc(label)}</a>'
        for tid, label in TABS
    )
    sections = "".join(
        f'<section class="panel" id="{tid}" data-panel="{tid}">'
        f'<h2 class="panel-title">{esc(label)}</h2>{panels[tid]}</section>'
        for tid, label in TABS
    )

    out = TEMPLATE.format(
        title=esc(site.get("titulo", "BIIA")),
        subtitle=esc(site.get("subtitulo", "")),
        descricao=esc(site.get("descricao", "")),
        nav=nav,
        sections=sections,
        foot_l=esc(site.get("rodape_esquerda", "")),
        foot_r=esc(site.get("rodape_direita", "")),
        css=CSS,
    )
    (ROOT / "index.html").write_text(out, encoding="utf-8")
    print("index.html gerado com", len(TABS), "abas.")


CSS = """
:root{--paper:#f5f7f3;--surface:#fff;--surface-2:#eef2ec;--ink:#1a231e;--muted:#586a60;
--faint:#7d8c82;--line:#d8e0d6;--pine:#1f6f5c;--pine-strong:#164b3f;--pine-soft:#e4efe9;--ochre:#9a6614;
--title-face:"Iowan Old Style","Palatino Linotype",Palatino,"Book Antiqua",Georgia,serif;
--body-face:system-ui,-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
--mono-face:ui-monospace,"SF Mono","JetBrains Mono",Menlo,Consolas,monospace;
--shadow:0 1px 2px rgba(20,40,30,.05),0 10px 30px -14px rgba(20,50,38,.22);}
@media (prefers-color-scheme:dark){:root{--paper:#0f1512;--surface:#161d19;--surface-2:#1a231e;
--ink:#e7ece7;--muted:#9ca99f;--faint:#7d8c82;--line:#2a352f;--pine:#5cc2a4;--pine-strong:#8bd6c1;
--pine-soft:#16241f;--ochre:#d9a94a;--shadow:0 1px 2px rgba(0,0,0,.3),0 14px 34px -18px rgba(0,0,0,.7);}}
:root[data-theme="light"]{--paper:#f5f7f3;--surface:#fff;--surface-2:#eef2ec;--ink:#1a231e;--muted:#586a60;--faint:#7d8c82;--line:#d8e0d6;--pine:#1f6f5c;--pine-strong:#164b3f;--pine-soft:#e4efe9;--ochre:#9a6614;}
:root[data-theme="dark"]{--paper:#0f1512;--surface:#161d19;--surface-2:#1a231e;--ink:#e7ece7;--muted:#9ca99f;--faint:#7d8c82;--line:#2a352f;--pine:#5cc2a4;--pine-strong:#8bd6c1;--pine-soft:#16241f;--ochre:#d9a94a;}
*{box-sizing:border-box;}
body{margin:0;background:var(--paper);color:var(--ink);font-family:var(--body-face);
font-size:1.0625rem;line-height:1.65;-webkit-font-smoothing:antialiased;}
a{color:var(--pine);text-underline-offset:2px;}a:hover{color:var(--pine-strong);}
:focus-visible{outline:2px solid var(--pine);outline-offset:3px;border-radius:4px;}
.wrap{max-width:62rem;margin:0 auto;padding:0 1.5rem;}
header.hero{border-bottom:1px solid var(--line);
background:radial-gradient(130% 120% at 85% -20%,var(--pine-soft),transparent 55%),var(--surface);}
.hero-in{max-width:62rem;margin:0 auto;padding:3.6rem 1.5rem 1.6rem;}
.brand{font-family:var(--mono-face);font-size:.82rem;letter-spacing:.2em;text-transform:uppercase;
color:var(--pine);font-weight:600;margin:0 0 1rem;}
h1{font-family:var(--title-face);font-weight:600;font-size:clamp(2.1rem,4.6vw,3.1rem);line-height:1.05;
letter-spacing:-.015em;margin:0 0 .6rem;text-wrap:balance;max-width:18ch;}
.tag{font-size:1.13rem;color:var(--muted);max-width:56ch;margin:0;}
.ribbon{font-family:var(--mono-face);font-size:.78rem;letter-spacing:.34em;color:var(--faint);
opacity:.5;white-space:nowrap;overflow:hidden;border-top:1px solid var(--line);
padding-top:.8rem;margin-top:1.5rem;user-select:none;}
nav.tabs{position:sticky;top:0;z-index:10;background:var(--paper);border-bottom:1px solid var(--line);}
.tabs-in{max-width:62rem;margin:0 auto;padding:0 1.1rem;display:flex;gap:.15rem;overflow-x:auto;
scrollbar-width:none;}
.tabs-in::-webkit-scrollbar{display:none;}
.tab{white-space:nowrap;text-decoration:none;color:var(--muted);font-size:.95rem;font-weight:550;
padding:.9rem .8rem;border-bottom:2px solid transparent;transition:color .15s,border-color .15s;}
.tab:hover{color:var(--ink);}
.tab.active{color:var(--pine-strong);border-bottom-color:var(--pine);font-weight:650;}
main{padding:2.4rem 0 1rem;min-height:44vh;}
.panel-title{font-family:var(--title-face);font-weight:600;font-size:1.7rem;letter-spacing:-.01em;
margin:0 0 1.3rem;}
.js .panel{display:none;}.js .panel.active{display:block;animation:fade .25s ease;}
@keyframes fade{from{opacity:0;transform:translateY(4px);}to{opacity:1;transform:none;}}
@media (prefers-reduced-motion:reduce){.js .panel.active{animation:none;}}
.panel:not(:last-child){margin-bottom:2.4rem;}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,20rem),1fr));gap:1.1rem;}
.card{display:flex;flex-direction:column;gap:.45rem;text-decoration:none;color:inherit;
background:var(--surface);border:1px solid var(--line);border-radius:14px;padding:1.25rem 1.3rem 1.35rem;
box-shadow:var(--shadow);transition:transform .16s,border-color .16s;}
a.card:hover{transform:translateY(-3px);border-color:var(--pine);}
@media (prefers-reduced-motion:reduce){a.card:hover{transform:none;}}
.card .kind{font-family:var(--mono-face);font-size:.7rem;letter-spacing:.1em;text-transform:uppercase;
color:var(--pine);font-weight:600;}
.card h3{font-family:var(--title-face);font-weight:600;font-size:1.25rem;margin:.05rem 0;line-height:1.2;}
.card p{margin:0;color:var(--muted);font-size:.95rem;}
.card .go{margin-top:.45rem;font-family:var(--mono-face);font-size:.8rem;color:var(--pine);font-weight:600;}
.card .go::after{content:" \\2192";}
.card.guia{flex-direction:row;gap:1.1rem;align-items:flex-start;}
.gnum{font-family:var(--mono-face);font-weight:600;font-size:2rem;line-height:1;color:var(--pine);
background:var(--pine-soft);border:1px solid var(--line);border-radius:12px;
padding:.6rem .7rem;min-width:3.3rem;text-align:center;}
.gbody{display:flex;flex-direction:column;gap:.35rem;}
.stack{display:flex;flex-direction:column;gap:.9rem;}
.note{display:flex;gap:1rem;background:var(--surface);border:1px solid var(--line);
border-left:3px solid var(--pine);border-radius:0 12px 12px 0;padding:1rem 1.2rem;box-shadow:var(--shadow);}
.note.event{border-left-color:var(--ochre);}
.note .date{font-family:var(--mono-face);font-size:.8rem;color:var(--faint);white-space:nowrap;
padding-top:.15rem;font-variant-numeric:tabular-nums;}
.note h3{font-family:var(--title-face);font-weight:600;font-size:1.18rem;margin:0 0 .2rem;}
.note p{margin:0;color:var(--muted);font-size:.96rem;}
.note .go{display:inline-block;margin-top:.4rem;font-family:var(--mono-face);font-size:.8rem;font-weight:600;}
.note .go::after{content:" \\2192";}
.empty{color:var(--faint);font-style:italic;border:1px dashed var(--line);border-radius:12px;
padding:1.6rem;text-align:center;background:var(--surface);}
footer{margin-top:3rem;border-top:1px solid var(--line);background:var(--surface);}
.foot-in{max-width:62rem;margin:0 auto;padding:1.6rem 1.5rem 2.4rem;color:var(--muted);font-size:.88rem;
display:flex;flex-wrap:wrap;gap:.4rem 1.4rem;justify-content:space-between;}
"""

TEMPLATE = """<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} — {subtitle}</title>
<meta name="description" content="{descricao}">
<meta name="color-scheme" content="light dark">
<style>{css}</style>
</head>
<body>
<header class="hero">
  <div class="hero-in">
    <p class="brand">{title}</p>
    <h1>{subtitle}</h1>
    <p class="tag">{descricao}</p>
    <div class="ribbon" aria-hidden="true">ATG·CATALASE···OBP···&#945;-AMILASE···MGNTVQYST·QHSTA·QHSTA·QHSTA·QHSTA·QHSTA·LHSRVEYST···PF00199···PF01395···PF00128</div>
  </div>
</header>
<nav class="tabs" aria-label="Seções"><div class="tabs-in">{nav}</div></nav>
<main class="wrap">{sections}</main>
<footer><div class="foot-in"><span>{foot_l}</span><span>{foot_r}</span></div></footer>
<script>
(function(){{
  var root=document.documentElement; root.classList.add('js');
  var tabs=[].slice.call(document.querySelectorAll('.tab'));
  var panels=[].slice.call(document.querySelectorAll('.panel'));
  var ids=panels.map(function(p){{return p.id;}});
  function show(id){{
    if(ids.indexOf(id)<0) id=ids[0];
    tabs.forEach(function(t){{t.classList.toggle('active',t.dataset.tab===id);}});
    panels.forEach(function(p){{p.classList.toggle('active',p.id===id);}});
  }}
  function fromHash(){{show((location.hash||'').replace('#',''));}}
  window.addEventListener('hashchange',fromHash);
  fromHash();
}})();
</script>
</body>
</html>
"""


if __name__ == "__main__":
    build()
