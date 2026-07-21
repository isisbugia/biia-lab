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
from urllib.parse import parse_qs, urlparse

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
    ("eventos", "Eventos"),
]


def load(name: str) -> dict:
    p = CONTENT / f"{name}.yaml"
    return yaml.safe_load(p.read_text(encoding="utf-8")) or {}


def esc(x) -> str:
    return html.escape(str(x).strip()) if x is not None else ""


def fmt_date(iso) -> str:
    """AAAA-MM-DD -> DD/MM/AAAA (para exibir na lista)."""
    p = str(iso or "").strip().split("-")
    return f"{p[2]}/{p[1]}/{p[0]}" if len(p) == 3 else esc(iso)


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


def panel_recursos(data) -> str:
    itens = (data or {}).get("recursos") or []
    if not itens:
        return empty("Recursos educativos em breve.")
    groups, order = {}, []
    for it in itens:
        cat = it.get("categoria", "Outros")
        if cat not in groups:
            groups[cat] = []; order.append(cat)
        groups[cat].append(it)
    out = []
    for cat in order:
        cards = []
        for it in groups[cat]:
            link = it.get("link", "")
            fonte = esc(it.get("fonte"))
            fonte_html = f'<span class="kind">{fonte}</span>' if fonte else ""
            go = '<span class="go">Abrir</span>' if link else ""
            tag = "a" if link else "div"
            cards.append(
                f'<{tag} class="card"{_link_attrs(link)}>{fonte_html}'
                f'<h3>{esc(it.get("nome"))}</h3>'
                f'<p>{esc(it.get("descricao"))}</p>{go}</{tag}>'
            )
        out.append(f'<h3 class="fgroup">{esc(cat)}</h3>'
                   f'<div class="grid">{"".join(cards)}</div>')
    return "".join(out)


def panel_ferramentas(data) -> str:
    itens = (data or {}).get("ferramentas") or []
    if not itens:
        return empty("Ferramentas serão listadas aqui em breve.")
    groups, order = {}, []
    for it in itens:
        cat = it.get("categoria", "Outras")
        if cat not in groups:
            groups[cat] = []; order.append(cat)
        groups[cat].append(it)
    out = []
    for cat in order:
        rows = []
        for it in groups[cat]:
            nome = esc(it.get("nome"))
            link = it.get("link", "")
            nome_html = f'<a{_link_attrs(link)}>{nome}</a>' if link else nome
            ex = esc(it.get("exemplo"))
            ex_html = f'<br><span class="ex">Ex.: {ex}</span>' if ex else ""
            rows.append(
                f'<tr><td class="fw"><strong>{nome_html}</strong></td>'
                f'<td><span class="badge">{esc(it.get("tipo"))}</span></td>'
                f'<td>{esc(it.get("descricao"))}{ex_html}</td></tr>'
            )
        out.append(
            f'<h3 class="fgroup">{esc(cat)}</h3>'
            '<div class="tablewrap"><table><thead><tr>'
            '<th>Ferramenta</th><th>Tipo</th><th>Descrição e utilizações</th>'
            f'</tr></thead><tbody>{"".join(rows)}</tbody></table></div>'
        )
    return "".join(out)


def yt_embed(url: str):
    """URL do YouTube (vídeo ou playlist) -> URL de embed, ou None."""
    try:
        u = urlparse(str(url)); q = parse_qs(u.query)
    except Exception:
        return None
    vid = (q.get("v") or [None])[0]
    plist = (q.get("list") or [None])[0]
    if u.netloc.endswith("youtu.be") and u.path.strip("/"):
        vid = u.path.strip("/")
    if "/embed/" in u.path:
        return url
    if plist and vid:
        return f"https://www.youtube.com/embed/{vid}?list={plist}"
    if plist:
        return f"https://www.youtube.com/embed/videoseries?list={plist}"
    if vid:
        return f"https://www.youtube.com/embed/{vid}"
    return None


_YT_ALLOW = ("accelerometer; autoplay; clipboard-write; encrypted-media; "
             "gyroscope; picture-in-picture; web-share")


