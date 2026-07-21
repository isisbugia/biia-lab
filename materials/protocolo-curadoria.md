# Protocolo de Curadoria Manual — Piloto (OBP, Catalase, Alfa-amilase)

> Projeto guarda-chuva: *Anotação funcional com curadoria manual de famílias
> proteicas da broca-da-bananeira (Cosmopolites sordidus)*.
> Este protocolo guia a **fase de curadoria** das candidatas geradas pelo
> pipeline. Acompanha a planilha `curation_pilot/planilha_curadoria_piloto.xlsx`.

---

## 1. O que é (e o que não é) esta etapa

O pipeline já fez o trabalho **computacional**: encontrou proteínas candidatas de
cada família e reuniu evidências (domínios conservados, assinaturas InterPro,
melhor alinhamento BLAST, nível de confiança A/B/C). A **curadoria** é o passo
**humano**: você **avalia** essa evidência e decide, caso a caso, se a proteína
é mesmo da família e qual a sua anotação funcional.

- **Não é** rodar programas — a evidência já está pronta na planilha.
- **É** julgamento biológico informado, registrado de forma rastreável.

## 2. A planilha

Arquivo (alunas): `curation_pilot/planilha_curadoria_EM_BRANCO.xlsx` (Excel/
LibreOffice).
- Aba **Instruções**: resumo rápido.
- Aba **Curadoria**: uma linha por candidata. As colunas à esquerda (evidência)
  já vêm preenchidas; as **cinco últimas, destacadas em laranja, são suas**.
- A coluna **nível_evidência** está colorida: verde = A, amarelo = B.
- Use o **filtro** (cabeçalho) para trabalhar por família.

**Sequências (FASTA):** as proteínas candidatas estão em `curation_pilot/fasta/`
— um arquivo por família (`CATALASE.faa`, `AMILASES.faa`, `OBP.faa`) e um
combinado (`todas_candidatas.faa`). O cabeçalho de cada sequência traz a
**rastreabilidade completa** até o genoma depositado, além de família, nível e
tamanho. Exemplo:

```
>CSOR_04408 orig=g2919.t1 loc=ptg000301l:14913-17233(+) genbank=JARFXV010000299.1 familia=OBP prov=dominio nivel=B len=135
```

| Campo | O que é |
|---|---|
| `CSOR_04408` | **ID do projeto** — use este nas planilhas e no relatório de curadoria. |
| `orig=g2919.t1` | ID original do **proteoma predito** (Braker2). Liga à anotação. |
| `loc=ptg000301l:14913-17233(+)` | **Posição no genoma**: contig, início-fim e fita. |
| `genbank=JARFXV010000299.1` | Contig no **genoma depositado no GenBank** (para citar/checar). Se aparecer `genbank=so_dryad`, o contig só existe na montagem do Dryad. |
| `familia / prov / nivel / len` | Família-alvo, proveniência (`dominio`/`similaridade`), nível A/B/C e tamanho (aa). |

Use-os para inspecionar a sequência, alinhar dentro da família (ex.: ver o padrão
de cisteínas das OBPs) ou rodar sua própria conferência (BLAST/InterPro).

> **⚠️ Ao conferir no BLAST, não busque contra o *genoma* — busque contra o
> *proteoma*.** Uma proteína predita é a junção dos éxons (o preditor removeu os
> íntrons). Se você BLASTar a proteína contra o **DNA do genoma**, o alinhamento
> quebra em pedaços (um por éxon) e **não dá 100%** — isso é normal, não é erro.
> Para confirmar que a sequência confere, faça `blastp` da candidata contra o
> **proteoma** (`data/raw/proteome.faa`): aí o acerto é 100%. (Ex. real: `CSOR_04408`
> tem 2 éxons separados por um íntron de ~1,9 kb — por isso some o 100% no genoma.)

## 3. Entendendo as colunas de evidência

