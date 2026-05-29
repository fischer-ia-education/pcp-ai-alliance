# /// script
# requires-python = ">=3.11"
# dependencies = ["markdown", "jinja2", "pyyaml", "pygments"]
# ///
"""
Gerador de site estático para os materiais da Aliança de IA para a Educação.

Uso:
    uv run site/generate.py              # Gera site em output/site/
    uv run site/generate.py --serve      # Gera + serve em localhost:8000
    uv run site/generate.py --watch      # Gera + recarrega em mudanças
"""

import argparse
import http.server
import os
import re
import shutil
import socketserver
import threading
import time
from pathlib import Path

import markdown
import yaml
from jinja2 import Environment, FileSystemLoader

# ── Diretórios ────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent  # materiais/
CONTENT_DIR = BASE_DIR / "conteudo"                 # materiais/conteudo/
SITE_DIR = Path(__file__).resolve().parent          # materiais/site/
TEMPLATE_DIR = SITE_DIR / "templates"
ASSETS_DIR = SITE_DIR / "assets"
OUTPUT_DIR = BASE_DIR / "output" / "site"

# ── Personas ──────────────────────────────────────────────────
PERSONAS = {
    "gestores": {
        "nome": "Gestores Públicos",
        "cor": "#2f855a",
        "pergunta": "Como contratar IA com segurança e intencionalidade pedagógica?",
        "descricao": "Secretários e equipes de redes públicas de educação",
        "icone": '<svg viewBox="0 0 32 32" width="32" height="32" xmlns="http://www.w3.org/2000/svg" aria-hidden="true"><rect x="2" y="5" width="22" height="9" fill="#A725FF"/><rect x="8" y="18" width="22" height="9" fill="#BBD634"/></svg>',
    },
    "edtechs": {
        "nome": "EdTechs",
        "cor": "#2b6cb0",
        "pergunta": "Como oferecer IA de forma responsável para o setor público?",
        "descricao": "Empreendedores e equipes de tecnologia educacional",
        "icone": '<svg viewBox="0 0 32 32" width="32" height="32" xmlns="http://www.w3.org/2000/svg" aria-hidden="true"><rect x="2" y="10" width="22" height="15" fill="#A725FF"/><polygon points="18,3 30,3 30,14" fill="#BBD634"/></svg>',
    },
}

# ── Sub-personas ──────────────────────────────────────────────
SUB_PERSONAS = {
    "edtechs": {
        "estagio-inicial": {
            "nome": "Estágio Inicial",
            "icone": '<svg viewBox="0 0 32 32" width="32" height="32" xmlns="http://www.w3.org/2000/svg" aria-hidden="true"><polygon points="16,3 30,27 2,27" fill="#A725FF"/><rect x="12" y="15" width="8" height="12" fill="#BBD634"/></svg>',
            "pergunta": "Como construo meu produto para ser contratável pelo setor público desde o início?",
            "descricao": "Tenho um produto em desenvolvimento ou MVP e quero entender como entrar no setor público.",
        },
        "entrada-setor-publico": {
            "nome": "Entrada no Setor Público",
            "icone": '<svg viewBox="0 0 32 32" width="32" height="32" xmlns="http://www.w3.org/2000/svg" aria-hidden="true"><rect x="3" y="14" width="26" height="15" fill="#A725FF"/><polygon points="1,14 16,3 31,14" fill="#BBD634"/></svg>',
            "pergunta": "O que preciso adaptar no meu produto, na minha documentação e no meu modelo de negócio?",
            "descricao": "Tenho produto consolidado no setor privado e quero vender para redes públicas.",
        },
        "escala": {
            "nome": "Escala",
            "icone": '<svg viewBox="0 0 32 32" width="32" height="32" xmlns="http://www.w3.org/2000/svg" aria-hidden="true"><rect x="2" y="18" width="10" height="11" fill="#BBD634"/><rect x="12" y="12" width="10" height="17" fill="#A725FF"/><rect x="22" y="6" width="8" height="23" fill="#BBD634"/></svg>',
            "pergunta": "Como escalo minha presença no setor público sem perder qualidade e sem criar dependência?",
            "descricao": "Já vendo para redes públicas e quero expandir para mais municípios e estados.",
        },
        "internacional": {
            "nome": "Internacional",
            "icone": '<svg viewBox="0 0 32 32" width="32" height="32" xmlns="http://www.w3.org/2000/svg" aria-hidden="true"><rect x="2" y="2" width="13" height="28" fill="#A725FF"/><rect x="17" y="2" width="13" height="28" fill="#BBD634"/><polygon points="16,8 24,16 16,24 8,16" fill="#A725FF"/></svg>',
            "pergunta": "Que pré-requisitos regulatórios, técnicos e pedagógicos preciso cumprir para entrar no Brasil?",
            "descricao": "Tenho produto fora do Brasil e quero entrar no mercado brasileiro de educação pública.",
        },
    },
}