def panel_videoaulas(data) -> str:
    itens = (data or {}).get("itens") or []
    if not itens:
        return empty("Vídeoaulas e tutoriais em breve.")
    out = []
    for it in itens:
        title, desc = esc(it.get("titulo")), esc(it.get("descricao"))
        emb = yt_embed(it.get("youtube")) if it.get("youtube") else None
        if emb:
            link = it.get("youtube") or it.get("link", "")
            out.append(
                '<div class="media">'
                f'<div class="embed"><iframe src="{esc(emb)}" title="{title}" loading="lazy" '
                f'allow="{_YT_ALLOW}" allowfullscreen '
                'referrerpolicy="strict-origin-when-cross-origin"></iframe></div>'
                f'<div class="media-cap"><h3>{title}</h3><p>{desc}</p>'
                + (f'<a class="go"{_link_attrs(link)}>Abrir no YouTube</a>' if link else "")
                + "</div></div>"
            )
        else:
            link = it.get("link", "")
            go = '<span class="go">Abrir</span>' if link else ""
            tag = "a" if link else "div"
            out.append(f'<{tag} class="card"{_link_attrs(link)}><h3>{title}</h3>'
                       f'<p>{desc}</p>{go}</{tag}>')
    return f'<div class="media-grid">{"".join(out)}</div>'


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
    for i, e in enumerate(itens):
        link = e.get("link", "")
        more = (f'<a class="go"{_link_attrs(link)}>Mais</a>' if link else "")
        iso = esc(e.get("data"))
        fim = e.get("data_fim")
        fim_attr = f' data-date-fim="{esc(fim)}"' if fim else ""
        disp = fmt_date(e.get("data")) + (f" a {fmt_date(fim)}" if fim else "")
        tag = esc(e.get("tag"))
        tag_html = f'<br><span class="badge">{tag}</span>' if tag else ""
        rows.append(
            f'<article class="note event" data-date="{iso}"{fim_attr} id="ev-{i}">'
            f'<span class="date">{esc(disp)}{tag_html}</span>'
            f'<div><h3>{esc(e.get("titulo"))}</h3>'
            f'<p>{esc(e.get("descricao"))}</p>{more}</div></article>'
        )
    return ('<div class="cal-wrap">'
            '<div class="cal" id="cal" aria-label="Calendário de eventos"></div>'
            f'<div class="stack cal-list" id="cal-list">{"".join(rows)}</div>'
            '</div>')


_MEMBER_ORDER = ["Coordenação", "Estágio de IC", "Colaboração"]


def _member_card(m) -> str:
    nome = esc(m.get("nome"))
    foto = m.get("foto")
    if foto:
        av = f'<div class="avatar"><img src="{esc(foto)}" alt="{nome}" loading="lazy"></div>'
    else:
        parts = str(m.get("nome", "")).split()
        initials = "".join(w[0] for w in parts[:2]).upper() or "•"
        av = f'<div class="avatar mono">{esc(initials)}</div>'
    links = []
    for lab, key in (("Lattes", "lattes"), ("ORCID", "orcid"),
                     ("GitHub", "github"), ("LinkedIn", "linkedin")):
        u = m.get(key)
        if u:
            links.append(f'<a class="badge" href="{esc(u)}" target="_blank" rel="noopener">{lab}</a>')
    links_html = f'<div class="mlinks">{"".join(links)}</div>' if links else ""
    func = esc(m.get("funcao"))
    area = esc(m.get("area"))
    return (
        f'<div class="card member">{av}<div class="minfo">'
        f'<h3>{nome}</h3>'
        + (f'<span class="mfunc">{func}</span>' if func else "")
        + (f'<p>{area}</p>' if area else "")
        + links_html + "</div></div>"
    )


def build_integrantes(site) -> None:
    itens = (load("integrantes") or {}).get("integrantes") or []
    if itens:
        groups, order = {}, []
        for m in itens:
            p = m.get("papel", "Integrantes")
            if p not in groups:
                groups[p] = []; order.append(p)
        ordered = [p for p in _MEMBER_ORDER if p in groups] + \
                  [p for p in order if p not in _MEMBER_ORDER]
        body = "".join(
            f'<h3 class="fgroup">{esc(p)}</h3>'
            f'<div class="grid">{"".join(_member_card(m) for m in groups[p])}</div>'
            for p in ordered
        )
    else:
        body = empty("A equipe do BIIA será apresentada aqui em breve.")
    out = INTEGRANTES_TEMPLATE.format(
        css=CSS, body=body,
        foot_l=esc(site.get("rodape_esquerda", "")),
        foot_r=esc(site.get("rodape_direita", "")),
    )
    (ROOT / "integrantes.html").write_text(out, encoding="utf-8")
    print(f"integrantes.html gerado ({len(itens)} integrante(s)).")


