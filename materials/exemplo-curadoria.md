# Exemplo resolvido de curadoria (demonstração)

> Acompanha o [protocolo de curadoria](protocolo_curadoria.md) e a planilha
> `curation_pilot/planilha_curadoria_piloto.xlsx`. Aqui, quatro casos reais são
> curados como **demonstração** — mostrando o raciocínio e a decisão. Use como
> modelo; as decisões finais de cada candidata são suas.

Os quatro casos foram escolhidos por cobrirem situações diferentes: uma
confirmação fácil, uma descoberta forte, uma incerteza por divergência e uma
incerteza por baixa confiança.

---

## Caso 1 — CSOR_00176 · Catalase · nível A (confirmação fácil)

**Evidência:** domínio `PF00199` (catalase); 478 aa (faixa esperada 450–550);
melhor hit *catalase-like [Sitophilus oryzae]*, 77% identidade; `is_coleoptera_hit
= True`; nível de evidência **A**.

**Raciocínio:** domínio diagnóstico presente, tamanho perfeito, alta identidade a
uma catalase de gorgulho (parente próximo), concordância InterPro (nível A). Não
há sinal de alerta.

| DECISÃO | ANOTAÇÃO FUNCIONAL | JUSTIFICATIVA |
|---|---|---|
| **Confirmada** | Catalase | Domínio PF00199, tamanho na faixa, 77% id a catalase de *S. oryzae*, nível A. |

---

## Caso 2 — CSOR_08391 · Alfa-amilase · proveniência "similaridade" (descoberta forte)

**Evidência:** **sem** o domínio diagnóstico PF00128, mas **com** o de apoio
`PF02806` (Alpha-amylase_C); 485 aa (faixa esperada 400–550); melhor hit
*alpha-amylase-like [Sitophilus oryzae]*, **81% identidade**, cobertura 99%.

**Raciocínio:** foi descoberta por similaridade (não passou pela seleção por
domínio, porque o domínio catalítico ficou abaixo do limiar). Mas: tem o domínio
de apoio da família, tamanho certo e **81% de identidade** a uma alfa-amilase de
gorgulho. É quase certamente uma alfa-amilase real cujo PF00128 divergiu.

| DECISÃO | ANOTAÇÃO FUNCIONAL | JUSTIFICATIVA |
|---|---|---|
| **Confirmada** | Alfa-amilase | Sem PF00128 mas com PF02806; 485 aa; 81% id a alpha-amylase de *S. oryzae*. Domínio catalítico provavelmente sub-limiar. |

---

## Caso 3 — CSOR_07687 · OBP · proveniência "similaridade" (incerteza por divergência)

**Evidência:** **sem** qualquer domínio Pfam; apenas 77 aa; melhor hit *general
odorant-binding protein 71 [Anoplophora glabripennis]*, **41% identidade**,
cobertura 97%.

**Raciocínio:** proteína curta, divergente, sem domínio — exatamente o perfil de
OBP que a busca por domínio perde. A semelhança (41%, cobertura alta) a uma OBP de
besouro é sugestiva, mas 41% é moderado e não há domínio para confirmar. **Não
force**: registre como incerta e leve para discussão (pode valer conferir se tem
o padrão de cisteínas típico das OBPs).

| DECISÃO | ANOTAÇÃO FUNCIONAL | JUSTIFICATIVA |
|---|---|---|
| **Incerta** | (provável OBP — a confirmar) | 41% id a OBP de besouro, cobertura alta, mas sem domínio; curta. Verificar padrão de cisteínas; discutir na reunião. |

---

## Caso 4 — CSOR_10506 · Alfa-amilase · proveniência "similaridade" (baixa confiança)

**Evidência:** sem domínio; 201 aa (bem abaixo dos ~400–550 de uma amilase
completa); melhor hit *alpha-amylase 4-like [Sitophilus oryzae]*, **31%
identidade**, cobertura 92%.

**Raciocínio:** identidade baixa (31%) e tamanho pequeno demais para uma
alfa-amilase digestiva completa. Pode ser um fragmento, uma GH13 aparentada
(maltase/glucosidase) ou um falso positivo. Sinais de alerta suficientes para
**não confirmar**; incerta é o mais honesto (foi, aliás, um dos casos que o
DIAMOND não recuperou — os mais divergentes).

| DECISÃO | ANOTAÇÃO FUNCIONAL | JUSTIFICATIVA |
|---|---|---|
| **Incerta** | (indefinida) | 31% id e apenas 201 aa (curto p/ amilase completa); possível fragmento ou GH13 aparentada. Não há evidência suficiente para confirmar. |

---

## O que esses exemplos ensinam

- **Nível A + parente próximo** → confirmação direta (Caso 1).
- **Descoberta sem domínio diagnóstico pode ser membro real** se tiver domínio de
  apoio, tamanho e identidade coerentes (Caso 2).
- **Identidade moderada + sem domínio** → incerta, verificar características da
  família (Caso 3).
- **Identidade baixa + tamanho atípico** → incerta/rejeitar; não superestimar
  (Caso 4).

A curadoria não é sobre "confirmar tudo": é sobre **graduar a confiança com
honestidade** e sinalizar o que precisa de um segundo olhar.
