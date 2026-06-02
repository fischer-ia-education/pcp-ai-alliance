---
title: "Contratação Pública de IA na Educação — Plataforma"
author: "Aliança de IA para a Educação"
date: "2026"
---

# Contratação Pública de Soluções de IA na Educação

Site estático da **[Aliança de IA para a Educação](http://iaparaeducacao.org.br)** (Fundação Lemann, Telles Foundation e VélezReyes+), em parceria com o **Instituto Jataí**, sobre contratação pública responsável de IA na educação brasileira. Conteúdo derivado da publicação *"Contratação Pública de Soluções de IA na Educação"* (pesquisa nov–dez 2025: literatura, análise PNCP 2024–2026 e 11 entrevistas).

> Para detalhes técnicos de arquitetura e do fluxo de trabalho, veja **[CLAUDE.md](CLAUDE.md)**.

## Como rodar (build + preview)

Com **`uv`** (recomendado — resolve as dependências via PEP 723):

```bash
uv run site/generate.py                  # gera o site em output/site/
uv run site/gerar_templates_docx.py      # regera os templates Word (.docx)
cd output/site && python3 -m http.server 8000   # preview em http://localhost:8000
```

Sem `uv`, use o venv do projeto:
```bash
python3 -m venv .venv && .venv/bin/pip install markdown jinja2 pyyaml pygments python-docx
.venv/bin/python site/generate.py
```

## Estrutura

- **`conteudo/`** — todo o conteúdo editável em Markdown. Guia de edição em [`conteudo/COMO-EDITAR.md`](conteudo/COMO-EDITAR.md).
- **`site/generate.py`** — gerador estático (descobre `.md`, aplica templates Jinja2).
- **`site/templates/`**, **`site/assets/`** — templates e CSS/JS.
- **`site/assets/downloads/`** — Guia completo (PDF) e templates editáveis (`.docx`).
- **`REVISAO-PLATAFORMA.html`** — documentação interna das rodadas de revisão (abas V2/V3), publicada como `revisao.html`.

## Navegação (atual)

Menu com **2 personas + 3 seções**:

| Entrada | Tipo | Conteúdo |
|---------|------|----------|
| **Gestores Públicos** | Persona | Usos em potencial · Antes / Durante / Após a contratação · Guia · Checklist · Framework |
| **EdTechs** | Persona | 5 Perguntas · Modalidades · Checklist · Guia + 4 sub-estágios (Inicial, Entrada, Escala, Internacional) |
| **Recursos** | Seção | Critérios de Contratação (interativo) · Glossário · Model Card e RIPD (com download Word) |
| **Contexto e Política** | Seção | Como as redes contratam · Desafios · Boas práticas internacionais · Documentos oficiais · Policy Brief |
| **Sobre o Guia** | Seção | Apresentação · Metodologia |

As pastas `educadores/`, `intermediarios/` e `legisladores/` permanecem em `conteudo/` mas estão fora do menu principal.

## Destaques da plataforma

- **Critérios de Contratação de IA** — 14 critérios (ET/AP/CC) numa página interativa (abas + acordeão), fonte única no gerador. Também embutidos como "cardápio" na página *Durante a Contratação*.
- **Templates editáveis (Word)** — RIPD Simplificado e Model Card Educacional para baixar e preencher, espelhando as orientações do site.
- **Guia completo (PDF)** — download na home.

## Deploy

Netlify — `netlify.toml`: `publish = "output/site"`.

## Créditos

Publicação original: Aliança de IA para a Educação, em parceria com o Instituto Jataí. Materiais derivados reorganizados por persona.

*Aliança de IA para a Educação · Instituto Jataí · 2026*