def build() -> None:
    site = load("site")
    panels = {
        "guias": panel_guias(load("guias")),
        "ferramentas": panel_ferramentas(load("ferramentas")),
        "videoaulas": panel_videoaulas(load("videoaulas")),
        "recursos": panel_recursos(load("recursos")),
        "avisos": panel_avisos(load("avisos")),
        "eventos": panel_eventos(load("eventos")),
    }

    ws_url = site.get("espaco_trabalho_url", "")
    ws_button = (
        f'<a class="ws-btn" href="{esc(ws_url)}" target="_blank" rel="noopener">'
        f'<span aria-hidden="true">\U0001F4C1</span> '
        f'{esc(site.get("espaco_trabalho_label", "Espaço de trabalho"))}</a>'
    ) if ws_url else ""

    integrantes_label = site.get("integrantes_label", "")
    integrantes_button = (
        f'<a class="ws-btn" href="integrantes.html">'
        f'<span aria-hidden="true">\U0001F465</span> {esc(integrantes_label)}</a>'
    ) if integrantes_label else ""

    participe_url = site.get("participe_url", "")
    participe_email = site.get("participe_email", "")
    if participe_url:
        p_href, p_target = participe_url, ' target="_blank" rel="noopener"'
    elif participe_email:
        p_href = f"mailto:{participe_email}?subject=Quero%20integrar%20o%20BIIA"
        p_target = ""
    else:
        p_href, p_target = "", ""
    participe_button = (
        f'<a class="ws-btn" href="{esc(p_href)}"{p_target}>'
        f'<span aria-hidden="true">✉</span> '
        f'{esc(site.get("participe_label", "Quero participar"))}</a>'
    ) if p_href else ""

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
        caljs=CAL_JS,
        ws_button=ws_button,
        integrantes_button=integrantes_button,
        participe_button=participe_button,
    )
    (ROOT / "index.html").write_text(out, encoding="utf-8")
    print("index.html gerado com", len(TABS), "abas.")
    build_integrantes(site)


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
.brand{font-family:var(--mono-face);font-size:.8rem;letter-spacing:.1em;text-transform:uppercase;
color:var(--pine);font-weight:600;margin:0 0 1rem;line-height:1.5;max-width:44ch;}
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
.cal-wrap{display:grid;grid-template-columns:17rem minmax(0,1fr);gap:1.4rem;align-items:start;}
@media (max-width:640px){.cal-wrap{grid-template-columns:1fr;}}
.cal{background:var(--surface);border:1px solid var(--line);border-radius:14px;padding:1rem;box-shadow:var(--shadow);}
.cal-head{display:flex;align-items:center;justify-content:space-between;margin-bottom:.6rem;}
.cal-title{font-family:var(--title-face);font-weight:600;font-size:1.05rem;text-transform:capitalize;}
.cal-nav{background:var(--surface-2);border:1px solid var(--line);border-radius:8px;color:var(--ink);
width:1.9rem;height:1.9rem;cursor:pointer;font-size:1rem;line-height:1;}
.cal-nav:hover{border-color:var(--pine);color:var(--pine-strong);}
.cal-grid{display:grid;grid-template-columns:repeat(7,1fr);gap:.15rem;text-align:center;}
.cal-wd{font-family:var(--mono-face);font-size:.62rem;text-transform:uppercase;letter-spacing:.03em;
color:var(--faint);padding:.2rem 0 .35rem;}
.cal-cell{aspect-ratio:1;border:none;background:none;color:var(--muted);font-size:.82rem;border-radius:8px;
display:flex;align-items:center;justify-content:center;position:relative;font-variant-numeric:tabular-nums;padding:0;}
.cal-cell.blank{visibility:hidden;}
.cal-cell.today{color:var(--ink);box-shadow:inset 0 0 0 1px var(--line);}
.cal-cell.has-ev{color:var(--pine-strong);font-weight:650;background:var(--pine-soft);cursor:pointer;}
.cal-cell.has-ev::after{content:"";position:absolute;bottom:.26rem;width:.28rem;height:.28rem;
border-radius:50%;background:var(--pine);}
.cal-cell.has-ev:hover{outline:1px solid var(--pine);}
.cal-cell[disabled]{cursor:default;}
.cal-list .event.flash{animation:evflash 1.6s ease;}
@keyframes evflash{0%,25%{background:var(--pine-soft);border-left-color:var(--pine-strong);}100%{background:var(--surface);}}
@media (prefers-reduced-motion:reduce){.cal-list .event.flash{animation:none;}}
.hero-actions:empty{display:none;}
.hero-actions{margin:1.3rem 0 0;display:flex;flex-wrap:wrap;gap:.7rem;}
.page-head{border-bottom:1px solid var(--line);
background:radial-gradient(130% 120% at 85% -20%,var(--pine-soft),transparent 55%),var(--surface);}
.page-head-in{max-width:62rem;margin:0 auto;padding:2.8rem 1.5rem 1.6rem;}
.page-eyebrow{font-family:var(--mono-face);font-size:.8rem;letter-spacing:.12em;text-transform:uppercase;
color:var(--pine);font-weight:600;margin:0 0 .8rem;}
.page-eyebrow a{color:inherit;text-decoration:none;}
.page-title{font-family:var(--title-face);font-weight:600;font-size:clamp(2rem,4.6vw,2.8rem);
line-height:1.05;letter-spacing:-.015em;margin:0 0 .4rem;}
.page-sub{color:var(--muted);font-size:1.1rem;margin:0;max-width:52ch;}
.member{flex-direction:row;gap:1rem;align-items:flex-start;}
.avatar{width:3.4rem;height:3.4rem;border-radius:50%;flex:none;overflow:hidden;display:flex;
align-items:center;justify-content:center;background:var(--pine-soft);border:1px solid var(--line);}
.avatar img{width:100%;height:100%;object-fit:cover;}
.avatar.mono{font-family:var(--mono-face);font-weight:600;color:var(--pine-strong);font-size:1.1rem;}
.minfo{display:flex;flex-direction:column;gap:.2rem;min-width:0;}
.minfo h3{margin:0;}
.mfunc{font-family:var(--mono-face);font-size:.72rem;letter-spacing:.04em;text-transform:uppercase;
color:var(--pine);font-weight:600;}
.minfo p{margin:.1rem 0 .2rem;color:var(--muted);font-size:.92rem;}
.mlinks{display:flex;flex-wrap:wrap;gap:.4rem;margin-top:.2rem;}
.mlinks .badge{text-decoration:none;color:var(--muted);}
.mlinks .badge:hover{border-color:var(--pine);color:var(--pine-strong);}
.ws-btn{display:inline-flex;align-items:center;gap:.5rem;background:var(--pine);color:#fff;
text-decoration:none;font-weight:600;font-size:.95rem;padding:.6rem 1.15rem;border-radius:999px;
box-shadow:var(--shadow);transition:transform .15s,background .15s;}
.ws-btn:hover{transform:translateY(-2px);background:var(--pine-strong);color:#fff;}
@media (prefers-color-scheme:dark){.ws-btn,.ws-btn:hover{color:#08110d;}}
:root[data-theme="light"] .ws-btn,:root[data-theme="light"] .ws-btn:hover{color:#fff;}
:root[data-theme="dark"] .ws-btn,:root[data-theme="dark"] .ws-btn:hover{color:#08110d;}
@media (prefers-reduced-motion:reduce){.ws-btn:hover{transform:none;}}
.media-grid{display:flex;flex-direction:column;gap:1.6rem;}
.media{background:var(--surface);border:1px solid var(--line);border-radius:14px;overflow:hidden;box-shadow:var(--shadow);}
.embed{position:relative;width:100%;padding-bottom:56.25%;height:0;background:#000;}
.embed iframe{position:absolute;inset:0;width:100%;height:100%;border:0;}
.media-cap{padding:1rem 1.3rem 1.3rem;}
.media-cap h3{font-family:var(--title-face);font-weight:600;font-size:1.2rem;margin:0 0 .25rem;}
.media-cap p{margin:0 0 .5rem;color:var(--muted);font-size:.95rem;}
.fgroup{font-family:var(--title-face);font-weight:600;font-size:1.25rem;margin:1.8rem 0 .7rem;}
.fgroup:first-child{margin-top:0;}
.tablewrap{overflow-x:auto;border:1px solid var(--line);border-radius:12px;margin:.4rem 0 1.4rem;}
.tablewrap table{border-collapse:collapse;width:100%;font-size:.93rem;min-width:34rem;}
.tablewrap th,.tablewrap td{text-align:left;padding:.6rem .85rem;border-bottom:1px solid var(--line);vertical-align:top;}
.tablewrap thead th{background:var(--surface-2);font-weight:650;font-size:.8rem;letter-spacing:.02em;}
.tablewrap tbody tr:last-child td{border-bottom:none;}
.tablewrap tbody tr:hover{background:var(--surface-2);}
.tablewrap td.fw{white-space:nowrap;}
.badge{display:inline-block;font-family:var(--mono-face);font-size:.68rem;letter-spacing:.03em;
color:var(--muted);background:var(--surface-2);border:1px solid var(--line);border-radius:999px;
padding:.12rem .5rem;white-space:nowrap;}
.ex{color:var(--faint);font-size:.86em;font-style:italic;}
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
    <div class="hero-actions">{ws_button}{integrantes_button}{participe_button}</div>
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
{caljs}
</script>
</body>
</html>
"""

CAL_JS = """
(function(){
  var cal=document.getElementById('cal'); if(!cal) return;
  var evs=[].slice.call(document.querySelectorAll('#cal-list .event[data-date]'));
  var MONTHS=['janeiro','fevereiro','março','abril','maio','junho','julho','agosto','setembro','outubro','novembro','dezembro'];
  var WD=['dom','seg','ter','qua','qui','sex','sáb'];
  function parse(s){ var p=s.split('-'); return new Date(+p[0],+p[1]-1,+p[2]); }
  function iso(yy,mm,dd){ return yy+'-'+String(mm+1).padStart(2,'0')+'-'+String(dd).padStart(2,'0'); }
  var dates={};
  evs.forEach(function(el){
    var s=el.getAttribute('data-date'); if(!s) return;
    var de=parse(el.getAttribute('data-date-fim')||s);
    for(var t=parse(s); t<=de; t.setDate(t.getDate()+1)){
      var k=iso(t.getFullYear(),t.getMonth(),t.getDate());
      (dates[k]=dates[k]||[]).push(el);
    }
  });
  var today=new Date(); today.setHours(0,0,0,0);
  var tkey=iso(today.getFullYear(),today.getMonth(),today.getDate());
  var keys=Object.keys(dates).sort();
  var start=today;
  var up=keys.filter(function(k){ return parse(k)>=today; });
  if(up.length) start=parse(up[0]); else if(keys.length) start=parse(keys[keys.length-1]);
  var y=start.getFullYear(), m=start.getMonth();
  function render(){
    var offset=new Date(y,m,1).getDay(), days=new Date(y,m+1,0).getDate();
    var h='<div class="cal-head"><button class="cal-nav" data-nav="-1" aria-label="Mês anterior">\\u2039</button>'
        +'<span class="cal-title">'+MONTHS[m]+' de '+y+'</span>'
        +'<button class="cal-nav" data-nav="1" aria-label="Próximo mês">\\u203A</button></div><div class="cal-grid">';
    WD.forEach(function(w){ h+='<span class="cal-wd">'+w+'</span>'; });
    var i;
    for(i=0;i<offset;i++) h+='<span class="cal-cell blank"></span>';
    for(var d=1;d<=days;d++){
      var k=iso(y,m,d), cls='cal-cell';
      if(dates[k]) cls+=' has-ev';
      if(k===tkey) cls+=' today';
      h+='<button class="'+cls+'" data-day="'+k+'"'+(dates[k]?'':' disabled')+'>'+d+'</button>';
    }
    cal.innerHTML=h+'</div>';
  }
  cal.addEventListener('click',function(e){
    var nav=e.target.closest('[data-nav]');
    if(nav){ m+=+nav.getAttribute('data-nav'); if(m<0){m=11;y--;} if(m>11){m=0;y++;} render(); return; }
    var day=e.target.closest('[data-day]');
    if(day && !day.disabled){
      var els=dates[day.getAttribute('data-day')];
      if(els && els[0]){
        els[0].scrollIntoView({behavior:'smooth',block:'center'});
        els.forEach(function(el){ el.classList.remove('flash'); void el.offsetWidth; el.classList.add('flash'); });
      }
    }
  });
  render();
})();
"""


INTEGRANTES_TEMPLATE = """<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Integrantes — BIIA</title>
<meta name="color-scheme" content="light dark">
<style>{css}</style>
</head>
<body>
<header class="page-head"><div class="page-head-in">
  <p class="page-eyebrow"><a href="index.html">&#8592; Materiais BIIA</a></p>
  <h1 class="page-title">Integrantes do BIIA</h1>
  <p class="page-sub">O Laboratório de Bioinformática e Inteligência Agrícola em pessoas.</p>
</div></header>
<main class="wrap" style="padding:2.4rem 1.5rem 4rem;">{body}</main>
<footer><div class="foot-in"><span>{foot_l}</span><span>{foot_r}</span></div></footer>
</body>
</html>
"""


if __name__ == "__main__":
    build()
