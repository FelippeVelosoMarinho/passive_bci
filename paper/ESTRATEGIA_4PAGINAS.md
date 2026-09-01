# Estratégia SBC/CBEB — limite de 4 páginas

## Posso quebrar o formato?

**Para submissão:** não. O template SBC (A4, coluna única, Times 12 pt, margens fixas, abstract/resumo ≤10 linhas na 1ª página) e o limite de páginas são exigências da conferência. Extrapolar tende a reprovação na mesa ou truncamento editorial.

**O que é permitido:**

| Entrega | Onde | Conteúdo |
|---------|------|----------|
| **Artigo SBC (≤4 p.)** | Anais CBEB | Contribuição + métodos compactos + 2 eixos de discussão |
| **Material suplementar** | Repositório / site / “disponível mediante solicitação” | Matriz PRISMA, fluxograma completo, string de busca, notebook |
| **Relatório completo** | `rascunho.tex` (versão longa) | Revisão de escopo integral, tabelas, 13 estudos |

Isso **não** quebra PRISMA: scoping reviews publicadas em formato curto frequentemente remetem protocolo e dados completos como suplemento (como o CBEB remete string de busca “on request”).

---

## Orçamento de páginas (meta 4)

| Seção | Páginas | O que entra |
|-------|---------|-------------|
| Título + abstract + resumo | ~0,4 | ≤10 linhas cada |
| Introdução | ~0,6 | 2–3 parágrafos: pBCI → lacuna Aricò/Haufe → objetivo |
| Métodos | ~0,7 | **Um bloco** PRISMA + I/E inline + corpus vs R2/R3 (1 frase) |
| Resultados | ~0,5 | Números PRISMA + figura pequena + 2 frases (Arif, Rutkowski) |
| Discussão | ~1,0 | **Só os 2 eixos:** interpretabilidade + protocolo COI |
| Referências | ~0,8 | ~12–18 citações (cortar redundantes) |

**Cortar do artigo curto:** subseções múltiplas em Métodos; parágrafo longo Arif em Resultados; Boas (fNIRS); Tabela de características; `table*` de síntese; 3ª subseção de Discussão genérica.

**Manter obrigatoriamente:** Haufe preenche lacuna de Aricò; protocolo F8/COI transferível; números PRISMA (86→82→13).

---

## Arquivos

- `rascunho.tex` — versão longa (trabalho contínuo da revisão)
- `rascunho_sbc4p.tex` — versão alvo CBEB (compilar e medir páginas)

```bash
cd paper && pdflatex rascunho_sbc4p && bibtex rascunho_sbc4p && pdflatex rascunho_sbc4p
```

Se ainda passar de 4 páginas: reduzir bibliografia, figura menor, Methods ainda mais curto.

---

## Framing honesto para o CBEB

Posicionar como **“revisão de escopo preliminar / contribuição metodológica”**, não como síntese fechada dos 13 estudos. Frases úteis:

- “Treze estudos pré-selecionados; leitura integral em andamento.”
- “Detalhes tabulares na matriz suplementar.”
- “Dois eixos analíticos emergentes da síntese parcial…”

Isso é compatível com PRISMA-ScR em formato curto e evita prometer tabela completa estilo CBEB-FES (82 estudos) em 4 páginas.
