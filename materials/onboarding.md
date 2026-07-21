# Guia de Onboarding — Estagiários de IC (BIIA-Csordidus)

> Guia de estudo + roteiro de trabalho para os estagiários que farão a anotação
> de famílias gênicas em *Cosmopolites sordidus* (bicudo-da-bananeira).
> Cada estagiário fica responsável por **uma família/categoria**.
>
> Como usar: leia a Parte A (o que você vai fazer), faça a instalação da Parte B,
> estude os módulos da Parte C **fazendo os exercícios**, e só então siga o
> roteiro de execução da Parte E. As respostas dos exercícios técnicos estão no
> fim (Apêndice). As questões de biologia são para **discutir com a orientadora**.

---

## PARTE A — O que você vai fazer (visão geral)

O projeto varre o proteoma inteiro do inseto procurando **domínios proteicos**
(Pfam) e, a partir disso, seleciona e anota as proteínas de famílias de
interesse (quimiorrecepção, detoxificação, metabolismo, sobrevivência).

O trabalho está dividido em duas fases:

- **Fase BASE (já feita para você):** validação, limpeza e a busca pesada de
  domínios (módulos M01→M04). O resultado já vem **pronto no pendrive**. Você
  **não** precisa refazer essa parte demorada.
- **Fase da SUA FAMÍLIA (sua responsabilidade):** a partir do módulo **M05**,
  você seleciona as candidatas da sua família, roda as evidências (InterProScan
  e BLAST), integra tudo em uma tabela de anotação e gera as estatísticas
  (M05 → M13). Depois **cura** os resultados (olhar caso a caso).

> **Por que isso funciona:** a busca de domínios (M03) é **agnóstica de família**
> — ela vale para qualquer família. Por isso é feita uma vez só e reaproveitada.

---

## PARTE B — Antes de começar (instalação, uma vez por computador)

O pendrive traz os **arquivos** do projeto, mas **não** traz o ambiente de
programas (BLAST, HMMER, Python e bibliotecas). Isso você instala no seu
computador **uma única vez**.

1. Copie a pasta `BIIA-Csordidus/` do pendrive para o seu computador (ex.: para
   a Área de Trabalho). **Trabalhe na cópia do seu computador, nunca direto no
   pendrive.**
2. Instale o **Miniforge** (gerenciador `conda`).
   - Mac (com Homebrew): `brew install --cask miniforge`
3. Crie o ambiente do projeto a partir do arquivo `environment.yml`:
   - **Mac com chip Apple (M1/M2/M3):**
     ```bash
     CONDA_SUBDIR=osx-64 mamba env create -f environment.yml
     conda activate biia-csordidus
     conda config --env --set subdir osx-64
     ```
   - **Outros:** `mamba env create -f environment.yml` e `conda activate biia-csordidus`
4. Toda vez que for trabalhar, ative o ambiente antes:
   ```bash
   conda activate biia-csordidus
   ```

> ⚠️ Se aparecer o erro *"Could not solve for environment specs: blast/hmmer
> does not exist"* no Mac, é porque faltou o `CONDA_SUBDIR=osx-64` do passo 3.

---

## PARTE C — Mapa das suas pastas

Dentro de `BIIA-Csordidus/` (o que você recebeu):

```
BIIA-Csordidus/
├── biia/              # código do pipeline (você LÊ, raramente edita)
├── scripts/           # os módulos M01..M13 que você executa
├── config/
│   ├── config.yaml        # configuração BASE — NÃO edite
│   ├── config_MEU.yaml    # SUA configuração (e-mail + sua família) ← VOCÊ EDITA
│   ├── targets.yaml       # catálogo de todas as famílias (referência)
│   └── targets_MEU.yaml   # SÓ a sua família ← VOCÊ EDITA
├── data/
│   ├── raw/proteome.faa           # proteoma de entrada (já incluído)
│   ├── processed/                 # JÁ PRONTO: proteome_clean.faa, id_map.tsv
│   └── reference/
│       └── blast/swissprot/       # banco BLAST Swiss-Prot (já incluído)
├── results/
│   ├── 03_hmmer/hmmscan.domtblout        # ← MESTRE, JÁ PRONTO. NÃO APAGUE!
│   ├── 04_hmmer_parsed/hmmer_hits.tsv    # ← JÁ PRONTO. NÃO APAGUE!
│   └── (05.. até 13 serão criados por VOCÊ quando rodar)
├── environment.yml
└── Makefile
```

