# Material Preparatório — focado na execução do pipeline BIIA

> Para estagiários de IC que vão **executar o pipeline** do projeto (fase futura).
> Escrito para quem nunca programou, mas **só com o que se usa neste projeto** —
> nada de teoria de programação que você não vai precisar. Depois deste material,
> siga o [guia de onboarding](guia_onboarding_bolsistas.md) (o roteiro prático).
>
> **A regra deste material:** você vai **rodar** programas prontos, **editar**
> arquivos de configuração e **ler** resultados. Você NÃO vai escrever programas.
> Então focamos exatamente nessas três coisas.

---

## O que você realmente vai fazer (o mapa)

1. **Ativar** o ambiente (uma vez por sessão).
2. **Editar** um arquivo de configuração para dizer qual família anotar.
3. **Rodar** os módulos do pipeline (um comando cada).
4. **Ler** as saídas (tabelas, relatórios, sequências).
5. **Entender o erro** quando algo falha.

As cinco seções abaixo são exatamente essas cinco coisas. É só isso.

---

## 1. Terminal — só os comandos que você vai usar

O **terminal** é a janela onde você digita comandos. Você não precisa dominar o
terminal inteiro — só estes:

| Comando | Para que serve NESTE projeto |
|---|---|
| `cd BIIA-Csordidus` | entrar na pasta do projeto (é de lá que tudo roda) |
| `ls` | ver o que há na pasta |
| `less results/05_candidates/report.md` | ler um relatório (aperte `q` para sair) |
| `grep -c '^>' data/raw/proteome.faa` | contar quantas sequências há num FASTA |
| `head results/05_candidates/candidates.tsv` | espiar o começo de uma tabela |

Só isso já cobre 90% do seu dia. O resto você aprende quando precisar.

**Exercício:** com o projeto montado, entre na pasta e conte as sequências do
proteoma: `grep -c '^>' data/raw/proteome.faa`.

> **Dica de erro:** "No such file or directory" = o caminho está errado (confira
> se você está na pasta certa com `pwd` e se digitou maiúsculas/minúsculas
> corretamente).

---

## 2. Ativar o ambiente (conda)

Os programas do projeto (BLAST, HMMER, Python + bibliotecas) vivem dentro de um
**ambiente** isolado. Antes de trabalhar, você o ativa:

```bash
conda activate biia-csordidus
```

Se você esquecer disso, os comandos falham com "command not found" — é o erro
nº 1. Ativar não muda nada nos seus arquivos; só "liga" as ferramentas certas.
(A instalação do ambiente é feita uma vez; está no guia de onboarding.)

---

## 3. Editar a configuração (YAML) — o que você mais vai mexer

Para anotar uma família, você a descreve num arquivo `.yaml`. **YAML** é só um
jeito organizado de escrever configurações. É aqui que você trabalha de verdade.

Exemplo real de uma família no `config/targets.yaml`:
```yaml
  quimiorrecepcao:                     # categoria
    families:
      OBP:                             # nome da família
        description: "Odorant-binding proteins"
        pfam_diagnostic: ["PF01395"]   # o domínio que caracteriza a família
        length_range_aa: [110, 250]    # faixa de tamanho esperada
```

Para trabalhar sem atrapalhar as colegas, cada estagiário tem um config próprio,
`config/config_MEU.yaml`, que aproveita o principal e muda só o essencial:
```yaml
extends: "config.yaml"
m06_interproscan:
  email: "seu.email@aluno.ifsp.edu.br"
paths_override:
  targets: "${project_root}/config/targets_MEU.yaml"
```

**As 3 regras de YAML que evitam 99% dos erros:**
1. Indentação é com **espaços**, nunca TAB (um espaço errado quebra o arquivo).
2. Formato é `chave: valor`.
3. Listas usam colchetes `["PF01395"]` ou hífens.

**Exercício:** abra `config/targets.yaml` e encontre o **domínio diagnóstico**
(`pfam_diagnostic`) e a **faixa de tamanho** da família CATALASE.

> Use um editor de **código** (VS Code) para editar YAML — ele mostra a
> indentação e ajuda a não errar. Nunca edite no Word.

---

## 4. Rodar o pipeline (o padrão dos comandos)

