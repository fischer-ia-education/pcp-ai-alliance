---
title: "Materiais por Persona: Contratação Pública de IA na Educação"
author: "Aliança de IA para a Educação"
date: "2026"
---

# Materiais por Persona: Contratação Pública de IA na Educação

Estes materiais são derivados da publicação **"Contratação Pública de Soluções de IA na Educação"**, iniciativa da [Aliança de IA para a Educação](http://iaparaeducacao.org.br), desenvolvida em parceria com o **Instituto Jataí**.

A publicação original é um instrumento abrangente que cobre desde conceitos de IA na educação até um guia prático de contratação responsável. Os materiais abaixo reorganizam e reenquadram esse conteúdo para **5 personas estratégicas**, oferecendo a cada público um caminho direto ao que é mais relevante para sua atuação.

---

## Navegação por Persona

### EdTechs (Empreendedores)

*Perspectiva: "Como vendo IA de forma responsável para o setor público?"*

| Material | Descrição | Tempo de leitura |
|----------|-----------|-----------------|
| [Guia de Modalidades de Contratação](edtechs/guia-modalidades-contratacao.md) | Pregão, registro de preço, inexigibilidade, dispensa, CPSI e ETEC — guia prático | ~20 min |
| [Checklist de Prontidão](edtechs/checklist-edtechs.md) | 35+ itens para verificar antes de abordar redes públicas | ~10 min |
| [Perguntas Frequentes](edtechs/faq-edtechs.md) | 16 respostas sobre mercado, requisitos, processo de venda e riscos | ~15 min |
| [Resumo Executivo](edtechs/one-pager-edtechs.md) | Visão geral em 1 página: cenário, oportunidade, 5 ações imediatas | ~3 min |
| [Guia para EdTechs Internacionais](edtechs/internacional/guia-internacionais.md) | Para empresas estrangeiras: presença jurídica, LGPD internacional, adaptação cultural, tributação | ~15 min |

---

### Gestores Públicos

*Perspectiva: "Como compro IA com segurança e intencionalidade pedagógica?"*

| Material | Descrição | Tempo de leitura |
|----------|-----------|-----------------|
| [Guia Completo](gestores/guia-gestores.md) | Da compreensão de IA ao guia antes/durante/após contratação | ~25 min |
| [Checklist da Jornada](gestores/checklist-gestores.md) | Itens acionáveis por fase: antes, durante e após a contratação | ~10 min |
| [Framework de Decisão](gestores/framework-decisao-gestores.md) | Árvore de decisão, matriz de risco, comparativo de modalidades, RACI | ~15 min |
| [Resumo Executivo](gestores/one-pager-gestores.md) | Visão geral em 1 página: problema, riscos, solução, próximos passos | ~3 min |

---

### Organizações Intermediárias

*Perspectiva: "Como facilitar contratações de IA mais responsáveis?"*

| Material | Descrição | Tempo de leitura |
|----------|-----------|-----------------|
| [Guia Completo](intermediarios/guia-intermediarios.md) | Modelos de intermediação, critérios de curadoria, letramento algorítmico | ~15 min |
| [Resumo Executivo](intermediarios/one-pager-intermediarios.md) | Oportunidade de atuação, 3 modelos, checklist de curadoria | ~3 min |

---

### Legisladores e Formuladores de Políticas

*Perspectiva: "Que marcos regulatórios e incentivos são necessários?"*

| Material | Descrição | Tempo de leitura |
|----------|-----------|-----------------|
| [Policy Brief](legisladores/policy-brief-legisladores.md) | Lacunas regulatórias, benchmarks internacionais, 7 recomendações | ~15 min |
| [Resumo Executivo](legisladores/one-pager-legisladores.md) | Problema, 5 recomendações, dados de impacto | ~3 min |

---

### Educadores (Professores e Coordenadores)

*Perspectiva: "Como uso e supervisiono IA no dia a dia da escola?"*

| Material | Descrição | Tempo de leitura |
|----------|-----------|-----------------|
| [Guia Prático](educadores/guia-educadores.md) | O que é IA, como ajuda, riscos, supervisão humana, perguntas essenciais | ~15 min |
| [Resumo Executivo](educadores/one-pager-educadores.md) | 5 benefícios, 5 alertas, 3 perguntas para a coordenação | ~3 min |

---

## Sobre a Publicação Original

A publicação **"Contratação Pública de Soluções de IA na Educação"** é resultante de pesquisa realizada entre novembro e dezembro de 2025, envolvendo:
- Mapeamento e revisão de literatura nacional e internacional sobre IA na educação
- Pesquisa documental de contratações públicas realizadas entre 2024 e fevereiro de 2026
- 11 entrevistas com gestores públicos, especialistas jurídicos, provedores de soluções e especialistas em IA

## Geração de PDF e HTML

Para gerar versões em PDF e HTML dos materiais:

```bash
# Instalar dependências
# pandoc: sudo pacman -S pandoc (Arch) / sudo apt install pandoc (Debian/Ubuntu)
# weasyprint: pip install weasyprint (para PDF via HTML)

# Gerar todos os materiais
./build.sh

# Gerar apenas HTML
./build.sh --html

# Gerar materiais de uma persona específica
./build.sh gestores
./build.sh edtechs
```

Os arquivos gerados ficam em `output/html/` e `output/pdf/`.

---

## Créditos

- **Publicação original:** Aliança de IA para a Educação, em parceria com o Instituto Jataí
- **Materiais derivados:** Gerados a partir da publicação original com reorganização por persona e enquadramento de perspectiva

---

*Aliança de IA para a Educação | 2026*
