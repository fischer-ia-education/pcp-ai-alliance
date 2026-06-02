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

# ── Critérios de Contratação (fonte única) ────────────────────
# Os 14 critérios práticos do Instituto Jataí, organizados em 3 blocos.
# Renderizados na página interativa recursos/criterios-contratacao.html
# e no launcher embutido em gestores/durante-a-contratacao.md.
BLOCOS_CRITERIOS = {
    "ET": {
        "nome": "Especificação Técnica",
        "resumo": "O que a solução deve ser capaz de fazer. Verificável por Prova de Conceito (POC).",
        "cor": "#A725FF",
    },
    "AP": {
        "nome": "Aceitabilidade da Proposta",
        "resumo": "Documentos e declarações que o fornecedor apresenta para participar da licitação. Propostas sem eles são desclassificadas.",
        "cor": "#5a8a00",
    },
    "CC": {
        "nome": "Cláusulas Contratuais",
        "resumo": "Obrigações que valem durante toda a vigência do contrato e guiam a fiscalização.",
        "cor": "#111111",
    },
}

CRITERIOS = [
    {
        "id": "et1", "bloco": "ET", "num": "ET 1",
        "titulo": "Sinalização permanente de IA",
        "salvaguarda": "Transparência e explicabilidade",
        "aplica": "Tutor inteligente e IA generativa",
        "porque": "Alunos e professores têm o direito de saber quando estão interagindo com uma IA, não com um ser humano. Sem essa sinalização, podem atribuir às respostas uma confiabilidade que ela não tem ou desenvolver uma relação com o sistema sem perceber que ele não compreende, não sente e não se responsabiliza pelo que diz.",
        "exigir": "A identificação de IA deve estar visível nas telas de interação, sem necessidade de rolagem. Quando perguntado diretamente se é humano, o sistema deve responder que é uma IA.",
        "onde": ["Termo de Referência: requisito funcional obrigatório da solução"],
        "verificar_intro": "Na POC, executar testes como:",
        "verificar": [
            "Verificar se a identificação de IA está visível em pelo menos 5 telas diferentes do fluxo do aluno",
            "Perguntar diretamente ao sistema “Você é humano?” e registrar a resposta",
        ],
    },
    {
        "id": "et2", "bloco": "ET", "num": "ET 2",
        "titulo": "Alerta obrigatório e validação humana para decisões de alto impacto",
        "salvaguarda": "Supervisão humana contínua",
        "aplica": "Todos os tipos de solução",
        "porque": "Algumas decisões têm consequências diretas e duradouras na vida do aluno, como progressão, reprovação ou classificações de risco de evasão. Nenhum sistema de IA deve tomá-las por conta própria: a responsabilidade pedagógica é do educador, não da solução.",
        "exigir": "O fornecedor deve garantir que nenhuma decisão de alto impacto seja executada sem confirmação ativa de um usuário humano. O sistema deve exigir uma ação deliberada de autorização e registrar quem autorizou e quando.",
        "onde": ["Termo de Referência: requisito funcional obrigatório da solução"],
        "verificar_intro": "Na POC, executar um teste como:",
        "verificar": [
            "Simular atribuição de uma nota ou resultado de progressão/reprovação",
            "Verificar se o sistema exige uma ação deliberada do usuário para prosseguir",
            "Confirmar que: (a) o sistema não executa a ação automaticamente; (b) registra quem confirmou e quando",
        ],
    },
    {
        "id": "et3", "bloco": "ET", "num": "ET 3",
        "titulo": "Anulação de recomendações com registro auditável",
        "salvaguarda": "Supervisão humana contínua",
        "aplica": "Todos os tipos de solução",
        "porque": "Soluções de IA recomendam conteúdos, notas e intervenções com base em dados históricos e podem errar. Equipe pedagógica e professores precisam poder discordar e substituir pelo próprio julgamento. Se essa capacidade não existir, ou não ficar registrada, o algoritmo passa a ter a palavra final sem que ninguém possa questionar.",
        "exigir": "Qualquer recomendação gerada pelo sistema deve poder ser anulada ou substituída pela equipe pedagógica a qualquer momento. Cada anulação registrada automaticamente em log com data, hora e identificação do usuário. O sistema não pode reverter automaticamente uma decisão da equipe. O histórico deve ser acessível ao fiscal da rede, não apenas ao fornecedor.",
        "onde": [
            "Termo de Referência: requisito funcional obrigatório",
            "Plano de fiscalização: verificação pelo fiscal, com frequência definida pela rede",
        ],
        "verificar_intro": "Na POC, executar um teste como:",
        "verificar": [
            "Solicitar uma recomendação ao sistema (trilha, nota, alerta)",
            "Anulá-la pelo perfil de professor ou coordenação pedagógica",
            "Confirmar que: (a) a anulação foi possível; (b) o registro aparece no histórico; (c) o sistema não reverteu a decisão",
            "Durante a execução: o fiscal acessa o histórico de anulações e confirma a disponibilidade para consulta",
        ],
    },
    {
        "id": "et4", "bloco": "ET", "num": "ET 4",
        "titulo": "Mecanismos de controle de conteúdo inapropriado",
        "salvaguarda": "Transparência e explicabilidade",
        "aplica": "Tutor inteligente e IA generativa",
        "porque": "Sistemas que geram texto livremente podem produzir conteúdo inadequado ao contexto escolar ou bloquear indevidamente temas legítimos. A exigência tem respaldo no ECA Digital (Lei nº 15.211/2025), que determina proteção desde a concepção (safety-by-design) para produtos digitais acessados por crianças e adolescentes.",
        "exigir": "O fornecedor deve documentar as categorias de conteúdo que o sistema não produz e a lógica desses limites — não uma lista exaustiva, mas critérios compreensíveis e verificáveis. Deve descrever o processo de atualização dos filtros e o prazo máximo de correção de falhas. As proteções devem estar incorporadas ao design, não apenas como filtros externos.",
        "onde": ["Termo de Referência: requisito funcional obrigatório"],
        "verificar_intro": "Na POC, executar testes como:",
        "verificar": [
            "Grupo 1: interações que devem ser bloqueadas — verificar se o sistema recusa e emite explicação",
            "Grupo 2: temas curriculares sensíveis mas legítimos — verificar se responde sem bloqueio indevido",
        ],
    },
    {
        "id": "et5", "bloco": "ET", "num": "ET 5",
        "titulo": "Proibição de treinamento do modelo com dados dos alunos da rede",
        "salvaguarda": "Privacidade e segurança de dados",
        "aplica": "Todos os tipos de solução",
        "porque": "Ao interagir com uma plataforma de IA, o aluno gera dados valiosos para as empresas. Esses dados pertencem aos alunos e à rede, não ao fornecedor. Usá-los para treinar ou ajustar o modelo pode violar a LGPD, que dá proteção máxima a dados de crianças e adolescentes.",
        "exigir": "O fornecedor não pode usar dados gerados por alunos e professores (interações, respostas, produções, desempenho) para treinar, ajustar ou melhorar o modelo, nem para qualquer finalidade que não seja a execução do contrato. A vedação deve constar na minuta e ser confirmada nos Termos de Serviço do provedor de infraestrutura.",
        "onde": [
            "Termo de Referência: requisito obrigatório",
            "Minuta contratual: cláusula expressa de vedação",
        ],
        "verificar_intro": "",
        "verificar": [
            "Acrescentar cláusula contratual e verificar se os Termos de Serviço do provedor de infraestrutura não a contradizem",
        ],
    },
    {
        "id": "ap1", "bloco": "AP", "num": "AP 1",
        "titulo": "Nota técnica do modelo: variáveis, lógica e dados de treinamento",
        "salvaguarda": "Transparência e explicabilidade",
        "aplica": "Todos os tipos de solução",
        "porque": "A documentação do modelo permite avaliar riscos técnicos, verificar adequação pedagógica e identificar vieses antes da contratação. Sem ela, o gestor contrata uma caixa-preta sem saber o que há dentro.",
        "exigir": "Nota técnica com, no mínimo: tipo de modelo; fonte e período dos dados de treinamento; competências e habilidades cobertas (referência à BNCC quando aplicável); limitações conhecidas; taxa de acerto ou desempenho; e grau de autonomia (sugestões que o humano valida vs. decisões autônomas).",
        "onde": ["Edital: exigência documental (modelo de preenchimento anexado ao edital)"],
        "verificar_intro": "",
        "verificar": ["Na fase de julgamento: conferir se a nota técnica preenche todos os campos exigidos"],
        "atencao": [
            "Modelo que exija informações restritas ou sigilosas pode afastar interessados e restringir a competição",
            "Modelo amplo demais pode dificultar o entendimento das características do objeto",
        ],
    },
    {
        "id": "ap2", "bloco": "AP", "num": "AP 2",
        "titulo": "Declaração de dados coletados com finalidade pedagógica justificada",
        "salvaguarda": "Privacidade e segurança de dados",
        "aplica": "Todos os tipos de solução",
        "porque": "Plataformas coletam muito mais dados do que os usuários percebem — tempo de tela, padrões de clique, histórico de erros, às vezes biometria. Sem uma lista explícita e justificada, a rede não sabe o que autoriza nem como verificar o uso.",
        "exigir": "Declaração de todos os dados coletados, com a finalidade pedagógica de cada variável: o que é coletado, para quê, por quanto tempo é retido e quem acessa. Dados não listados não podem ser coletados na vigência. A declaração integra o contrato como anexo vinculante.",
        "onde": [
            "Edital: exigência documental",
            "Minuta contratual: anexo vinculante, vedando uso para publicidade ou perfilamento",
        ],
        "verificar_intro": "",
        "verificar": ["Na fase de julgamento: verificar se a declaração foi preenchida e se cada dado tem finalidade pedagógica justificada"],
        "atencao": [
            "Dados declaratórios não são confirmáveis no momento do julgamento",
            "Prever rotina de verificação na execução e definir quem na rede é responsável",
        ],
    },
    {
        "id": "ap3", "bloco": "AP", "num": "AP 3",
        "titulo": "Política específica de proteção de dados de crianças e adolescentes",
        "salvaguarda": "Privacidade e segurança de dados",
        "aplica": "Todos os tipos de solução",
        "porque": "A LGPD (art. 14) estabelece proteção reforçada para dados de crianças e adolescentes. Política genérica não basta. Ao contratar, a rede é controladora e o fornecedor, operador — que só pode tratar dados conforme as instruções da rede.",
        "exigir": "Política que mencione explicitamente crianças e adolescentes e descreva: (a) consentimento e bases legais por faixa etária — atenção ao consentimento parental para crianças até 12 anos; (b) vedação a usos não pedagógicos (publicidade, perfilamento, compartilhamento); (c) dados coletados e tratamento de dados sensíveis, com base legal e segurança reforçada; (d) papéis de controlador (rede) e operador (fornecedor), vedado uso autônomo inclusive após o encerramento.",
        "onde": ["Edital: exigência documental"],
        "verificar_intro": "Na fase de julgamento:",
        "verificar": [
            "Verificar se a declaração foi preenchida",
            "Se cada dado coletado tem finalidade pedagógica justificada",
            "Se há distinção entre crianças e adolescentes",
            "Se os dados sensíveis estão identificados com a respectiva base legal",
        ],
        "atencao": [
            "Dados declaratórios não são confirmáveis no momento do julgamento",
            "Prever rotina de verificação na execução e definir o responsável",
        ],
    },
    {
        "id": "cc1", "bloco": "CC", "num": "CC 1",
        "titulo": "Auditoria pedagógica: output da IA vs. julgamento docente",
        "salvaguarda": "Auditabilidade",
        "aplica": "Todos os tipos de solução",
        "porque": "Eficácia técnica não garante eficácia educacional. Um sistema pode funcionar bem no algoritmo e gerar recomendações sem sentido para a turma, o currículo ou a realidade local. A auditoria pedagógica traz o julgamento docente para dentro do ciclo de supervisão.",
        "exigir": "Auditoria pedagógica periódica, confrontando uma amostra das recomendações do sistema com o julgamento de professores usuários. Divergências recorrentes acionam protocolo de revisão junto ao fornecedor.",
        "onde": [
            "Minuta contratual: obrigação periódica com protocolo de revisão",
            "Plano de fiscalização: responsável, periodicidade e forma de registro dos resultados",
        ],
        "verificar_intro": "",
        "verificar": [
            "Apresentar a professores uma amostra de recomendações sem indicar a origem",
            "Registrar os casos avaliados como inadequados ou sem sentido pedagógico",
            "Formalizar divergências recorrentes e encaminhar ao fornecedor para revisão",
        ],
    },
    {
        "id": "cc2", "bloco": "CC", "num": "CC 2",
        "titulo": "Canal de contestação de decisões algorítmicas com SLA definido",
        "salvaguarda": "Auditabilidade",
        "aplica": "Todos os tipos de solução",
        "porque": "Sistemas de IA erram — notas incorretas, alertas equivocados, conteúdos inadequados. Professores, alunos e famílias precisam de um caminho claro para questionar e obter resposta em prazo razoável. Sem canal, os erros ficam sem correção e a confiança se deteriora.",
        "exigir": "Canal de contestação acessível diretamente da interface da plataforma, que registre todas as contestações, com prazo de resposta definido conforme o nível de impacto da decisão. Todos os registros disponíveis para auditoria pela rede.",
        "onde": [
            "Minuta contratual: SLA e obrigação de registro de contestações",
            "Plano de fiscalização: verificação periódica do volume e prazo de atendimento; definir responsável",
        ],
        "verificar_intro": "Durante a execução contratual:",
        "verificar": [
            "Verificar a existência e o funcionamento do canal na interface",
            "Conferir registros e prazos de resposta nas verificações periódicas",
        ],
    },
    {
        "id": "cc3", "bloco": "CC", "num": "CC 3",
        "titulo": "Formação inicial e continuada da equipe da rede",
        "salvaguarda": "Alfabetização algorítmica",
        "aplica": "Todos os tipos de solução",
        "porque": "Uma solução que ninguém sabe usar bem, ou que a equipe usa sem entender os limites, não gera valor pedagógico real e pode causar danos. Quem não reconhece quando o sistema erra tende a seguir as sugestões acriticamente. A formação é condição para a solução funcionar.",
        "exigir": "Formação inicial antes da implantação e formação continuada durante a vigência. Carga horária, formato e periodicidade definidos no contrato conforme o porte da solução. O conteúdo vai além do uso operacional: abrange os limites do sistema e como identificar e tratar resultados inadequados.",
        "onde": [
            "Termo de Referência: carga horária, formato e periodicidade como entregável",
            "Minuta contratual: obrigação com evidência de realização",
            "Plano de fiscalização: verificação a cada ciclo formativo",
        ],
        "verificar_intro": "Durante a execução contratual:",
        "verificar": [
            "Confirmar que a formação inicial ocorreu antes do início do uso da solução",
            "A cada ciclo: confirmar realização com registro de participação",
        ],
    },
    {
        "id": "cc4", "bloco": "CC", "num": "CC 4",
        "titulo": "Portabilidade em formato aberto com destruição certificada",
        "salvaguarda": "Reversibilidade e prevenção de lock-in",
        "aplica": "Todos os tipos de solução",
        "porque": "Ao final do contrato, os dados produzidos pertencem à rede, não ao fornecedor. Se ficarem presos em formato proprietário, a rede perde acesso à própria informação e fica dependente de renovar só para não perder o histórico — um dos mecanismos mais comuns de lock-in.",
        "exigir": "Ao término, o fornecedor entrega todos os dados em formato aberto, destrói as cópias em seus sistemas e apresenta certificado de destruição. Prazo de entrega definido no contrato. Dados legíveis com ferramentas básicas, sem depender de sistemas proprietários.",
        "onde": [
            "Minuta contratual: entrega em formato aberto, prazo e certificado de destruição por terceiro",
            "Plano de fiscalização: checklist de encerramento contratual",
        ],
        "verificar_intro": "No encerramento:",
        "verificar": [
            "Confirmar recebimento dos dados no prazo e que o formato é aberto e legível",
            "Exigir o certificado de destruição antes de dar quitação ao contrato",
        ],
    },
    {
        "id": "cc5", "bloco": "CC", "num": "CC 5",
        "titulo": "Gatilhos objetivos de rescisão sem ônus à rede",
        "salvaguarda": "Reversibilidade e prevenção de lock-in",
        "aplica": "Todos os tipos de solução",
        "porque": "Contratos de IA podem precisar ser encerrados antes do prazo — erros sistemáticos graves, discriminação algorítmica, violação de dados. Sem gatilhos definidos previamente, a rede pode ficar presa a um contrato problemático. Definir antes é mais simples e seguro do que negociar depois do problema.",
        "exigir": "Gatilhos objetivos e mensuráveis para rescisão sem ônus financeiro. Mínimos sugeridos: taxa de erro/inconsistência acima de [XX%] confirmada em auditoria; discriminação algorítmica confirmada; violação confirmada de dados de alunos; descumprimento reiterado do SLA de contestações.",
        "onde": [
            "Minuta contratual: cláusula com gatilhos mensuráveis e procedimento de acionamento",
            "Plano de fiscalização: verificação periódica dos indicadores vinculados aos gatilhos",
        ],
        "verificar_intro": "Durante a execução contratual:",
        "verificar": [
            "Monitorar os indicadores de cada gatilho na periodicidade definida pela rede",
            "O fornecedor entrega relatório com os dados necessários",
        ],
    },
    {
        "id": "cc6", "bloco": "CC", "num": "CC 6",
        "titulo": "Comitê de supervisão algorítmica",
        "salvaguarda": "Governança algorítmica",
        "aplica": "Todos os tipos de solução",
        "porque": "A supervisão tende a se concentrar no fiscal ou numa única área. Um comitê multissetorial distribui a responsabilidade e traz olhares complementares — pedagógico, técnico e jurídico. Redes sem essa estrutura podem começar com arranjos simples (reuniões periódicas) e evoluir conforme a maturidade.",
        "exigir": "Instância de supervisão com representação mínima das áreas pedagógica e técnica da rede e um representante do fornecedor — que participa como informante técnico, não deliberativo. Formato variável conforme a capacidade institucional, de reuniões periódicas a comitê formalizado. Espaço estruturado, com registro.",
        "onde": [
            "Minuta contratual: obrigação da rede e do fornecedor, formato e periodicidade a definir",
            "Plano de fiscalização: composição mínima, periodicidade e forma de registro",
        ],
        "verificar_intro": "Durante a execução contratual:",
        "verificar": [
            "Confirmar que as reuniões acontecem com registro (ata ou equivalente)",
            "Verificar se abordam o uso da solução, não apenas aspectos administrativos",
            "Verificar a presença do fornecedor e o registro das informações técnicas prestadas",
        ],
    },
]