# ── Seções extras (não-persona) ───────────────────────────────
SECTIONS = {
    "recursos": {
        "nome": "Recursos",
        "cor": "#718096",
        "descricao": "Instrumentos, checklists, glossário e publicação para download",
        "icone": '<svg viewBox="0 0 32 32" width="32" height="32" xmlns="http://www.w3.org/2000/svg" aria-hidden="true"><rect x="2" y="8" width="20" height="16" fill="#A725FF"/><rect x="12" y="5" width="18" height="12" transform="rotate(15,21,11)" fill="#BBD634"/></svg>',
    },
    "contexto-politica": {
        "nome": "Contexto e Política",
        "cor": "#c05621",
        "descricao": "Cenário atual, desafios, boas práticas internacionais e documentos oficiais",
        "icone": '<svg viewBox="0 0 32 32" width="32" height="32" xmlns="http://www.w3.org/2000/svg" aria-hidden="true"><rect x="14" y="2" width="16" height="28" fill="#BBD634"/><polygon points="2,6 16,16 2,26" fill="#A725FF"/></svg>',
    },
    "sobre-o-guia": {
        "nome": "Sobre o Guia",
        "cor": "#4a5568",
        "descricao": "Apresentação, metodologia e informações sobre a publicação",
        "icone": '<svg viewBox="0 0 32 32" width="32" height="32" xmlns="http://www.w3.org/2000/svg" aria-hidden="true"><path d="M6 4h14l6 6v18H6z" fill="#A725FF"/><rect x="10" y="14" width="12" height="2" fill="#BBD634"/><rect x="10" y="18" width="9" height="2" fill="#BBD634"/><rect x="10" y="22" width="11" height="2" fill="#BBD634"/></svg>',
    },
}

# Prioridade de exibição dos tipos de material
TIPO_PRIORIDADE = {
    "one-pager": ("comece", "Resumo Executivo", 0),
    "template": ("comece", "Template", 1),
    "usos": ("aprofunde", "Usos em Potencial", 0),
    "jornada-antes": ("aprofunde", "Antes da Contratação", 1),
    "jornada-durante": ("aprofunde", "Durante a Contratação", 2),
    "jornada-apos": ("aprofunde", "Após a Contratação", 3),
    "cinco-perguntas": ("aprofunde", "5 Perguntas", 4),
    "guia": ("aprofunde", "Guia Completo", 5),
    "checklist": ("aprofunde", "Checklist", 6),
    "faq": ("aprofunde", "FAQ", 7),
    "framework": ("aprofunde", "Framework de Decisão", 8),
    "policy-brief": ("aprofunde", "Policy Brief", 9),
    "contexto": ("aprofunde", "Contexto", 1),
    "glossario": ("aprofunde", "Glossário", 2),
    "apresentacao": ("comece", "Apresentação", 0),
    "metodologia": ("aprofunde", "Metodologia", 1),
    "guia-complementar": ("complementar", "Material Complementar", 10),
}

# ── Markdown → HTML ──────────────────────────────────────────

def parse_frontmatter(text: str) -> tuple[dict, str]:
    """Extrai frontmatter YAML e retorna (metadata, conteúdo)."""
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            meta = yaml.safe_load(parts[1]) or {}
            body = parts[2].strip()
            return meta, body
    return {}, text


