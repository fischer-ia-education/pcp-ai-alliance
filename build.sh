#!/usr/bin/env bash
# ============================================================================
# Build script para materiais da Aliança de IA para a Educação
# Converte arquivos Markdown em PDF e HTML usando pandoc + weasyprint
#
# Uso:
#   ./build.sh              # Gera tudo (PDF + HTML)
#   ./build.sh --html       # Só HTML
#   ./build.sh --pdf        # Só PDF
#   ./build.sh edtechs      # Só materiais de edtechs
#   ./build.sh gestores     # Só materiais de gestores
#   ./build.sh intermediarios
#   ./build.sh legisladores
#   ./build.sh educadores
#
# Dependências: pandoc
# Opcionais:    weasyprint (para PDF via HTML), wkhtmltopdf (alternativa)
# ============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONTENT_DIR="$SCRIPT_DIR/conteudo"
CSS_FILE="$SCRIPT_DIR/style.css"
OUTPUT_DIR="$SCRIPT_DIR/output"
HTML_DIR="$OUTPUT_DIR/html"
PDF_DIR="$OUTPUT_DIR/pdf"

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

info()  { echo -e "${GREEN}[INFO]${NC} $*"; }
warn()  { echo -e "${YELLOW}[WARN]${NC} $*"; }
error() { echo -e "${RED}[ERRO]${NC} $*" >&2; }

# Verificar dependências
check_deps() {
    if ! command -v pandoc &>/dev/null; then
        error "pandoc não encontrado. Instale com: sudo pacman -S pandoc (Arch) ou sudo apt install pandoc (Debian/Ubuntu)"
        exit 1
    fi
    if ! command -v weasyprint &>/dev/null; then
        warn "weasyprint não encontrado. PDFs não serão gerados."
        warn "Instale com: pip install weasyprint"
        HAS_WEASYPRINT=false
    else
        HAS_WEASYPRINT=true
    fi
}

# Converter um arquivo .md para HTML
md_to_html() {
    local input="$1"
    local filename
    filename="$(basename "$input" .md)"
    local persona_dir
    persona_dir="$(basename "$(dirname "$input")")"
    local output="$HTML_DIR/${persona_dir}/${filename}.html"

    mkdir -p "$(dirname "$output")"

    pandoc "$input" \
        --from markdown \
        --to html5 \
        --standalone \
        --css "$CSS_FILE" \
        --embed-resources \
        --metadata lang=pt-BR \
        --template="$SCRIPT_DIR/template.html" 2>/dev/null \
        || pandoc "$input" \
            --from markdown \
            --to html5 \
            --standalone \
            --css "$CSS_FILE" \
            --metadata lang=pt-BR \
            -o "$output"

    # Fallback se template não existir
    if [[ ! -f "$output" ]]; then
        pandoc "$input" \
            --from markdown \
            --to html5 \
            --standalone \
            --css "$CSS_FILE" \
            --metadata lang=pt-BR \
            -o "$output"
    fi

    info "HTML: $output"
}

# Converter HTML para PDF via weasyprint
html_to_pdf() {
    local html_file="$1"
    local filename
    filename="$(basename "$html_file" .html)"
    local persona_dir
    persona_dir="$(basename "$(dirname "$html_file")")"
    local output="$PDF_DIR/${persona_dir}/${filename}.pdf"

    mkdir -p "$(dirname "$output")"

    weasyprint "$html_file" "$output" 2>/dev/null
    info "PDF:  $output"
}

# Converter um arquivo .md direto para PDF (fallback sem weasyprint)
md_to_pdf_direct() {
    local input="$1"
    local filename
    filename="$(basename "$input" .md)"
    local persona_dir
    persona_dir="$(basename "$(dirname "$input")")"
    local output="$PDF_DIR/${persona_dir}/${filename}.pdf"

    mkdir -p "$(dirname "$output")"

    pandoc "$input" \
        --from markdown \
        --to pdf \
        --pdf-engine=xelatex \
        -V geometry:margin=2.5cm \
        -V lang=pt-BR \
        -V fontsize=11pt \
        -o "$output" 2>/dev/null && info "PDF:  $output" \
        || warn "Falha ao gerar PDF para $input (xelatex disponível?)"
}

# Processar uma pasta de persona
process_persona() {
    local persona="$1"
    local persona_dir="$CONTENT_DIR/$persona"

    if [[ ! -d "$persona_dir" ]]; then
        warn "Diretório não encontrado: $persona_dir"
        return
    fi

    info "Processando persona: $persona"

    for md_file in "$persona_dir"/*.md; do
        [[ -f "$md_file" ]] || continue

        if [[ "$FORMAT" == "all" || "$FORMAT" == "html" ]]; then
            md_to_html "$md_file"
        fi

        if [[ "$FORMAT" == "all" || "$FORMAT" == "pdf" ]]; then
            if $HAS_WEASYPRINT; then
                local filename
                filename="$(basename "$md_file" .md)"
                local html_output="$HTML_DIR/${persona}/${filename}.html"
                # Gera HTML primeiro se ainda não existe
                [[ -f "$html_output" ]] || md_to_html "$md_file"
                html_to_pdf "$html_output"
            else
                md_to_pdf_direct "$md_file"
            fi
        fi
    done
}

# Main
main() {
    local FORMAT="all"
    local PERSONAS=("edtechs" "gestores" "intermediarios" "legisladores" "educadores")

    # Parse argumentos
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --html)   FORMAT="html"; shift ;;
            --pdf)    FORMAT="pdf"; shift ;;
            edtechs|gestores|intermediarios|legisladores|educadores)
                      PERSONAS=("$1"); shift ;;
            --help|-h)
                echo "Uso: $0 [--html|--pdf] [persona]"
                echo ""
                echo "Personas: edtechs, gestores, intermediarios, legisladores, educadores"
                echo "Formatos: --html (só HTML), --pdf (só PDF), sem flag = ambos"
                exit 0
                ;;
            *)
                error "Argumento desconhecido: $1"
                exit 1
                ;;
        esac
    done

    check_deps

    mkdir -p "$HTML_DIR" "$PDF_DIR"

    info "=== Build dos Materiais da Aliança de IA ==="
    info "Formato: $FORMAT"
    info "Personas: ${PERSONAS[*]}"
    echo ""

    for persona in "${PERSONAS[@]}"; do
        process_persona "$persona"
    done

    echo ""
    info "=== Build concluído ==="
    info "Saída em: $OUTPUT_DIR"
}

main "$@"