def criterios_por_bloco() -> dict:
    """Agrupa os critérios por bloco (ET/AP/CC) preservando a ordem."""
    grupos = {b: [] for b in BLOCOS_CRITERIOS}
    for c in CRITERIOS:
        grupos[c["bloco"]].append(c)
    return grupos


def render_criterios_launcher(rel_path: str) -> str:
    """Gera o HTML do launcher de critérios embutido em 'Durante a Contratação'.

    rel_path: caminho relativo até criterios-contratacao.html a partir do doc.
    Fonte única: os rótulos saem de CRITERIOS, sem duplicar conteúdo.
    """
    grupos = criterios_por_bloco()
    blocos_html = []
    for sigla, info in BLOCOS_CRITERIOS.items():
        chips = "".join(
            f'<a class="crit-launch-chip" href="{rel_path}#{c["id"]}">'
            f'<span class="crit-launch-num">{c["num"]}</span>{c["titulo"]}</a>'
            for c in grupos[sigla]
        )
        blocos_html.append(
            f'<div class="crit-launch-bloco" style="--bloco-cor: {info["cor"]}">'
            f'<div class="crit-launch-bloco-head"><span class="crit-launch-sigla">{sigla}</span>'
            f'<span class="crit-launch-nome">{info["nome"]}</span></div>'
            f'<p class="crit-launch-resumo">{info["resumo"]}</p>'
            f'<div class="crit-launch-chips">{chips}</div></div>'
        )
    return (
        '<aside class="criterios-launcher" aria-label="Cardápio de critérios de contratação">'
        '<div class="crit-launch-header">'
        '<span class="crit-launch-tag">Cardápio prático</span>'
        '<h3 class="crit-launch-title">Critérios para a contratação de IA</h3>'
        '<p class="crit-launch-intro">Selecione os critérios pertinentes ao tipo de solução e à realidade da rede. '
        'Cada um traz por que existe, o que exigir, onde incluir e como verificar.</p>'
        '</div>'
        + "".join(blocos_html)
        + f'<a class="crit-launch-cta" href="{rel_path}">Ver todos os critérios em detalhe '
        '<svg width="16" height="16" viewBox="0 0 16 16" fill="none" aria-hidden="true"><path d="M3 8h10M9 4l4 4-4 4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg></a>'
        '</aside>'
    )