| Coluna | O que significa |
|---|---|
| original_id | ID no proteoma predito (ex.: `g2919.t1`) — rastreabilidade até a anotação. |
| genomic_location | Posição no genoma: `contig:início-fim(fita)`. |
| genbank_accession | Contig no genoma depositado no GenBank (`JARFXV…`) ou `so_dryad`. |
| arquitetura_domínios | Sequência de domínios Pfam encontrados (ex.: `PF00199:PF06628`). O **diagnóstico** da família tem que estar presente. |
| domínios_InterPro | Assinaturas InterPro (corroboram o domínio). |
| nível_evidência | **A** = forte (domínio + concordância InterPro + bom hit); **B** = intermediário; **C** = fraco. |
| melhor_hit_descrição | Proteína mais parecida em banco de referência (ex.: *general odorant-binding protein 83a-like [Sitophilus oryzae]*). |
| hit_identidade_% / cobertura_% | Quão parecido e quão completo é o alinhamento. Maior = melhor. |
| hit_coleoptera | `True` = o melhor hit é de um besouro (parente próximo) → reforça a confiança. |
| flags | Sinalizações automáticas — não reprovam sozinhas, são para olhar: `LENGTH_ATYPICAL` = tamanho fora da faixa esperada; **`LOW_COMPLEXITY`** = sequência de baixa complexidade (repetição em tandem, ex.: `QHSTAQHSTA...`), quase sempre **falso positivo** — provável **rejeição** (ver 4b). |

## 4. Critérios de decisão

Preencha **DECISÃO** com uma das três opções:

### ✅ Confirmada
A proteína é, com segurança, da família. Em geral:
- Domínio **diagnóstico presente** e arquitetura coerente com a família;
- Tamanho dentro (ou próximo) da faixa esperada;
- Bom hit em parente próximo (especialmente `hit_coleoptera = True` com
  identidade alta) **ou** concordância InterPro clara.
- Nível **A** costuma ser confirmação direta — mas **sempre confira** a
  arquitetura e o tamanho (o nível é um guia, não um carimbo).

### ❓ Incerta
Evidência ambígua ou conflitante. É uma resposta **válida e esperada**:
- Nível **B** com hit fraco (baixa identidade/cobertura);
- Melhor hit apenas a proteína "uncharacterized";
- Arquitetura ou tamanho estranhos, mas não claramente errados.
- Descreva a dúvida na **JUSTIFICATIVA** para discutirmos na reunião.

### ❌ Rejeitada
Evidência indica que **não** é da família:
- Arquitetura **incompatível** (ex.: domínio diagnóstico acompanhado de muitos
  domínios de outra função dominando a proteína);
- Tamanho **muito** fora da faixa sem explicação plausível;
- Ausência de qualquer corroboração além de um match fraco e isolado.

## 4b. Candidatas descobertas por similaridade (proveniência = "similaridade")

Além das candidatas por **domínio**, a planilha traz candidatas descobertas por
**forte semelhança a parentes de besouro, SEM o domínio diagnóstico** (etapa de
descoberta por similaridade). Elas **não** têm nível A/B/C nem InterPro (não
passaram por essas etapas) — a decisão apoia-se em semelhança + arquitetura +
tamanho + julgamento. Curar com **critério extra**:

- **Amilases:** muitas têm `PF02806` (domínio de *apoio*) mas não `PF00128` (o
  catalítico). Se tamanho (~400–550 aa) e identidade forem coerentes, são
  provavelmente **amilases reais** cujo domínio catalítico ficou abaixo do limiar.
  Distinga alfa-amilase digestiva de outras GH13 (maltase/glucosidase).
- **OBP vs CSP:** proteínas com `PF03392` são **CSP** (família vizinha, **não**
  OBP) — classifique corretamente. OBPs **sem domínio**, curtas e com alta
  identidade a OBP de besouro, são candidatas legítimas (divergentes).
- Quanto **menor** a identidade ao besouro, **mais cuidado** — pode ser homologia
  distante ou família aparentada.
