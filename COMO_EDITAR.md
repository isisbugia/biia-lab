# Como editar o conteúdo do site

Você edita **texto**; eu monto a página. Nenhum arquivo abaixo é HTML — são
arquivos de texto simples (YAML) em `content/`. Cada um controla uma aba.

## Qual arquivo controla o quê

| Arquivo em `content/` | Aba / parte do site |
|---|---|
| `site.yaml` | Título, subtítulo, descrição e rodapé (topo do site). |
| `guias.yaml` | Aba **Guias de estudo** (lista numerada). |
| `ferramentas.yaml` | Aba **Ferramentas de Bioinfo**. |
| `videoaulas.yaml` | Aba **Vídeoaulas e Tutoriais**. |
| `recursos.yaml` | Aba **Recursos educativos**. |
| `avisos.yaml` | Aba **Quadro de avisos**. |
| `eventos.yaml` | Aba **Eventos importantes**. |

## Como editar

1. Abra o arquivo da parte que quer mudar.
2. Edite o **texto depois dos dois-pontos** (`:`), mantendo a estrutura e a
   indentação (os espaços no início das linhas).
3. Para **adicionar um item**, copie um bloco que começa com `-` e edite; ou
   tire o `#` de um exemplo comentado.
4. Salve e me devolva (ou me diga as mudanças). **Eu rodo o gerador e publico** —
   o site atualiza em ~1 min.

### Regras rápidas de YAML (para não quebrar)

- Mantenha os **espaços** no começo das linhas (a indentação importa).
- Textos com **dois-pontos** ou aspas: coloque entre `"aspas"`.
- Uma linha começada com `#` é **comentário** (o site ignora).
- Datas no formato `AAAA-MM-DD` (ex.: `2026-07-27`).

## E o texto DENTRO de um guia de estudo?

Atenção: os arquivos `content/*.yaml` controlam **o site** (abas, cards, avisos).
Eles **não** contêm o texto interno de cada guia.

Cada guia (ex.: `guia-rastreabilidade-qc.html`) é um **documento completo e
desenhado** (com diagramas, tabelas, destaques). O texto dele mora numa **fonte
markdown separada**, no repositório do projeto
(`BIIA-Csordidus/docs/guia_estudo_rastreabilidade_qc.md`) — markdown puro, fácil
de editar. O `.html` do site é uma renderização dessa fonte.

**Para mudar o texto de um guia:** edite o markdown do guia **ou** peça a alteração
em português. A versão visual é regenerada e republicada — o `guias.yaml` só muda
o **card** (número, título, resumo, link), não o miolo.

## Detalhe técnico (para quem for rodar)

O gerador é `build.py` (precisa de `pyyaml`). Ele lê `content/*.yaml` e escreve
`index.html`. Rodar: `python build.py`. Os guias de estudo em si (ex.:
`guia-rastreabilidade-qc.html`) são arquivos separados, referenciados em
`guias.yaml` pelo campo `link`.