# Templates editáveis para download (slug → arquivo em assets/downloads/)
# Gerados por site/gerar_templates_docx.py
DOWNLOADS = {
    "ripd-simplificado": {
        "arquivo": "ripd-simplificado-template.docx",
        "rotulo": "Baixar versão editável (Word)",
    },
    "model-card-educacional": {
        "arquivo": "model-card-educacional-template.docx",
        "rotulo": "Baixar versão editável (Word)",
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
    # Marcador do launcher de critérios (fonte única → HTML gerado).
    # Usado em gestores/durante-a-contratacao.md (profundidade 1 → ../recursos/).
    if "[[CRITERIOS_LAUNCHER]]" in html_content:
        launcher = render_criterios_launcher("../recursos/criterios-contratacao.html")
        html_content = re.sub(
            r"<p>\s*\[\[CRITERIOS_LAUNCHER\]\]\s*</p>|\[\[CRITERIOS_LAUNCHER\]\]",
            launcher,
            html_content,
        )
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
        "download": DOWNLOADS.get(slug),
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

    # 3b. Página interativa de Critérios de Contratação (dentro de Recursos)
    tmpl_criterios = env.get_template("criterios.html")
    recursos_info = SECTIONS["recursos"]
    (OUTPUT_DIR / "recursos" / "criterios-contratacao.html").write_text(
        tmpl_criterios.render(
            **base_ctx,
            root="..",
            section_key="recursos",
            section=recursos_info,
            blocos=BLOCOS_CRITERIOS,
            criterios_grupos=criterios_por_bloco(),
            outras_personas=[{"key": k, **v} for k, v in PERSONAS.items()],
        ),
        encoding="utf-8",
    )
    print("  ✓ recursos/criterios-contratacao.html")

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

    # 5b. Página interna de Revisão (standalone, com abas V2/V3)
    revisao_src = BASE_DIR / "REVISAO-PLATAFORMA.html"
    if revisao_src.exists():
        shutil.copy(revisao_src, OUTPUT_DIR / "revisao.html")
        print("  ✓ revisao.html")

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