def md_to_html(text: str) -> str:
    """Converte markdown para HTML com extensões."""
    md = markdown.Markdown(
        extensions=[
            "tables",
            "fenced_code",
            "codehilite",
            "toc",
            "nl2br",
            "sane_lists",
        ],
        extension_configs={
            "codehilite": {"css_class": "highlight", "guess_lang": False},
            "toc": {"permalink": False},
        },
    )
    html = md.convert(text)
    # Converte task list items (GFM-style checkboxes)
    html = re.sub(
        r"<li>\s*\[ \]\s*",
        '<li class="task-item"><input type="checkbox" disabled> ',
        html,
    )
    html = re.sub(
        r"<li>\s*\[x\]\s*",
        '<li class="task-item"><input type="checkbox" checked disabled> ',
        html,
        flags=re.IGNORECASE,
    )
    return html


def extract_toc(html: str) -> list[dict]:
    """Extrai headings H2 do HTML para montar o TOC da sidebar."""
    pattern = re.compile(r'<h2[^>]*id="([^"]*)"[^>]*>(.*?)</h2>', re.DOTALL)
    toc = []
    for match in pattern.finditer(html):
        anchor = match.group(1)
        # Remove tags HTML internas ao heading
        label = re.sub(r"<[^>]+>", "", match.group(2)).strip()
        toc.append({"id": anchor, "label": label})
    return toc


def estimate_reading_time(text: str) -> int:
    """Estima tempo de leitura em minutos (~200 palavras/min em pt-BR)."""
    words = len(text.split())
    return max(1, round(words / 200))


def _infer_tipo(stem: str) -> str:
    """Infere tipo de material a partir do nome do arquivo."""
    if "one-pager" in stem:
        return "one-pager"
    elif "checklist" in stem:
        return "checklist"
    elif "faq" in stem:
        return "faq"
    elif "framework" in stem:
        return "framework"
    elif "policy-brief" in stem:
        return "policy-brief"
    elif "internacionais" in stem:
        return "guia-complementar"
    else:
        return "guia"


def _process_md(md_file: Path, persona_key: str) -> dict:
    """Processa um arquivo .md e retorna o dict do material."""
    text = md_file.read_text(encoding="utf-8")
    meta, body = parse_frontmatter(text)

    tipo = meta.get("tipo", "") or _infer_tipo(md_file.stem)

    html_content = md_to_html(body)
    toc = extract_toc(html_content)
    reading_time = estimate_reading_time(body)
    prio_info = TIPO_PRIORIDADE.get(tipo, ("complementar", tipo, 99))

    slug = md_file.stem
    return {
        "slug": slug,
        "filename": f"{slug}.html",
        "title": meta.get("title", slug),
        "subtitle": meta.get("subtitle", ""),
        "tipo": tipo,
        "categoria": prio_info[0],
        "tipo_label": prio_info[1],
        "sort_order": prio_info[2],
        "html": html_content,
        "toc": toc,
        "reading_time": reading_time,
        "persona": persona_key,
    }


# ── Descoberta de materiais ──────────────────────────────────

def discover_materials() -> dict[str, list[dict]]:
    """Descobre todos os .md e organiza por persona (e sub-persona)."""
    materials: dict[str, list[dict]] = {p: [] for p in PERSONAS}

    for persona_key in PERSONAS:
        persona_dir = CONTENT_DIR / persona_key
        if not persona_dir.is_dir():
            continue

        # Materiais root-level da persona (ex: materiais/edtechs/*.md)
        for md_file in sorted(persona_dir.glob("*.md")):
            materials[persona_key].append(_process_md(md_file, persona_key))

        # Ordena por prioridade
        materials[persona_key].sort(key=lambda m: m["sort_order"])

        # Sub-personas (ex: materiais/edtechs/estagio-inicial/*.md)
        if persona_key in SUB_PERSONAS:
            for sp_key in SUB_PERSONAS[persona_key]:
                sp_dir = persona_dir / sp_key
                composite_key = f"{persona_key}/{sp_key}"
                materials[composite_key] = []
                if not sp_dir.is_dir():
                    continue
                for md_file in sorted(sp_dir.glob("*.md")):
                    materials[composite_key].append(
                        _process_md(md_file, persona_key)
                    )
                materials[composite_key].sort(key=lambda m: m["sort_order"])

    # Seções extras (recursos, etc.)
    for section_key in SECTIONS:
        section_dir = CONTENT_DIR / section_key
        materials[section_key] = []
        if not section_dir.is_dir():
            continue
        for md_file in sorted(section_dir.glob("*.md")):
            materials[section_key].append(_process_md(md_file, section_key))
        materials[section_key].sort(key=lambda m: m["sort_order"])

    return materials


