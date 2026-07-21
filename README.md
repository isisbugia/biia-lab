# BIIA — Materiais abertos do laboratório

Site público de materiais de estudo do **Laboratório de Bioinformática e
Inteligência Agrícola (BIIA)** — IFSP, Campus Miracatu — a partir do trabalho com
*Cosmopolites sordidus* (broca-do-rizoma da bananeira).

🌐 **Site:** https://isisbugia.github.io/biia-lab/

## Como funciona

O conteúdo mora em arquivos de texto simples em [`content/`](content/) (um por
aba); o gerador [`build.py`](build.py) monta o `index.html`. Para editar textos,
veja **[COMO_EDITAR.md](COMO_EDITAR.md)** — você mexe só no conteúdo, não no HTML.

Abas: Guias de estudo · Ferramentas de Bioinfo · Vídeoaulas e Tutoriais ·
Recursos educativos · Quadro de avisos · Eventos importantes.

Regenerar o site após editar o conteúdo:

```
python build.py        # precisa de pyyaml
```

## Conteúdo atual

- **Guia de estudo 01 — Rastreabilidade & Controle de Qualidade**
  ([guia-rastreabilidade-qc.html](guia-rastreabilidade-qc.html)).

Cada guia é um HTML **autossuficiente** (abre offline, sem conta).

## Relação com o projeto

Este repositório é **público** (só material de divulgação). O desenvolvimento do
pipeline vive num repositório **privado** separado (`BIIA-Csordidus`); a fonte
editável dos guias é mantida lá (em `docs/`) e publicada aqui como versão visual.