Todo módulo se roda **do mesmo jeito**:
```bash
python scripts/05_filter_candidates.py --config config/config_MEU.yaml
```
Muda só o número/nome do script. `--config` diz qual configuração usar. Há também
atalhos no `Makefile` (ex.: `make m05 CONFIG=config/config_MEU.yaml`).

Dois "acessórios" úteis (valem em todos os módulos):
- `--dry-run` → mostra o que **seria** feito, sem executar (ótimo para conferir
  antes de rodar algo demorado).
- `--force` → refaz uma saída que já existe (por padrão, o módulo não sobrescreve).

**Exercício:** rode um módulo em modo de teste:
`python scripts/05_filter_candidates.py --config config/config_MEU.yaml --dry-run`.

---

## 5. Ler as saídas

Cada módulo escreve numa pasta em `results/` (ex.: `results/05_candidates/`).
Três tipos de arquivo importam:

| Arquivo | O que é |
|---|---|
| `report.md` | **Relatório humano** — leia primeiro; resume o que aconteceu. |
| `status.json` | Resumo para a máquina (o `make check` usa). |
| `candidates.tsv` / `family_counts.tsv` | **Tabelas** de resultado (abrem no Excel/LibreOffice; colunas separadas por tabulação). |
| `candidates.faa` | As **sequências** das candidatas (FASTA). |

**FASTA e TSV — o que você vai ver:**
- **FASTA (`.faa`):** linha com `>` = cabeçalho; abaixo, a sequência de aminoácidos.
- **TSV:** tabela em texto; cada coluna separada por um "tab". Abra no
  Excel/LibreOffice importando como "separado por tabulação".

**Exercício:** depois de rodar, abra `results/05_candidates/report.md` (com `less`
ou num editor) e veja quantas candidatas cada família teve.

---

## 6. Quando dá erro (não entre em pânico)

Os módulos avisam claramente. Cada um termina com um **código**:

| Código | Significa | O que costuma ser |
|---|---|---|
| 0 | sucesso | tudo certo (ou a saída já existia) |
| 1 | erro de configuração | algo no `.yaml` (indentação, chave errada) |
| 2 | erro de entrada | arquivo faltando (rodou fora de ordem?) |
| 3 | erro de ferramenta | esqueceu de ativar o ambiente? banco faltando? |

**Como agir:** leia a **última linha** da mensagem — costuma dizer exatamente o
que faltou. Anote o que fez antes e **traga para a reunião** se não resolver.
Erros são normais e quase sempre têm solução simples.

---

## 7. Python — o mínimo (você roda, não escreve)

Neste projeto você **não escreve** Python — você roda scripts prontos. Então só
precisa de duas noções:

1. **Rodar:** `python scripts/nome.py --config ...` (visto acima).
2. **Ler um erro (traceback):** quando um script Python falha, ele imprime várias
   linhas terminando na causa. **Leia a última linha** — é o resumo do problema.

Só isso é suficiente para a execução. (Se mais adiante você quiser *entender* o
que um script faz por dentro, o código do projeto foi escrito para ser legível —
mas isso é opcional e vem depois.)

---

## Roteiro de estudo (enxuto e direcionado)

Ritmo tranquilo, focado no que acima. Não precisa de curso longo.

| Etapa | Foco | Recurso |
|---|---|---|
| 1 | Os 5 comandos de terminal da Seção 1 | pratique no seu computador |
| 2 | YAML: ler e editar uma família (Seção 3) | `config/targets.yaml` do projeto |
| 3 | Rodar um módulo e ler o `report.md` (Seções 4–5) | o próprio pipeline |
| 4 | Ler um erro e um código de saída (Seção 6) | provoque um erro de propósito |

**Metas (amarradas ao projeto):**
- [ ] Entrar na pasta do projeto e contar as sequências do proteoma.
- [ ] Ativar o ambiente `biia-csordidus`.
- [ ] Achar o domínio diagnóstico de uma família no `targets.yaml`.
- [ ] Rodar um módulo com `--dry-run` e depois de verdade.
- [ ] Abrir o `report.md` e interpretar as contagens.
- [ ] Ler uma mensagem de erro e dizer a causa provável.

> Fora desta lista, **não precisa estudar mais nada agora** — o objetivo é você
> operar o pipeline com segurança e focar no que importa: a **interpretação
> biológica**. O que faltar, a gente ensina no caminho.
