# Notas de leitura integral — pontos principais por estudo

Referência para extração na matriz PRISMA e na Tabela de síntese do manuscrito.

---

## Literatura de referência (fora da busca)

Estudos **não** entram no fluxograma PRISMA nem na Tabela de síntese empírica.

| ID | Obra | Papel | Como citar no manuscrito |
|----|------|-------|---------------------------|
| **R1** | Aricò et al. (2017) | Revisão narrativa seed | Eixos neurometrics / ML / calibração; incluído no corpus **porque** foi recuperado pela busca (está nos 13 pré-incluídos), mas também orientou o escopo |
| **R2** | Haufe et al. (2014) | Referência conceitual | Critério de interpretabilidade (forward vs backward); Discussão e classificação analítica; **nunca** conta como estudo incluído |
| **R3** | Faria et al. (2026) | Precedente metodológico | `@unpublished`; adaptação PRISMA-ScR, formulário, benchmark C3/C4/Cz; **não** recuperado pela busca (BCI-FES ativo) |

Frase-modelo (Methods): «Distinguimos o corpus primário (registros identificados pela busca) da literatura de referência (R1--R3), utilizada para delineamento metodológico e discussão interpretativa, sem integração às contagens do fluxograma PRISMA.»

---

## Arif et al. (2023) — Driving drowsiness detection

**DOI:** 10.3389/fphys.2023.1153268

Estado mental: sonolência vs. alerta. Setup: simulador, privação de sono, ~03h00, lane-keeping 30 min. EEG: OpenBCI Ultracortex Mark-IV; 16 ch @ 125 Hz; análise em Fp1, Fp2, F7, F8, O1, O2. Biomarcador: PSD Welch; razões R1–R4; COI = **F8**. ML: 7 famílias; melhor Ensemble Bagged Trees (AUC 0,91). Validação: ANOVA + t pareado Bonferroni.

---

## Rutkowski et al. (2023) — Dementia neurobiomarker

**DOI:** 10.3389/fnhum.2023.1155194

Estado mental: CCL (MoCA ≤ 25) vs. cognição saudável. n=27 idosos. Biomarcador: topologia OPN (nós/arestas). Validação: LOOS-CV. Domínio: clínico domiciliar.

---

## Boas et al. (2020) — GLM fNIRS (perspectiva)

**DOI:** 10.3389/fnhum.2020.00030

Fora do escopo EEG empírico. Lição: GLM+SS dentro da CV; evitar data leakage. Usar na Discussão ou excluir por E3.

---

## Escopo adiado

Comparação sistemática de todas as arquiteturas ML após extração completa dos 13 estudos.
