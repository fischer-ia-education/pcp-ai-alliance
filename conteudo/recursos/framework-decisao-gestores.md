---
title: "Framework de Decisão para Contratação de IA na Educação"
subtitle: "Ferramentas de Apoio à Decisão para Gestores Públicos"
author: "Aliança de IA para a Educação"
date: "2026"
persona: recursos
tipo: framework
---

# Framework de Decisão para Contratação de IA na Educação

---

## 1. Árvore de Decisão: Devo Contratar IA?

Use esta sequência de perguntas para avaliar se a contratação de IA é o caminho adequado:

```
┌─────────────────────────────────────────────────────┐
│ Há um problema pedagógico claramente definido?       │
└──────────┬──────────────────────────┬───────────────┘
           │ SIM                      │ NÃO
           ▼                          ▼
┌──────────────────────┐   ┌──────────────────────────┐
│ Uma solução           │   │ PARE: Defina primeiro o   │
│ convencional resolve? │   │ problema pedagógico.      │
└────┬─────────────┬───┘   │ IA é meio, não fim.       │
     │ SIM         │ NÃO   └──────────────────────────┘
     ▼             ▼
┌────────────┐  ┌────────────────────────────────────┐
│ Use a       │  │ A rede tem capacidade institucional │
│ solução     │  │ mínima? (equipe, letramento, infra) │
│ convencional│  └────┬──────────────────────┬────────┘
└────────────┘       │ SIM                   │ NÃO
                     ▼                       ▼
          ┌─────────────────────┐  ┌─────────────────────┐
          │ A infraestrutura     │  │ INVISTA primeiro em  │
          │ escolar é adequada?  │  │ capacitação e        │
          │ (conectividade,      │  │ letramento           │
          │ hardware)            │  │ algorítmico.         │
          └──┬───────────────┬──┘  └─────────────────────┘
             │ SIM           │ NÃO
             ▼               ▼
  ┌────────────────────┐  ┌────────────────────────────┐
  │ PROSSIGA com a     │  │ Considere soluções de IA   │
  │ contratação.       │  │ offline/desplugada ou      │
  │ Use o Checklist    │  │ invista em infraestrutura  │
  │ da Jornada.        │  │ antes de contratar.        │
  └────────────────────┘  └────────────────────────────┘
```

---

## 2. Matriz de Classificação de Risco

Inspirada na Avaliação de Impacto Algorítmico (AIA) canadense, esta matriz ajuda a definir o nível de governança necessário para cada tipo de solução.

| Nível | Impacto | Exemplos | Governança Exigida |
|-------|---------|----------|-------------------|
| **1. Baixo** | Decisões reversíveis, impacto breve | Chatbot para dúvidas administrativas, organização de grades horárias | Documentação técnica básica, monitoramento leve |
| **2. Moderado** | Influência sobre processo de aprendizagem, mas com supervisão humana direta | Recomendação de exercícios, sugestões de plano de aula, feedback formativo | Model Card, LGPD verificada, dashboards para professores, auditoria anual |
| **3. Alto** | Decisões que afetam trajetórias escolares | Correção automatizada de avaliações, diagnósticos de aprendizagem que orientam intervenções | Tudo do nível 2 + RIPD, auditorias pedagógicas e técnicas semestrais, mecanismos de contestação, supervisão humana obrigatória |
| **4. Crítico** | Decisões irreversíveis ou com impacto permanente | Sistemas preditivos que rotulam alunos "em risco", ferramentas que influenciam aprovação/reprovação, reconhecimento facial | Tudo do nível 3 + avaliação de impacto algorítmico completa, revisão por especialistas externos, testes rigorosos de vieses, plano de reversibilidade obrigatório |

**Regra geral:** quanto maior o impacto sobre os direitos e as trajetórias dos estudantes, maior deve ser o escrutínio técnico e ético.

---

## 3. Comparativo de Modalidades de Contratação

| Critério | Inexigibilidade | Pregão Eletrônico | Parceria Intermediada | CPSI (Inovação) |
|----------|----------------|-------------------|----------------------|----------------|
| **Quando usar** | Solução exclusiva (fornecedor único) | Especificações objetivamente definidas | Quando há instituição parceira qualificada (Sebrae, universidade, fundação) | Quando a solução ainda não existe no mercado |
| **Base legal** | Art. 74, Lei 14.133/2021 | Lei 14.133/2021 | Art. 75, XV, Lei 14.133/2021 | Art. 13, Lei Complementar 182/2021 |
| **Vantagens** | Agilidade, acesso a soluções especializadas | Competitividade de preço, transparência | Curadoria e validação prévia, menor risco | Foco no problema (não na solução), aprendizado institucional |
| **Riscos** | Sem competição, risco de lock-in, preço não otimizado | Pode priorizar preço sobre qualidade pedagógica | Depende da qualidade do intermediário | Processo mais longo e complexo |
| **Caso real** | Joinville/SC: Letrus (R$2,1M) | Rio Verde/GO: Herby Vision (R$211K) | RN: Sebrae/LIZE (R$15K) | Inspiração: contratação de soluções inovadoras para educação |
| **Recomendação** | Use com análise jurídica rigorosa e com salvaguardas contratuais reforçadas | Adequado quando há múltiplos fornecedores e requisitos objetivos | Bom para municípios com menor capacidade institucional | Ideal para soluções inovadoras em teste |

