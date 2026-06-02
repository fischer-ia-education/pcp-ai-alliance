# CLAUDE.md

Guia para o Claude Code trabalhar neste repositório. Leia antes de mexer.

## Visão Geral

**Aliança de IA para a Educação** — plataforma de conteúdo (site estático) sobre contratação pública responsável de IA na educação brasileira, em parceria com o **Instituto Jataí**. Conteúdo em Markdown (`conteudo/`), gerado por Python + Jinja2, publicado no **Netlify**. Todo o conteúdo é em **pt-BR**.

## Build, Preview e Geração — IMPORTANTE

**`uv` está instalado** (`~/.local/bin/uv`). Os scripts têm cabeçalho PEP 723, então o `uv` resolve as dependências sozinho — é o caminho preferido:

```bash
# Gerar o site → output/site/
uv run site/generate.py

# (Re)gerar os templates .docx editáveis (RIPD, Model Card) em assets/downloads/
uv run site/gerar_templates_docx.py

# Servir localmente para revisão (o usuário SEMPRE revisa no live server antes de push)
cd output/site && python3 -m http.server 8000   # http://localhost:8000
```

Se `uv` não estiver no PATH, use `~/.local/bin/uv` ou rode `source ~/.local/bin/env`. **Fallback sem uv** (venv do projeto, `.venv/` fora do git):
```bash
python3 -m venv .venv && .venv/bin/pip install markdown jinja2 pyyaml pygments python-docx
.venv/bin/python site/generate.py
```

> Regra do usuário: **nunca dar `git push` sem ele revisar no live server primeiro.** Branch/commit só quando ele pedir.

Para conferir UI mobile com fidelidade, **não** use `chrome --headless --window-size` (distorce o viewport e corta a imagem → falso "overflow"). Use o Chrome via DevTools Protocol com `Emulation.setDeviceMetricsOverride {width,height,deviceScaleFactor,mobile:true}` → `Page.captureScreenshot`. (Há uma memória do projeto com um cliente WS pronto em Python stdlib.)

## Arquitetura

### Pipeline de conteúdo
```
conteudo/[persona|secao]/*.md  →  site/generate.py  →  output/site/*.html
        (fonte)                   (Jinja2 templates)     (site estático)
```
- **Gerador**: `site/generate.py` — descobre `.md`, parseia frontmatter YAML, renderiza via Jinja2.
- **Templates**: `site/templates/` — `base.html`, `index.html` (home), `persona.html`, `persona_with_subpersonas.html`, `document.html`, `section_recursos.html`, `criterios.html`.
- **Assets**: `site/assets/style.css` + `script.js` (vanilla, sem build tools). `site/assets/downloads/` contém o PDF do guia e os `.docx` — copiados inteiros para o build via `shutil.copytree`.
- **Pandoc** (`build.sh`, `style.css` da raiz): caminho secundário p/ PDF/HTML, raramente usado.

### Navegação (estado V2/V3)
Menu = **2 personas + 3 seções**: `gestores`, `edtechs` (com 4 sub-estágios), e seções `recursos`, `contexto-politica`, `sobre-o-guia`. As pastas `educadores/`, `intermediarios/`, `legisladores/` existem em `conteudo/` mas **estão fora do menu** (conteúdo preservado). Tudo isso é definido nos dicts `PERSONAS`, `SUB_PERSONAS` e `SECTIONS` em `generate.py`.

### Critérios de Contratação (fonte única) — central na V3
Os **14 critérios** do Jataí (blocos ET/AP/CC) vivem em **um só lugar**: a lista `CRITERIOS` (+ `BLOCOS_CRITERIOS`) em `generate.py`. A partir dela:
- Renderiza-se a página interativa `recursos/criterios-contratacao.html` (template `criterios.html`): abas ET/AP/CC + acordeão acessível + deep-link por critério (`#et1`…`#cc6`).
- Injeta-se o "cardápio" em `gestores/durante-a-contratacao.md` via o marcador **`[[CRITERIOS_LAUNCHER]]`**, substituído em `_process_md` por `render_criterios_launcher()`. **Não duplicar conteúdo** — editar critério só em `CRITERIOS`.

### Downloads / Templates editáveis
- `DOWNLOADS` em `generate.py` mapeia `slug → {arquivo, rotulo}`. Em `_process_md`, o doc ganha `download`, e `document.html` mostra o botão "Baixar versão editável (Word)".
- Os `.docx` são gerados por `site/gerar_templates_docx.py` (usa `python-docx`), espelhando o conteúdo de `conteudo/recursos/ripd-simplificado.md` e `model-card-educacional.md` em formato preenchível. Saída em `site/assets/downloads/`.
- O **Guia completo (PDF, 9 MB)** fica em `site/assets/downloads/`; download oferecido **só na home** (hero + faixa de download). Foi removido da página de critérios e de Recursos por decisão (evitar repetição).

### Página de Revisão (documentação interna)
`REVISAO-PLATAFORMA.html` (raiz) é uma página standalone com **abas V2 / V3** (segmented control + JS inline) documentando cada rodada de mudanças e as **premissas** por trás (inclusive o que o Jataí sugeriu e NÃO foi feito). `generate.py` a copia para `output/site/revisao.html` (etapa 5b). O menu (`base.html`) aponta para `revisao.html` com o rótulo "· Revisão". Tem botão "Voltar para a plataforma".
> Ao concluir uma rodada de mudanças, **atualizar o painel correspondente** desta página (hoje V3) com o log e as premissas.

### Modelo de conteúdo
- Frontmatter YAML: `title`, `subtitle`, `author`, `date`, `persona`, `tipo`.
- `tipo` define categoria/ordem via `TIPO_PRIORIDADE` (comece / aprofunde / complementar). Inferido pelo nome do arquivo se ausente.
- Metadados de persona (cor, ícone, pergunta) ficam em `generate.py`, não no conteúdo.

## Estado atual / onde paramos (jun/2026)
- **V3 implementada localmente** e validada por screenshot (desktop + mobile). **Ainda não commitada/enviada.**
- Pendências registradas na aba V3 de `revisao.html`: versão resumida do Guia (~10 págs, em design pelo Jataí — card "em breve"); avaliar mais templates Word (AP1–AP3); avaliar critérios na home (opção 1, descartada por ora); revisão página-a-página.

## Deploy
Netlify, config em `netlify.toml` (raiz): `publish = "output/site"`. Redirects de `/sobre` → `/sobre-o-guia/`.
