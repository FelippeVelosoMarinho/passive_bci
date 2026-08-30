# Rascunho LaTeX — Revisão de Escopo pBCI

## Arquivos

| Arquivo | Descrição |
|---------|-----------|
| `rascunho.tex` | Manuscrito principal (SBC) |
| `referencias.bib` | Bibliografia inicial |

## Compilação

Requer o pacote **sbc-template** (SBC). Exemplo:

```bash
cd paper
pdflatex rascunho
bibtex rascunho
pdflatex rascunho
pdflatex rascunho
```

Se `sbc-template` não estiver instalado, baixe em:
https://www.sbc.org.br/documentos-da-sbc/summary/169-templates-para-artigos-e-capas-de-livros/878-template-sbc

## Próximos passos

1. Preencher Tabela III com os 13 estudos de `Matriz_Mapeamento_PRISMA.xlsx`
2. Gerar Fig. 1 (fluxograma PRISMA) a partir dos números do notebook
3. Completar leitura integral e revisar pré-seleções
4. Adicionar coautores e agradecimentos (CAPES etc.)
5. Expandir Discussão após extração completa