**Regra de ouro:** nunca apague `data/processed/` nem `results/03_hmmer/` e
`results/04_hmmer_parsed/`. São o trabalho pesado já pronto; tudo que você faz
parte deles.

---

## PARTE D — Módulos de estudo (com exercícios)

Estude na ordem. Faça os exercícios no seu computador, com o ambiente ativado.

### Módulo 1 — Linha de comando (terminal / Bash)

**Você precisa saber:** navegar entre pastas, olhar arquivos sem abrir tudo,
rodar comandos e ler mensagens de erro.

Comandos-chave: `cd`, `ls`, `pwd`, `head`, `tail`, `less`, `wc -l`, `grep`, `cut`.

**Exercícios:**
1. Abra o terminal, entre na pasta do projeto (`cd .../BIIA-Csordidus`) e
   confirme onde está com `pwd`.
2. Liste o conteúdo de `data/raw/` com `ls -la`.
3. Quantas sequências há no proteoma? (Dica: cada sequência começa com `>`.)
   `grep -c '^>' data/raw/proteome.faa`
4. Mostre os 3 primeiros cabeçalhos: `grep '^>' data/raw/proteome.faa | head -3`
5. Veja as primeiras 5 linhas de `results/04_hmmer_parsed/hmmer_hits.tsv` com
   `head -5`. Quantas colunas parecem ter?

### Módulo 2 — Ambiente conda

**Você precisa saber:** que os programas do pipeline só existem *dentro* do
ambiente, e como ativá-lo.

**Exercícios:**
1. Ative o ambiente: `conda activate biia-csordidus`.
2. Confirme que as ferramentas existem:
   `which blastp hmmsearch makeblastdb cd-hit`
3. Veja a versão do BLAST: `makeblastdb -version`
4. **Teste do erro:** abra um terminal **sem** ativar o ambiente e rode
   `blastp -version`. O que acontece? (Anote a mensagem — é o erro típico de
   "esqueci de ativar o ambiente".)

### Módulo 3 — YAML e o arquivo da sua família (`targets`)

**Você precisa saber:** editar arquivos YAML (a configuração das famílias) sem
quebrar a indentação. Em YAML, **indentação é com espaços, nunca TAB**.

Bloco de uma família (exemplo real de `targets.yaml`):
```yaml
categories:
  quimiorrecepcao:
    families:
      OBP:
        description: "Odorant-binding proteins"
        pfam_diagnostic: ["PF01395"]   # domínio que caracteriza a família
        length_range_aa: [110, 250]    # faixa de tamanho esperada
```

**Exercícios:**
1. Abra `config/targets_MEU.yaml` e identifique: qual é o **domínio diagnóstico
   (PFxxxxx)** da sua família e qual a **faixa de tamanho**?
2. Faça uma cópia de teste (`cp config/targets_MEU.yaml /tmp/teste.yaml`),
   troque um espaço de indentação por um TAB e tente carregar — observe que
   quebra. Depois desfaça. (Objetivo: sentir como YAML é sensível.)
3. Pesquise, na base Pfam (site InterPro/Pfam), o que é o domínio diagnóstico
   da sua família. Anote em uma frase o que ele representa biologicamente.

### Módulo 4 — Ler tabelas de resultado (TSV)

**Você precisa saber:** abrir e interpretar as tabelas `.tsv` que os módulos
geram — é o coração da **curadoria**.

