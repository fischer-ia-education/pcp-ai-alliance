---
title: "Especificações Técnicas de IA para Termos de Referência"
subtitle: "Blocos de texto e critérios para incluir em editais e TRs de soluções de IA educacional"
author: "Aliança de IA para a Educação"
date: "2026"
persona: gestores
tipo: guia-complementar
---

# Especificações Técnicas de IA para Termos de Referência

Este material é para quem monta edital e Termo de Referência (TR) na secretaria de educação. Quando a equipe pedagógica define que precisa de uma solução de IA, alguém precisa traduzir essa necessidade em especificações técnicas. Sem especificações adequadas, o edital atrai soluções genéricas e deixa a rede vulnerável.

## Bloco 1: Descrição da solução e do componente de IA

Exigir do fornecedor: tipo de IA utilizada (ML, PLN, generativa, preditiva, combinação), grau de autonomia (assistiva, semiautônoma, autônoma), dados de treinamento (fontes, idioma, população, período), limitações conhecidas.

Exemplo de redação para o TR: "O fornecedor deverá apresentar documentação técnica que descreva o tipo de inteligência artificial utilizada na solução, o grau de autonomia do sistema em relação a decisões pedagógicas, as fontes e características dos dados de treinamento e as limitações conhecidas do modelo."

## Bloco 2: Infraestrutura e compatibilidade

Especificar dispositivos suportados (Chromebooks, tablets Android, PCs, celulares), requisitos de conectividade (largura de banda mínima, modo offline), hospedagem (nuvem em território brasileiro ou país com proteção adequada), integração com sistemas existentes (API REST, formatos abertos).

Exemplo: "A solução deverá funcionar em dispositivos Chromebook e Android com navegador Chrome versão 100 ou superior, com conexão mínima de 1 Mbps, dispor de funcionalidade offline para inserção de dados em ambiente sem conectividade, e disponibilizar API REST documentada para integração com o sistema [nome do sistema da rede]."

## Bloco 3: Proteção de dados e privacidade

Exigir: conformidade com LGPD e indicação de DPO, mecanismo de consentimento dos responsáveis (art. 14 LGPD), minimização de dados (especificar categorias aceitáveis e vedadas), criptografia (TLS 1.2+ em trânsito, AES-256 em repouso), política de retenção e exclusão (prazo sugerido: 60 dias após encerramento), pseudonimização em relatórios.

Exemplo: "O fornecedor deverá apresentar política de privacidade em conformidade com a Lei 13.709/2018 (LGPD), implementar mecanismo de consentimento dos responsáveis legais para tratamento de dados de menores, utilizar criptografia TLS 1.2+ em trânsito e AES-256 em repouso, e garantir a exclusão segura de todos os dados em até 60 dias após o encerramento do contrato."

## Bloco 4: Transparência, explicabilidade e auditabilidade

Exigir: rotulagem (informar ao usuário quando interage com IA), explicabilidade (justificativas compreensíveis para decisões/recomendações), logs de decisões automatizadas (entrada, processamento, saída, timestamp, acessíveis à rede, exportáveis, mantidos por vigência + 12 meses), permissão para auditorias técnicas e pedagógicas.

Exemplo: "O fornecedor deverá manter logs de todas as decisões automatizadas, acessíveis à equipe gestora em formato exportável, pelo período de vigência e por 12 meses após encerramento. O fornecedor deverá permitir auditorias técnicas e pedagógicas realizadas pela contratante ou por terceiro por ela indicado, mediante aviso prévio de 30 dias."

## Bloco 5: Supervisão humana

Exigir: nenhuma decisão de alto impacto executada automaticamente sem validação humana, ferramentas para o professor anular/corrigir recomendações da IA, formação contratual (presencial ou online, mínimo de [X] horas).

## Bloco 6: Portabilidade e saída

Exigir: exportação de dados em formato aberto (CSV, JSON, XML) a qualquer momento sem custo, API documentada e padrões abertos, plano de transição para encerramento (prazo de exportação, formato, suporte, exclusão), ausência de cláusulas que restrinjam migração ou imponham custos de saída desproporcionais.

Exemplo: "Ao término do contrato, o fornecedor deverá disponibilizar todos os dados gerados em formato aberto, em prazo de até 30 dias, sem custo adicional, e proceder à exclusão segura em até 60 dias. O contrato não conterá cláusulas que restrinjam a portabilidade ou imponham custos de migração."

## Bloco 7: Indicadores de desempenho (SLA)

| Indicador | Meta sugerida | Periodicidade |
|-----------|---------------|---------------|
| Disponibilidade da plataforma | ≥ 99% | Mensal |
| Tempo de resposta para incidentes críticos | ≤ 4 horas úteis | Por ocorrência |
| Tempo de resposta para suporte pedagógico | ≤ 24 horas úteis | Por ocorrência |
| Entrega de relatórios periódicos | Conforme cronograma | Trimestral |
| Atualização de segurança | ≤ 72 horas para vulnerabilidades críticas | Por ocorrência |

Prever glosas ou sanções proporcionais ao descumprimento, com escala progressiva.
