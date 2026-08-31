# Notas de leitura integral — pontos principais por estudo

Referência para extração na matriz PRISMA e na Tabela de síntese do manuscrito.

---

## Arif et al. (2023) — Driving drowsiness detection

**DOI:** 10.3389/fphys.2023.1153268

### O que observar

| Dimensão | Ponto principal |
|----------|-----------------|
| **Estado mental / ground truth** | Sonolência ao volante (*driving drowsiness*) vs. alerta; rotulagem pós-hoc por vídeo facial, desempenho na faixa e respostas físicas |
| **População** | $n=12$, homens saudáveis, destros, $30 \pm 2$ anos, $\geq 2$ anos de experiência de condução |
| **Setup experimental** | Simulador veicular; privação de sono; coleta ~03h00; ambiente escuro/silencioso; *lane-keeping* por $30 \pm 2$ min |
| **Aquisição EEG** | OpenBCI Ultracortex Mark-IV; referencial (orelhas); 16 canais @ 125 Hz; **6 canais analíticos:** Fp1, Fp2, F7, F8, O1, O2 |
| **Biomarcador** | Potência espectral (Welch) em $\delta$, $\theta$, $\alpha$, $\beta$; janelas de 10 s; razões $R_1$–$R_4$; espectrogramas contínuos |
| **Hipótese fisiológica** | Transição alerta→sonolência = queda de $\beta$ + aumento de $\alpha$, $\theta$, $\delta$; assimetria hemisférica direita |
| **COI (canal de interesse)** | **F8** (frontal direito) — melhor separação alerta/sonolência com um único eletrodo |
| **Classificação** | 7 famílias comparadas **por canal**; melhor: *Ensemble Bagged Trees* no F8 (Acc 85,6%; Recall 89,7%; F1 87,6%; AUC 0,91; 76 ms) |
| **Validação estatística** | ANOVA bidirecional entre canais ($p<0{,}05$); $t$ pareado F8 vs. demais com Bonferroni ($p<0{,}01$) |
| **Relevância para o review** | *Pipeline* espectral completo e reprodutível; modelo de reportagem de setup + COI + razões espectrais; contrapõe concentração sensorimotora (C3/C4/Cz) de revisões BCI motor |

### Campos da matriz a preencher

Canais_EEG, Biomarcador_Quantitativo, Construcao_Biomarcador (janela 10 s, Welch, razões), Validacao, Ground_Truth, Dominio_Aplicacao (Neuroergonomia), Aspectos_IHC (detecção precoce, baixa intrusividade).

---

## Rutkowski et al. (2023) — Dementia neurobiomarker (network topology)

**DOI:** 10.3389/fnhum.2023.1155194

### O que observar

| Dimensão | Ponto principal |
|----------|-----------------|
| **Estado mental / ground truth** | CCL (*mild cognitive impairment*, MoCA $\leq 25$) vs. envelhecimento cognitivo saudável |
| **População** | $n=27$ idosos na Polônia ($70{,}76 \pm 5{,}34$ anos); 1 homem, 26 mulheres; desbalanceamento de classes |
| **Paradigma pBCI** | Três tarefas cognitivas passivas: (1) aprendizagem de emoções faciais; (2) avaliação de emoções; (3) *oddball* com imagens reminiscentes |
| **Aquisição EEG** | Unicorn headset (g.tec); artefatos oculares/musculares removidos por pipeline do grupo |
| **Biomarcador** | **Topologia de rede** (OPN — *ordinal partition networks*): contagem de nós e arestas por canal EEG |
| **Construção** | Grafos de transição de estados a partir de séries temporais; UMAP para redução dimensional |
| **Classificação** | LOOS-CV (*leave-one-subject-out*): LR, LDA, linear SVM, RF, DFNN; acurácias 82–95% conforme tarefa |
| **Achado central** | CCL apresenta **menos** nós/arestas que cognição saudável (menor complexidade/microestados) |
| **Limitações** | Piloto; $n$ pequeno; classes desbalanceadas; validação clínica (PET, LCR, MRI) ausente |
| **Relevância para o review** | Biomarcador de **conectividade/topologia** (não espectral); pBCI clínico domiciliar; translação pedagogia/reabilitação cognitiva |

### Campos da matriz a preencher

Biomarcador_Quantitativo (topologia OPN), Validacao (LOOS-CV), Ground_Truth (MoCA), Dominio_Aplicacao (Clínico), Transferibilidade (monitoramento domiciliar).

---

## Boas et al. (2020) — GLM for fNIRS single-trial (perspectiva)

**DOI:** 10.3389/fnhum.2020.00030

### O que observar

| Dimensão | Ponto principal |
|----------|-----------------|
| **Tipo de publicação** | Hipótese/teoria; **não é estudo empírico pBCI-EEG** — candidato a exclusão no escopo EEG-centrado |
| **Modalidade** | fNIRS contínuo (CW); sistema CW7 (TechEn); 48 canais longa separação + 8 SS (~8 mm); 50 Hz |
| **Problema metodológico** | Pré-processamento fNIRS em BCI ignora GLM; limpeza global fora da CV causa **data leakage** e overfitting |
| **Solução proposta** | GLM + regressores de curta separação (SS) **dentro** de cada *fold* da validação cruzada |
| **Feature nova** | Peso $\beta$ da HRF individual por canal (em vez de potência/bruto filtrado) |
| **Resultado simulado** | +7,4% acurácia média vs. pipeline convencional; melhor separabilidade de *features* |
| **Relevância para o review** | Lição transferível: validação cruzada aninhada, pré-processamento dentro do *fold*, distinção sinal neural vs. ruído sistemático — **analogia** para EEG espectral, não inclusão como estudo empírico do corpus |

### Decisão de elegibilidade pendente

Manter como referência metodológica na Discussão ou excluir na leitura integral por critério E3 (fNIRS sem EEG).

---

## Escopo deliberadamente adiado

A comparação sistemática de **todas** as arquiteturas de ML (7 famílias no Arif, 5 no Rutkowski, etc.) em tabela unificada é **trabalho futuro** após extração completa dos 13 estudos. Nesta fase, priorizar: setup → biomarcador → validação → métrica principal.
