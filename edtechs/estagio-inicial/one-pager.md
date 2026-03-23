---
title: "Prontidão Mínima: O que Sua EdTech Precisa Ter Antes de Bater na Porta de uma Secretaria"
subtitle: "Essencial, importante e diferencial para EdTechs em estágio inicial"
author: "Aliança de IA para a Educação"
date: "2026"
persona: edtechs
sub_persona: estagio-inicial
tipo: one-pager
---

# Prontidão Mínima: O que Sua EdTech Precisa Ter Antes de Bater na Porta de uma Secretaria

Se você está desenvolvendo uma solução de IA para educação e pensa em algum momento vendê-la para redes públicas de ensino, vale construir prontidão para isso desde agora. Não porque o setor público vá bater na sua porta amanhã, mas porque decisões de arquitetura, de dados e de modelo de negócio tomadas no início são muito mais caras de corrigir depois.

Este resumo separa o que é essencial (sem isso, você não entra no jogo), o que é importante (aumenta muito sua chance de sucesso) e o que é diferencial (destaca, mas não bloqueia).

## Essencial: sem isso, não adianta avançar

Na dimensão regulatória, sua empresa precisa ter CNPJ ativo no Brasil. Não há exceção: a administração pública só contrata quem tem personalidade jurídica brasileira. Precisa também ter uma política de privacidade publicada e minimamente aderente à LGPD, com atenção especial ao tratamento de dados de crianças e adolescentes (consentimento dos responsáveis legais, finalidade educacional explícita, coleta mínima). E precisa ter as certidões de regularidade fiscal e trabalhista em dia, porque são exigência de habilitação em qualquer processo licitatório.

Na dimensão técnica, o produto precisa funcionar em condições reais de escola pública brasileira. Isso significa: rodar em Chromebooks e celulares Android de entrada, funcionar com conexão instável (latência alta, quedas frequentes), não exigir instalação de software proprietário nos dispositivos da rede. Se a solução não funciona nessas condições, o contrato pode até ser assinado, mas a implementação fracassa e o dinheiro público é desperdiçado. Também é essencial que a solução permita a extração de dados em formato aberto (CSV, JSON), para evitar dependência tecnológica (lock-in).

Na dimensão pedagógica, a solução precisa resolver um problema pedagógico concreto e nomeável. "Usamos IA" não é proposta de valor para o gestor público. "Reduzimos o tempo de correção de redações de três semanas para três dias, permitindo feedback formativo dentro do ciclo de aula" é. Precisa estar alinhada à BNCC ou ser configurável para tal, porque redes públicas operam com a Base Nacional como referência curricular. E precisa preservar a agência do professor: o educador consegue revisar, contextualizar e, se necessário, anular as recomendações ou resultados da IA. Solução que tira o professor do circuito decisório enfrenta resistência justificada e risco pedagógico real.

## Importante: aumenta muito sua chance de sucesso

Ter um encarregado de dados (DPO) nomeado formalmente, mesmo que acumulando função. Ter uma política de retenção e exclusão de dados documentada (não apenas "cumprimos a LGPD", mas "deletamos dados de alunos inativos após X meses, conforme Y critério"). Ter API documentada para integração com sistemas de gestão escolar (i-Educar, SED, SGE, plataformas estaduais). Ter dados de treinamento do modelo em português brasileiro (não apenas português europeu ou tradução automática do inglês). Ter alguma evidência de uso, mesmo que não seja estudo de impacto rigoroso: dados de uso em escolas parceiras, relatos estruturados de implementação, pré/pós em indicadores simples. Isso ajuda o gestor a montar o Estudo Técnico Preliminar (ETP) e dá segurança na justificativa de compra.

## Diferencial: destaca, mas não bloqueia

Ter um Model Card ou ficha técnica do modelo documentada (descrevendo dados de treinamento, métricas de acurácia, limitações conhecidas, cenários de falha). Poucas edtechs brasileiras fazem isso hoje; quem fizer se posiciona como referência de transparência. Ter um RIPD (Relatório de Impacto à Proteção de Dados) elaborado voluntariamente. Ter estudo de impacto com metodologia robusta (experimental ou quase-experimental). Poucas edtechs terão isso, e está tudo bem, mas quando existe, é um ativo poderoso, especialmente para justificar contratação por inexigibilidade, porque o argumento de singularidade fica mais forte quando há evidência de que aquela solução específica gera resultados comprovados que outras não demonstraram.