---

## 4. As 8 Perguntas do Contrato como Governança

Um contrato de IA bem estruturado deve responder a estas 8 perguntas. Para cada uma, descrevemos o que esperar como "boa resposta" e os sinais de alerta.

| # | Pergunta | Boa Resposta | Sinal de Alerta |
|---|----------|-------------|-----------------|
| 1 | **Para quê?** Qual a finalidade pedagógica? | Propósito específico e mensurável (ex.: "reduzir defasagem em leitura no 5º ano") | Respostas genéricas ("melhorar a educação", "modernizar a rede") |
| 2 | **Com o quê?** Quais dados, bases e métodos de validação? | Fontes de dados documentadas, métodos de validação explícitos, dados em português | "Dados proprietários" sem detalhamento, treinamento exclusivamente em inglês |
| 3 | **Como?** Com base em quais métricas e logs? | Métricas claras de desempenho, logs acessíveis, trilhas de auditoria | Sem métricas definidas, "caixa-preta" |
| 4 | **Para quem?** Quem supervisiona, com que autoridade? | Papéis definidos (gestor, professor, fiscal de contrato), poder de revisão/anulação | Ninguém designado, professor sem poder de intervenção |
| 5 | **Com que segurança?** Proteção de dados e mitigação de vieses? | LGPD verificada, RIPD disponível, testes de vieses, criptografia | Sem menção a proteção de dados, sem testes de vieses |
| 6 | **Até quando?** Manutenção, atualização, descontinuação? | Plano de atualizações, critérios para descontinuação, plano de saída | Contrato sem prazo de revisão, sem previsão de saída |
| 7 | **E se falhar?** Reversibilidade e correção? | Mecanismos de contestação, reversibilidade de decisões, plano de incidentes | "Garantimos 99% de acurácia" sem plano para os 1% de erro |
| 8 | **Com que legado?** Dados e aprendizados retornam à rede? | Dados pertencem à rede, exportação garantida, compartilhamento de aprendizados | Dados ficam com o fornecedor, lock-in contratual |

---

## 5. Matriz de Responsabilidades (RACI)

**R** = Responsável | **A** = Aprovador | **C** = Consultado | **I** = Informado

| Atividade | Gestor / Secretário | Equipe TI | Equipe Pedagógica | Jurídico | Fornecedor (EdTech) | Professores |
|-----------|:--:|:--:|:--:|:--:|:--:|:--:|
| Definir problema pedagógico | A | I | R | I | C | C |
| Diagnosticar capacidade institucional | A | R | C | I | I | I |
| Elaborar Termo de Referência | A | R | C | C | I | I |
| Avaliar soluções disponíveis | A | R | R | C | I | C |
| Definir salvaguardas contratuais | A | C | C | R | I | I |
| Validar conformidade LGPD | A | C | I | R | R | I |
| Treinar professores | I | C | A | I | R | R |
| Monitorar impacto pedagógico | A | I | R | I | C | R |
| Realizar auditorias técnicas | A | R | I | C | C | I |
| Realizar auditorias pedagógicas | A | I | R | I | C | R |
| Gerenciar dados e segurança | A | R | I | C | R | I |
| Processar contestações | A | I | R | C | C | I |
| Decidir sobre descontinuação | R | C | C | C | I | I |

---

## 6. Indicadores de Sucesso e Sinais de Alerta por Fase

### Primeiros 3 meses (Implantação)

| Indicador de Sucesso | Sinal de Alerta |
|---------------------|-----------------|
| Professores treinados e usando a ferramenta | Professores não foram capacitados ou resistem ao uso |
| SLAs sendo cumpridos (disponibilidade, suporte) | Plataforma instável, suporte lento |
| Dados de uso sendo gerados e acessíveis | Sem acesso a relatórios ou métricas |

### 6 meses (Consolidação)

| Indicador de Sucesso | Sinal de Alerta |
|---------------------|-----------------|
| Primeiras evidências de impacto pedagógico | Nenhuma melhora mensurável na aprendizagem |
| Professores usando dashboards e intervindo quando necessário | Professores delegando decisões acriticamente à IA |
| Nenhum incidente de segurança de dados | Vazamentos, acesso não autorizado ou dados expostos |

### 12 meses (Avaliação)

| Indicador de Sucesso | Sinal de Alerta |
|---------------------|-----------------|
| Impacto pedagógico documentado e positivo | Evidências de "preguiça cognitiva" ou aprendizado superficial |
| Auditorias realizadas sem achados críticos | Vieses detectados, falhas não corrigidas |
| Comunidades de prática ativas entre professores | Ferramenta subutilizada ou abandonada |
| Decisão informada sobre renovação/descontinuação | Renovação automática sem avaliação |

---

*Material derivado da publicação "Contratação Pública de Soluções de IA na Educação", da Aliança de IA para a Educação, em parceria com o Instituto Jataí.*

*Aliança de IA para a Educação | Instituto Jataí | 2026*
