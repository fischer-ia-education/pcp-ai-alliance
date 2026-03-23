---
title: "Model Card Educacional: Template para Documentação de Soluções de IA na Educação Brasileira"
subtitle: "Ficha técnica padronizada para descrever como um modelo de IA educacional funciona"
author: "Aliança de IA para a Educação"
date: "2026"
tipo: template
---

# Model Card Educacional: Template para Documentação de Soluções de IA na Educação Brasileira

O Model Card é uma ficha técnica padronizada que descreve como um modelo de IA funciona, para que serve, quais são seus limites e como foi avaliado. No contexto educacional brasileiro, tem duas funções: para a edtech, é um instrumento de responsabilidade e diferenciação. Para o gestor público, permite avaliar se a solução é adequada, segura e auditável.

Nem todos os campos serão aplicáveis a todas as soluções. Preencha o que for pertinente e indique "Não aplicável" nos demais.

## MODEL CARD: [Nome da Solução]

Versão: [ex.: 2.1] | Data: [ex.: março/2026] | Empresa: [nome] | Contato técnico: [nome e e-mail]

## 1. Visão geral

1.1 Descrição da solução: [O que faz, para quem, que problema pedagógico resolve. 2-3 parágrafos, linguagem acessível.]

1.2 Tipo de IA utilizada: [ML supervisionado / não supervisionado / por reforço / PLN / IA generativa / recomendação / preditiva / outro.]

1.3 Grau de autonomia: [Assistiva / Semiautônoma / Autônoma. Especifique por funcionalidade.]

1.4 Público-alvo: [Série/etapa, disciplina, perfil.]

1.5 Alinhamento curricular: [Relação com a BNCC: áreas, competências, habilidades.]

## 2. Dados

2.1 Dados de treinamento: [Fontes, idioma, período, volume, diversidade regional e socioeconômica.]

2.2 Dados de operação: [O que a solução coleta durante o uso e para que finalidade.]

2.3 Tratamento de dados de menores: [Consentimento, minimização, pseudonimização, retenção, exclusão.]

2.4 Localização dos dados: [País/região de armazenamento e processamento. Provedor de nuvem.]

## 3. Arquitetura e funcionamento

3.1 Modelo utilizado: [Descrição em linguagem acessível da arquitetura. Não exige revelar código proprietário, mas deve permitir compreensão da lógica geral.]

3.2 Processo de inferência: [Como vai dos dados de entrada ao resultado. Variáveis que mais influenciam.]

3.3 Atualizações: [Frequência de retreinamento, dados utilizados, validação antes de deploy.]

## 4. Desempenho e avaliação

4.1 Métricas: [Acurácia, precisão, recall, F1, kappa de Cohen, ou outras pertinentes. Apresente valores.]

4.2 Avaliação por subgrupo: [Resultados por região, série, gênero, raça, escola urbana/rural, nível socioeconômico.]

4.3 Testes de viés: [Testes realizados e resultados. Se não realizados, plano para fazê-lo.]

4.4 Evidências de impacto pedagógico: [Metodologia, escala, contexto, limitações.]

## 5. Limitações e riscos conhecidos

5.1 Cenários de falha: [Quando o modelo erra ou tem desempenho inferior.]

5.2 Risco de alucinação: [Para generativos: risco e medidas de mitigação.]

5.3 Risco de dependência cognitiva: [Como a solução mitiga.]

5.4 Riscos não mitigados: [Lista honesta.]

## 6. Supervisão humana

6.1 Pontos de decisão humana: [Quando o professor/gestor intervém. O que pode ser anulado.]

6.2 Mecanismos de contestação: [Como alunos/famílias contestam decisões da IA.]

6.3 Formação oferecida: [Treinamento para interpretação e supervisão.]

## 7. Portabilidade e encerramento

7.1 Licenciamento: [SaaS, perpétua, outro.]

7.2 Portabilidade: [Formatos de exportação, procedimento, prazo.]

7.3 Encerramento: [O que acontece com dados ao fim do contrato. Exclusão.]

7.4 Propriedade dos dados: [Declaração de que dados pertencem à rede, não ao fornecedor.]

## 8. Histórico de versões

| Versão | Data | Principais alterações |
|--------|------|----------------------|
| | | |

## Quem usa este template e como

**EdTech:** preencha antes de ofertar para redes públicas. Seja honesto sobre limitações. Anexe à proposta técnica.

**Gestor:** use como referência para avaliar soluções. Exija documentação equivalente no TR.

**Intermediário:** use como parte da rubrica de credenciamento. Campos essenciais para triagem: 1, 2.1-2.3, 4.1, 5, 6.