Você pode abrir no **Excel/LibreOffice** (importando como "separado por
tabulação") ou com **Python/pandas**:
```python
import pandas as pd
df = pd.read_csv("results/05_candidates/candidates.tsv", sep="\t")
print(df.shape)      # (linhas, colunas)
print(df.head())
```

**Exercícios (faça depois de rodar sua fase — Parte E):**
1. Abra `results/05_candidates/candidates.tsv`. Quantas candidatas a sua família
   teve? (compare com `family_counts.tsv`).
2. Abra `results/10_integration/annotation_table.tsv`. Quantas proteínas ficaram
   em **nível de evidência A**, quantas em **B** e quantas em **C**?
3. Ordene por identidade (`pident`) do melhor hit BLAST. Qual candidata teve o
   hit mais forte? E a mais fraca?

### Módulo 5 — Python (leitura leve — opcional, mas recomendado)

**Você precisa saber (o básico):** ler uma mensagem de erro (*traceback*) e
entender o que um script faz lendo o código. O código foi escrito para ser
legível por estagiário.

**Exercícios:**
1. Abra `biia/fasta.py` e leia a função `iter_fasta`. Explique, em uma frase,
   por que ela lê "uma sequência por vez" em vez de tudo de uma vez.
2. Provoque um erro de propósito: rode um módulo apontando para um config que
   não existe (`--config config/naoexiste.yaml`). Leia o *traceback*: qual é a
   última linha (a mensagem do erro)?

---

## PARTE D2 — Alfabetização em ferramentas e formatos

Antes de curar, entenda o que cada número significa.

### FASTA
Arquivo de sequências. Cada registro tem **cabeçalho** (linha com `>`) e a
**sequência** (aminoácidos, no nosso caso — proteínas).

*Exercício:* pegue um cabeçalho do `candidates.faa` e diga qual é o **ID** da
proteína.

### HMMER / Pfam (domínios)
Um **domínio** é uma região funcional/estrutural conservada da proteína. O Pfam
é um catálogo de domínios, cada um com um **perfil HMM**. O `--cut_ga` usa um
limiar curado por família (mais confiável que E-value fixo). A tabela
`hmmer_hits.tsv` lista **domínios encontrados**, não famílias prontas.

*Exercício:* em `results/04_hmmer_parsed/hmmer_hits.tsv`, ache uma linha com o
domínio diagnóstico da sua família (o `PFxxxxx` do Módulo 3). Qual proteína o
contém?

### BLAST (blastp)
Compara suas candidatas com proteínas já conhecidas (Swiss-Prot). Colunas que
importam (definidas no config):
- `pident` — **identidade %** com o hit
- `qcov` (derivada de `length`/`qlen`) — **cobertura**: quanto da sua proteína foi alinhada
- `evalue` — significância (quanto **menor**, melhor)
- `bitscore` — pontuação (quanto **maior**, melhor)
- `stitle` — descrição do hit (contém o organismo, ex.: `OS=...`)

Limiares do projeto (M09): `pident ≥ 30%`, `qcov ≥ 50%`, `evalue ≤ 1e-5`.

*Exercício:* um hit com `pident = 32%` e `qcov = 55%` passa no filtro mínimo?
E ele seria "forte" (nível A exige `pident ≥ 50%` e `qcov ≥ 70%`)? Justifique.

### InterProScan
Roda **online** (serviço do EBI) e agrega domínios de várias fontes + **termos
GO** (função) + vias. Precisa de internet e do seu **e-mail** no config (é só
identificação — **não precisa criar conta**).

*Exercício:* explique por que "só ter um termo GO em comum" é uma evidência
**fraca** (dica: GOs muito genéricos aparecem em muitas proteínas).

---

## PARTE D3 — Biologia molecular (revisar com a orientadora)

Estas questões são para **discutir na revisão** — são onde a interpretação
biológica decide a curadoria.

1. **Domínio ≠ proteína ≠ família.** Por que ter o domínio diagnóstico não basta
   para afirmar que a proteína é da família? (Pense em domínio de apoio e
   tamanho plausível.)
2. **Ortólogo × parálogo.** Qual a diferença? Por que famílias de praga
   (quimiorrecepção, detoxificação) costumam estar **expandidas** (muitos
   parálogos)? — isto é o que o M12 mede.
3. **Conservação e os 3 regimes:** por que uma **OBP** (curta, divergente) tende
   a dar **falso-negativo**, uma **catalase** é fácil (controle positivo), e um
   domínio como **GH13 (amilase)** tende a dar **falso-positivo**?
4. **Inferência de função por homologia:** quais os riscos de "transferir"
   a anotação de um hit? Por que existem os **níveis A/B/C** e por que o nível A
   exige **concordância de InterPro**, não só um BLAST forte?
5. **Contexto taxonômico:** por que um hit em **Coleoptera** vale mais? (conceito
   de `is_coleoptera_hit`).
6. **A biologia da SUA família:** qual a função dela no inseto e por que é
   relevante para o controle da praga *Cosmopolites sordidus*?
7. **GO e InterPro:** o que é um termo GO (função molecular, processo biológico,
   componente celular) e uma entrada InterPro?

---

## PARTE E — Roteiro de execução (a sua fase: M05 → M13)

Com o ambiente ativado e dentro da pasta do projeto. Use **sempre** o seu
config (`config_MEU.yaml`).

```bash
conda activate biia-csordidus

# M05 — seleciona as candidatas da sua família
python scripts/05_filter_candidates.py --config config/config_MEU.yaml

# M06 — InterProScan (online; precisa de internet e do seu e-mail no config)
python scripts/06_run_interproscan.py --config config/config_MEU.yaml

# M08 / M09 — BLAST contra Swiss-Prot e leitura dos resultados
python scripts/08_run_blast.py  --config config/config_MEU.yaml
python scripts/09_parse_blast.py --config config/config_MEU.yaml

# M10 — integra evidências e atribui nível A/B/C
python scripts/10_integrate_evidence.py --config config/config_MEU.yaml

# M12 — parálogos / expansão da família (CD-HIT)
python scripts/12_characterize_clusters.py --config config/config_MEU.yaml

# M13 — estatísticas e figuras finais
python scripts/13_statistics.py --config config/config_MEU.yaml
```

Depois de cada passo, **olhe o `report.md`** gerado na pasta de resultados
daquele módulo — ele resume o que aconteceu.

---

## PARTE F — Checklist antes de entregar à orientadora

- [ ] Rodei M05 → M13 sem erros (cada `status.json` = ok).
- [ ] Conferi `results/05_candidates/family_counts.tsv` (nº de candidatas).
- [ ] Curadoria: revisei a `annotation_table.tsv`, caso a caso, olhando nível
      de evidência, `pident`/`qcov` e a descrição do hit.
- [ ] Anotei as candidatas duvidosas para discutir na revisão.
- [ ] Guardei as figuras do M13.
- [ ] **Não** apaguei `data/processed/` nem `results/03_hmmer` / `04_hmmer_parsed`.

---

## Apêndice — Respostas dos exercícios técnicos

- **M1.3:** `grep -c '^>' data/raw/proteome.faa` → deve retornar 193810.
- **M2.4:** sem o ambiente ativado, o sistema diz que `blastp` não foi
  encontrado (*command not found*) — porque o programa vive dentro do env.
- **M4.1/4.2:** os números saem de `family_counts.tsv` e
  `evidence_level_counts.tsv` (colunas A/B/C).
- **Ferramentas/BLAST:** `pident=32%`, `qcov=55%` → **passa** no filtro mínimo
  (≥30% e ≥50%), mas **não** é "forte" (nível A pede ≥50% e ≥70%). Provavelmente
  seria nível B ou C.
- **InterProScan:** GOs genéricos (ex.: "binding", "catalytic activity")
  aparecem em milhares de proteínas; concordância só faz sentido com termos/
  domínios específicos — por isso o nível A exige concordância de **InterPro**.

> Dúvidas? Anote e leve para a revisão com a orientadora. É normal travar no
> começo — o objetivo desta fase é você ganhar autonomia no operacional para
> focar na **interpretação biológica**, que é o que realmente importa.
