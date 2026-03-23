# Como Editar os Materiais

Este guia é para quem quer criar ou editar conteúdo. Você só precisa saber editar texto — não precisa entender de programação.

## Onde estão os arquivos

Cada persona tem sua própria pasta dentro de `conteudo/`:

```
conteudo/
├── edtechs/           ← Empreendedores de tecnologia educacional
├── gestores/          ← Secretários e equipes de redes públicas
├── intermediarios/    ← Institutos, fundações, universidades
├── legisladores/      ← Parlamentares e formuladores de políticas
├── educadores/        ← Professores e coordenadores pedagógicos
└── recursos/          ← Materiais transversais (não ligados a uma persona)
```

A persona **edtechs** também tem subpastas por estágio de maturidade:
`estagio-inicial/`, `entrada-setor-publico/`, `escala/`, `internacional/`.

## Estrutura de um arquivo

Cada arquivo `.md` (Markdown) tem duas partes:

### 1. Cabeçalho (frontmatter)

No início do arquivo, entre `---`, ficam os metadados:

```yaml
---
title: "Título do Documento"
subtitle: "Subtítulo opcional"
author: "Aliança de IA para a Educação"
date: "2026"
persona: gestores
tipo: guia
---
```

**Campos importantes:**

| Campo | O que é | Obrigatório? |
|-------|---------|:---:|
| `title` | Título que aparece no site | Sim |
| `subtitle` | Subtítulo (aparece abaixo do título) | Não |
| `persona` | A qual persona pertence (`edtechs`, `gestores`, `intermediarios`, `legisladores`, `educadores`) | Sim |
| `tipo` | Tipo do material (veja tabela abaixo) | Não* |

*Se `tipo` não for informado, ele é inferido pelo prefixo do nome do arquivo (ex: `guia-gestores.md` → tipo `guia`).

**Valores válidos para `tipo`:**

| Tipo | Categoria | Aparece como |
|------|-----------|-------------|
| `one-pager` | Comece | Resumo Executivo |
| `template` | Comece | Template |
| `guia` | Aprofunde | Guia Completo |
| `checklist` | Aprofunde | Checklist |
| `faq` | Aprofunde | FAQ |
| `framework` | Aprofunde | Framework de Decisão |
| `policy-brief` | Aprofunde | Policy Brief |
| `guia-complementar` | Complementar | Material Complementar |

### 2. Corpo do texto

Após o cabeçalho, escreva o conteúdo usando Markdown:

```markdown
# Título principal

Parágrafo de texto normal.

## Seção

- Item de lista
- Outro item

> Citação em destaque

**Texto em negrito** e *texto em itálico*.
```

## Como adicionar um novo material

1. Escolha a pasta da persona (ex: `conteudo/gestores/`)
2. Crie um arquivo `.md` com nome descritivo (ex: `guia-novo-tema.md`)
3. Copie o cabeçalho de um arquivo existente e ajuste os campos
4. Escreva o conteúdo abaixo do cabeçalho
5. O site será atualizado automaticamente no próximo build

## O que NÃO editar

Tudo que está **fora** da pasta `conteudo/` é código do sistema. Não edite:
- `site/` (gerador do site)
- `build.sh` (script de build)
- `style.css` (estilos do PDF)
- `output/` (arquivos gerados — serão sobrescritos)

Em caso de dúvida, pergunte à equipe técnica.