- **`LOW_COMPLEXITY` → rejeitar.** Sequências de baixa complexidade (repetição em
  tandem, ex.: `QHSTAQHSTA...`) grudam por acaso em proteínas sem relação (amilase,
  extensina, fator de transcrição) e pegam a família pelo melhor hit à toa. Sinais:
  identidade baixa (~30%), sem domínio catalítico, e o mesmo trecho repetido dezenas
  de vezes. **Não são amilases** — marque **Rejeitada**. (Ex. do piloto: `CSOR_10506`
  e `CSOR_16554`, idênticas, em dois contigs diferentes.)

## 4c. Padrão calibrado (definido com a orientadora — 2026-07-20)

Regras a aplicar de forma **consistente** por todas as curadoras:

1. **Nível A** (domínio diagnóstico + concordância InterPro + bom hit) →
   **Confirmar** como a família. Vale **mesmo quando o melhor hit é
   "uncharacterized protein"** de besouro: o domínio + a alta identidade bastam
   para atribuir a **família** (anotação = nome da família, ex.: "Odorant-binding
   protein").
2. **OBP em nível B** (domínio PF01395 presente, mas homologia ao besouro de
   37–49%) → **Incerta** (revisar caso a caso). Não confirmar automaticamente.
3. **Alfa-amilases (GH13) que batem em "maltase"** → **Confirmar** como família
   (GH13/alfa-amilase) e **anotar especificamente** (ex.: "maltase-like"),
   **sinalizando para sub-classificação funcional** posterior (alfa-amilase
   digestiva vs maltase/glucosidase).
4. **Descobertas por similaridade** (proveniência "similaridade", sem domínio
   diagnóstico) → escrutínio extra (seção 4b): **Confirmar só com evidência
   forte** (domínio de apoio + tamanho coerente + identidade alta); caso
   contrário, **Incerta**.

**Consequência nas 41 candidatas por domínio:** 33 **Confirmar** (5 catalase +
5 alfa-amilase + 23 OBP nível A) e 8 **Incerta** (OBP nível B). As 15 descobertas
seguem a regra 4 (caso a caso).

## 5. Passo a passo por candidata

1. Leia **família** e **arquitetura_domínios** — o domínio diagnóstico está lá e
   coerente?
2. Veja **tamanho_aa** e **flags** — dentro do esperado? Se `LENGTH_ATYPICAL`,
   investigue o porquê.
3. Olhe **melhor_hit_descrição**, **identidade%/cobertura%** e **hit_coleoptera** —
   a que proteína conhecida se parece, e quão bem?
4. Considere **nível_evidência** e **domínios_InterPro** como reforço.
5. Registre **DECISÃO**, **ANOTAÇÃO FUNCIONAL** (o nome/função que você atribui) e
   uma **JUSTIFICATIVA** de uma frase. Preencha **CURADOR(A)** e **DATA**.

## 6. O que esperamos da sua análise

- **Consistência:** os mesmos critérios para todas as candidatas da sua família.
- **Rastreabilidade:** toda decisão com justificativa (nem que seja curta).
- **Honestidade intelectual:** "Incerta" é melhor que uma confirmação forçada.
- **Olhar biológico:** a anotação faz sentido para a biologia da praga?
  (quimiorrecepção = localizar hospedeiro; detoxificação = tolerar inseticidas;
  metabolismo = digestão). Ver a biologia das famílias no
  [guia de onboarding](guia_onboarding_bolsistas.md).
- **Dúvidas trazidas à reunião** — não travar sozinha; anotar e discutir.

## 7. Sugestão de divisão (as 3 famílias do piloto)

- **Catalase (5 candidatas)** — família muito conservada, hits fortes: ótima para
  "aquecer" e calibrar o olhar.
- **Alfa-amilase (5)** — atenção ao domínio GH13, que é inespecífico (risco de
  falso-positivo): bom exercício de rejeição criteriosa.
- **OBP (31)** — a mais numerosa e rica: onde a curadoria da incerteza mais
  aparece (família divergente). Boa para aprofundar.

## 8. Depois da curadoria

Devolver a planilha preenchida. Vamos consolidar as decisões, discutir as
"Incertas" em conjunto e usar o resultado curado como base para o relatório e a
divulgação (eventos/artigo). Cada rodada de curadoria também alimenta a melhoria
do próprio protocolo.