def _group_by_category(docs: list[dict]) -> dict[str, list[dict]]:
    """Agrupa documentos por categoria (comece/aprofunde/complementar)."""
    categorias = {"comece": [], "aprofunde": [], "complementar": []}
    for doc in docs:
        cat = doc["categoria"]
        if cat in categorias:
            categorias[cat].append(doc)
    return categorias


_CAT_LABELS = {
    "comece": "Comece por aqui",
    "aprofunde": "Aprofunde",
    "complementar": "Complementar",
}


def _group_docs_for_journey(docs: list[dict]) -> list[dict]:
    """Retorna lista de grupos [{cat_label, docs}] mantendo ordem de exibição."""
    groups: list[dict] = []
    seen: dict[str, dict] = {}
    for doc in docs:
        cat = doc["categoria"]
        if cat not in seen:
            group: dict = {"cat": cat, "cat_label": _CAT_LABELS.get(cat, cat), "docs": []}
            groups.append(group)
            seen[cat] = group
        seen[cat]["docs"].append(doc)
    return groups


# ── Geração do site ──────────────────────────────────────────

def build_site():
    """Gera o site estático completo."""
    print("🔨 Gerando site...")

    # Limpa saída anterior
    if OUTPUT_DIR.exists():
        shutil.rmtree(OUTPUT_DIR)
    OUTPUT_DIR.mkdir(parents=True)

    # Configura Jinja2
    env = Environment(
        loader=FileSystemLoader(str(TEMPLATE_DIR)),
        autoescape=False,
    )

    materials = discover_materials()

    # Contexto base (root será ajustado por nível de profundidade)
    base_ctx = {
        "personas": PERSONAS,
        "sections": SECTIONS,
        "materials": materials,
        "site_title": "Contratação Pública de IA na Educação",
        "site_subtitle": "Aliança de IA para a Educação · Instituto Jataí",
    }

    # 1. Landing page (nível raiz: root = ".")
    tmpl_index = env.get_template("index.html")
    persona_summaries = []
    for key, info in PERSONAS.items():
        # Contar todos os materiais (root + sub-personas)
        count = len(materials.get(key, []))
        if key in SUB_PERSONAS:
            for sp_key in SUB_PERSONAS[key]:
                count += len(materials.get(f"{key}/{sp_key}", []))
        persona_summaries.append({
            **info,
            "key": key,
            "count": count,
        })
    (OUTPUT_DIR / "index.html").write_text(
        tmpl_index.render(**base_ctx, root=".", persona_list=persona_summaries),
        encoding="utf-8",
    )
    print("  ✓ index.html")

    # 2. Páginas de persona e conteúdo
    tmpl_persona = env.get_template("persona.html")
    tmpl_document = env.get_template("document.html")

    for persona_key, persona_info in PERSONAS.items():
        persona_dir = OUTPUT_DIR / persona_key
        persona_dir.mkdir(parents=True)

        docs = materials.get(persona_key, [])
        categorias = _group_by_category(docs)

        # Outras personas (para navegação lateral)
        outras_personas = [
            {"key": k, **v} for k, v in PERSONAS.items() if k != persona_key
        ]

        # Persona com sub-personas? (ex: edtechs)
        has_sub = persona_key in SUB_PERSONAS

        if has_sub:
            # Landing page especial com seletor de sub-personas
            tmpl_sp_landing = env.get_template("persona_with_subpersonas.html")
            sub_personas_list = []
            for sp_key, sp_info in SUB_PERSONAS[persona_key].items():
                sp_count = len(materials.get(f"{persona_key}/{sp_key}", []))
                sub_personas_list.append({
                    **sp_info,
                    "key": sp_key,
                    "count": sp_count,
                })
            (persona_dir / "index.html").write_text(
                tmpl_sp_landing.render(
                    **base_ctx,
                    root="..",
                    persona_key=persona_key,
                    persona=persona_info,
                    docs=docs,
                    categorias=categorias,
                    outras_personas=outras_personas,
                    sub_personas=sub_personas_list,
                ),
                encoding="utf-8",
            )
            print(f"  ✓ {persona_key}/index.html (com sub-personas)")

            # Renderizar materiais transversais (root-level)
            journey_groups = _group_docs_for_journey(docs)
            for idx, doc in enumerate(docs):
                prev_doc = docs[idx - 1] if idx > 0 else None
                next_doc = docs[idx + 1] if idx < len(docs) - 1 else None
                (persona_dir / doc["filename"]).write_text(
                    tmpl_document.render(
                        **base_ctx,
                        root="..",
                        persona_key=persona_key,
                        persona=persona_info,
                        doc=doc,
                        outras_personas=outras_personas,
                        back_url=f"../{ persona_key}/index.html",
                        all_docs=docs,
                        journey_groups=journey_groups,
                        doc_index=idx,
                        doc_total=len(docs),
                        prev_doc=prev_doc,
                        next_doc=next_doc,
                    ),
                    encoding="utf-8",
                )
                print(f"  ✓ {persona_key}/{doc['filename']}")

            # Sub-personas
            for sp_key, sp_info in SUB_PERSONAS[persona_key].items():
                sp_dir = persona_dir / sp_key
                sp_dir.mkdir(parents=True)
                composite_key = f"{persona_key}/{sp_key}"
                sp_docs = materials.get(composite_key, [])
                sp_categorias = _group_by_category(sp_docs)

                # Sub-persona index (usa persona.html com parent_persona)
                (sp_dir / "index.html").write_text(
                    tmpl_persona.render(
                        **base_ctx,
                        root="../..",
                        persona_key=f"{persona_key}/{sp_key}",
                        persona={**sp_info, "cor": persona_info["cor"]},
                        docs=sp_docs,
                        categorias=sp_categorias,
                        outras_personas=outras_personas,
                        parent_persona=persona_info,
                        parent_persona_key=persona_key,
                    ),
                    encoding="utf-8",
                )
                print(f"  ✓ {persona_key}/{sp_key}/index.html")

                # Documentos da sub-persona
                sp_journey_groups = _group_docs_for_journey(sp_docs)
                for idx, doc in enumerate(sp_docs):
                    prev_doc = sp_docs[idx - 1] if idx > 0 else None
                    next_doc = sp_docs[idx + 1] if idx < len(sp_docs) - 1 else None
                    (sp_dir / doc["filename"]).write_text(
                        tmpl_document.render(
                            **base_ctx,
                            root="../..",
                            persona_key=f"{persona_key}/{sp_key}",
                            persona={**sp_info, "cor": persona_info["cor"]},
                            doc=doc,
                            outras_personas=outras_personas,
                            parent_persona=persona_info,
                            parent_persona_key=persona_key,
                            back_url=f"../../{persona_key}/{sp_key}/index.html",
                            all_docs=sp_docs,
                            journey_groups=sp_journey_groups,
                            doc_index=idx,
                            doc_total=len(sp_docs),
                            prev_doc=prev_doc,
                            next_doc=next_doc,
                        ),
                        encoding="utf-8",
                    )
                    print(f"  ✓ {persona_key}/{sp_key}/{doc['filename']}")
        else:
            # Persona sem sub-personas (comportamento original)
            (persona_dir / "index.html").write_text(
                tmpl_persona.render(
                    **base_ctx,
                    root="..",
                    persona_key=persona_key,
                    persona=persona_info,
                    docs=docs,
                    categorias=categorias,
                    outras_personas=outras_personas,
                ),
                encoding="utf-8",
            )
            print(f"  ✓ {persona_key}/index.html")

            journey_groups = _group_docs_for_journey(docs)
            for idx, doc in enumerate(docs):
                prev_doc = docs[idx - 1] if idx > 0 else None
                next_doc = docs[idx + 1] if idx < len(docs) - 1 else None
                (persona_dir / doc["filename"]).write_text(
                    tmpl_document.render(
                        **base_ctx,
                        root="..",
                        persona_key=persona_key,
                        persona=persona_info,
                        doc=doc,
                        outras_personas=outras_personas,
                        back_url=f"../{persona_key}/index.html",
                        all_docs=docs,
                        journey_groups=journey_groups,
                        doc_index=idx,
                        doc_total=len(docs),
                        prev_doc=prev_doc,
                        next_doc=next_doc,
                    ),
                    encoding="utf-8",
                )
                print(f"  ✓ {persona_key}/{doc['filename']}")

    # 3. Seções extras (recursos, etc.)
    for section_key, section_info in SECTIONS.items():
        section_dir = OUTPUT_DIR / section_key
        section_dir.mkdir(parents=True)

        docs = materials.get(section_key, [])
        categorias = _group_by_category(docs)

        outras_personas = [
            {"key": k, **v} for k, v in PERSONAS.items()
        ]

        tmpl_section = env.get_template("section_recursos.html")
        (section_dir / "index.html").write_text(
            tmpl_section.render(
                **base_ctx,
                root="..",
                section_key=section_key,
                section=section_info,
                docs=docs,
                categorias=categorias,
                outras_personas=outras_personas,
            ),
            encoding="utf-8",
        )
        print(f"  ✓ {section_key}/index.html")

        section_journey_groups = _group_docs_for_journey(docs)
        for idx, doc in enumerate(docs):
            prev_doc = docs[idx - 1] if idx > 0 else None
            next_doc = docs[idx + 1] if idx < len(docs) - 1 else None
            (section_dir / doc["filename"]).write_text(
                tmpl_document.render(
                    **base_ctx,
                    root="..",
                    persona_key=section_key,
                    persona=section_info,
                    doc=doc,
                    outras_personas=outras_personas,
                    back_url=f"../{section_key}/index.html",
                    all_docs=docs,
                    journey_groups=section_journey_groups,
                    doc_index=idx,
                    doc_total=len(docs),
                    prev_doc=prev_doc,
                    next_doc=next_doc,
                ),
                encoding="utf-8",
            )
            print(f"  ✓ {section_key}/{doc['filename']}")

    # 4. Redirect para URL antiga do guia internacional
    redirect_html = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta http-equiv="refresh" content="0;url=internacional/guia-internacionais.html">
