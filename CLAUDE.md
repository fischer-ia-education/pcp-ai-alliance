# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Aliança de IA para a Educação — a persona-driven educational content platform about responsible AI procurement in Brazilian public education. Content is authored in Markdown inside the `conteudo/` directory and published as a static site via Netlify.

Five personas: **edtechs**, **gestores**, **intermediarios**, **legisladores**, **educadores**. EdTechs has sub-personas by maturity stage (estagio-inicial, entrada-setor-publico, escala, internacional).

All content is in Brazilian Portuguese (pt-BR).

## Build & Development Commands

All commands run from `.`:

```bash
# Static site generation (primary workflow)
uv run site/generate.py              # Build to output/site/
uv run site/generate.py --serve      # Build + serve on localhost:8000
uv run site/generate.py --watch      # Build + serve + auto-rebuild on changes

# PDF/HTML via Pandoc (secondary)
./build.sh                           # All personas → output/html/ and output/pdf/
./build.sh --html                    # HTML only
./build.sh gestores                  # Specific persona
```

Python dependencies (managed via PEP 723 inline metadata, resolved by `uv`): markdown, jinja2, pyyaml, pygments.

System dependencies for build.sh: pandoc (required), weasyprint or xelatex (for PDF).

## Architecture

### Content Pipeline

```
conteudo/[persona]/*.md  →  site/generate.py  →  output/site/*.html
     (source)             (Jinja2 templates)     (static site)
```

- **Source of truth**: Markdown files with YAML frontmatter (`title`, `subtitle`, `persona`, `tipo`)
- **Generator**: `site/generate.py` — discovers `.md` files, parses frontmatter, renders via Jinja2
- **Templates**: `site/templates/` — base.html, index.html, persona.html, persona_with_subpersonas.html, document.html, section_recursos.html
- **Assets**: `site/assets/style.css` and `script.js` — vanilla CSS/JS, no build tools
- **Pandoc CSS**: `./style.css` (root) — used by `build.sh` for HTML/PDF output, separate from the site assets

### Content Model

Materials are categorized by `tipo` (type) with priority ordering defined in `TIPO_PRIORIDADE` in generate.py:
- **comece** (entry): one-pager, template
- **aprofunde** (deep): guia, checklist, faq, framework, policy-brief
- **complementar** (extra): guia-complementar

The `tipo` is inferred from the filename prefix if not set in frontmatter (e.g., `guia-gestores.md` → tipo: guia).

### Frontmatter Format

```yaml
---
title: "Document Title"
subtitle: "Optional subtitle"
author: "Aliança de IA para a Educação"
date: "2026"
persona: edtechs
tipo: one-pager
---
```

### Key Design Decisions

- Persona metadata (color, icon, description) is defined in `PERSONAS` dict in generate.py, not in content files
- Sub-personas only exist for edtechs; the template `persona_with_subpersonas.html` handles this special case
- The `recursos/` section is cross-cutting (not tied to a single persona) and uses its own template
- No JavaScript framework — vanilla JS for TOC scroll-spy, mobile menu, and external link handling
- CSS uses custom properties with a "Editorial Brasileira" aesthetic (Source Serif 4 for headings, DM Sans for body)

## Deployment

Static site deployed to Netlify. Config at `materiais/.netlify/netlify.toml`. Build output is `materiais/output/site/`.