<title>Redirecionando...</title>
</head>
<body>
<p>Redirecionando para <a href="internacional/guia-internacionais.html">nova localização</a>...</p>
</body>
</html>"""
    redirect_path = OUTPUT_DIR / "edtechs" / "guia-edtechs-internacionais.html"
    if not redirect_path.exists():
        redirect_path.write_text(redirect_html, encoding="utf-8")
        print("  ✓ edtechs/guia-edtechs-internacionais.html (redirect)")

    # 5. Copia assets
    assets_out = OUTPUT_DIR / "assets"
    if ASSETS_DIR.exists():
        shutil.copytree(ASSETS_DIR, assets_out)
    print("  ✓ assets/")

    print(f"\n✅ Site gerado em {OUTPUT_DIR}")
    return OUTPUT_DIR


# ── Servidor local ───────────────────────────────────────────

def serve(directory: Path, port: int = 8000):
    """Serve o site localmente."""
    os.chdir(directory)
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", port), handler) as httpd:
        print(f"\n🌐 Servindo em http://localhost:{port}")
        print("   Ctrl+C para parar\n")
        httpd.serve_forever()


def watch_and_rebuild(interval: float = 1.0):
    """Monitora arquivos e reconstrói ao detectar mudanças."""
    def get_mtimes():
        mtimes = {}
        for ext in ("*.md", "*.html", "*.css", "*.js"):
            for p in BASE_DIR.rglob(ext):
                if "output" not in p.parts:
                    mtimes[str(p)] = p.stat().st_mtime
        return mtimes

    last = get_mtimes()
    print("👁️  Monitorando mudanças... (Ctrl+C para parar)")
    while True:
        time.sleep(interval)
        current = get_mtimes()
        if current != last:
            print("\n🔄 Mudança detectada, reconstruindo...")
            try:
                build_site()
            except Exception as e:
                print(f"❌ Erro: {e}")
            last = get_mtimes()


# ── CLI ──────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Gera site estático dos materiais da Aliança de IA"
    )
    parser.add_argument(
        "--serve", action="store_true",
        help="Gera o site e serve em localhost:8000",
    )
    parser.add_argument(
        "--watch", action="store_true",
        help="Gera, serve e recarrega em mudanças",
    )
    parser.add_argument(
        "--port", type=int, default=8000,
        help="Porta do servidor local (padrão: 8000)",
    )
    args = parser.parse_args()

    output = build_site()

    if args.watch:
        server_thread = threading.Thread(
            target=serve, args=(output, args.port), daemon=True,
        )
        server_thread.start()
        watch_and_rebuild()
    elif args.serve:
        serve(output, args.port)


if __name__ == "__main__":
    main()
