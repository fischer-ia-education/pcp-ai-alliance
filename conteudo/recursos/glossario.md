---
title: "Glossário: IA na Educação"
subtitle: "Conceitos essenciais para entender e contratar inteligência artificial na educação pública"
author: "Aliança de IA para a Educação"
date: "2026"
persona: recursos
tipo: glossario
---

# Glossário: IA na Educação

> Este glossário reúne os principais conceitos utilizados no Guia Prático de Contratação de IA na Educação, organizados por tema para facilitar a consulta.

---

## Inteligência Artificial x Tecnologia Digital Convencional

A distinção fundamental que todo gestor público e EdTech precisa dominar:

| | **Tecnologia Digital Convencional** | **Solução de Inteligência Artificial** |
|-|------------------------------------|-----------------------------------------|
| **Como opera** | Regras estáticas, lógica binária e previsível | Algoritmos probabilísticos aplicados a grandes volumes de dados |
| **Tipo de sistema** | Ferramenta de execução, não de interpretação | Sistema de inferência que aprende e se aperfeiçoa |
| **Quando erra** | O erro está no código; pode ser corrigido diretamente | O erro pode estar nos dados de treinamento, na inferência estatística ou na interpretação contextual: difícil de rastrear |
| **Interação** | Humano-a-computador (menus, funções limitadas) | Semelhante à relação humano-a-humano (linguagem natural, ampla gama de comandos) |
| **Exemplos** | Sistemas de matrícula, planilhas, correção de formulários | Tutoria inteligente, avaliação adaptativa, análise preditiva |

---

## Conceitos de IA

**Algoritmo**
Conjunto de regras ou instruções que um sistema computacional executa para resolver um problema ou tomar uma decisão. Em IA, algoritmos aprendem com dados, em vez de apenas seguir regras fixas.

**Aprendizado de Máquina (Machine Learning)**
Tipo de IA em que a máquina aprende com dados, ajustando modelos estatísticos sem que alguém escreva todas as regras à mão. É a base da maioria das soluções de IA educacional disponíveis no mercado.

**IA Generativa**
Tipo de aprendizado de máquina que, usando redes neurais profundas e modelos de linguagem natural, aprende com grandes volumes de dados e passa a gerar novos conteúdos: textos, imagens, códigos, áudio, vídeo: a partir de comandos do usuário. Ferramentas como ChatGPT, Gemini, Copilot e Claude são exemplos. São as mais usadas por estudantes e professores.

**IA Simbólica (IA de Primeira Geração)**
Sistema de especialistas baseado em regras estabelecidas pelo conhecimento humano. Opera com inferências lógicas encadeadas dentro dos limites do que foi codificado. Mais próxima das tecnologias convencionais; não é o foco deste guia.

**Modelo (de IA)**
A "inteligência" de um sistema de IA: o conjunto de parâmetros matemáticos que resultam do treinamento sobre um conjunto de dados. Um modelo de linguagem, por exemplo, é o resultado de treinar uma rede neural em bilhões de textos.

**Dados de Treinamento**
O conjunto de dados usado para treinar um modelo de IA. A qualidade, diversidade e representatividade dos dados de treinamento determinam, em grande medida, a qualidade e os possíveis vieses do modelo resultante.

**Inferência**
O processo pelo qual um modelo de IA já treinado aplica o que aprendeu a novos dados para gerar uma previsão, classificação ou recomendação. É o que acontece quando um aluno interage com uma plataforma adaptativa: o sistema *infere* qual exercício propor.

**Alucinação**
Fenômeno em que um sistema de IA (especialmente IA generativa) gera informações que parecem autênticas mas são factualmente incorretas. Nome oriundo do fato de que o sistema "vê" (gera) algo que não existe.

---

## Conceitos de Governança Algorítmica

**Transparência Algorítmica**
Disponibilização de informações essenciais sobre o comportamento da IA, seus limites e seu desempenho: mostrando *como* o sistema opera. Dois níveis:
- **Técnico-operacional:** documentação para auditores e especialistas (tipo de modelo, dados, métricas, vieses identificados)
- **Pedagógico-formativo:** explicação para professores e estudantes, apoiando a interpretação crítica dos resultados

**Explicabilidade**
Revela o "porquê" de um resultado específico ter sido gerado: fornece justificativas interpretáveis por humanos para uma decisão ou recomendação automatizada. Exemplo: um sistema explicável não apenas diz que um aluno está "em risco", mas explica quais indicadores levaram a essa conclusão.

**Auditabilidade**
Capacidade de rastrear e verificar retrospectivamente como o sistema de IA chegou a determinados resultados. Exige que logs e histórico de decisões sejam mantidos e acessíveis.

**Supervisão Humana (Human-in-the-Loop)**
Princípio segundo o qual nenhuma decisão pedagógica de alto impacto é delegada ao algoritmo de forma autônoma. O professor ou gestor sempre tem a palavra final. A supervisão humana não é evento único: é regime contínuo de monitoramento.

**Corresponsabilidade**
Distribuição clara das responsabilidades entre fornecedor, rede de ensino e educadores em cada fase do ciclo de uso da IA. O contrato deve especificar quem responde pelo quê: e por quê quando algo dá errado.

**Caixa-Preta (Black Box)**
Sistema de IA cujo funcionamento interno não está aberto à inspeção, sendo seus resultados inexplicáveis ou incompreensíveis para os usuários. Contratos de IA não devem aceitar sistemas de caixa-preta sem salvaguardas de explicabilidade.

---

## Riscos e Problemas

**IA Embutida / Contratação Invisível**
Fenômeno em que plataformas digitais incorporam algoritmos de IA em suas funcionalidades sem que tais mecanismos sejam explicitados nos contratos. A IA chega como "plataforma inteligente" ou "avaliação adaptativa", sem ser declarada.

**Opacidade Funcional**
Situação em que professores e gestores interagem com sistemas que aparentam ser softwares comuns, mas na prática tomam decisões com base em inferências estatísticas sobre trajetórias escolares: sem que ninguém saiba exatamente como.

**Viés Algorítmico (Discriminação Algorítmica)**
Quando um sistema de IA produz resultados sistematicamente desfavoráveis a determinados grupos (por raça, gênero, classe social, dialeto). Geralmente decorre de vieses presentes nos dados de treinamento ou na definição do problema.

**Lock-in Tecnológico**
Situação em que a administração pública se torna excessivamente dependente da tecnologia ou infraestrutura proprietária de um fornecedor específico, tornando inviável a migração para outra solução.

**Assimetria de Informação**
Desequilíbrio de conhecimento técnico entre o fornecedor de IA e o gestor público que contrata. O fornecedor conhece profundamente seu sistema; o gestor, frequentemente, depende do fornecedor para compreendê-lo.

**Profecia Autorrealizável**
Quando um sistema preditivo que rotula alunos como "em risco" leva professores a reduzir expectativas e esforços pedagógicos em relação a esses estudantes, consolidando o fracasso escolar antes mesmo que ele ocorra.

**Falsa Maestria**
Resultados impressionantes gerados pela IA que mascaram a falta de competência real do aluno, criando uma ilusão de aprendizado que não se traduz em conhecimento duradouro ou transferível.

---

## Conceitos Contratuais

**Portabilidade de Dados**
Direito da rede pública de obter todos os dados gerados no âmbito do contrato em formato aberto e interoperável ao final da relação contratual, sem custo adicional.

**Plano de Saída (Exit Plan)**
Documento que especifica como se dará a transição ao encerrar um contrato de IA: portabilidade de dados, continuidade pedagógica, comunicação com a comunidade escolar e migração para outra solução.

**Model Card**
Documento técnico que descreve um modelo de IA de forma padronizada: sua finalidade, dados de treinamento, métricas de desempenho, limitações e riscos conhecidos. Equivalente ao "manual do produto" para sistemas de IA.

**RIPD: Relatório de Impacto à Proteção de Dados**
Documento exigido pela LGPD quando o tratamento de dados pessoais pode gerar riscos às liberdades civis e aos direitos fundamentais. Em contratos de IA educacional que tratam dados de crianças e adolescentes, o RIPD é prático obrigatório.

**DPO: Encarregado de Proteção de Dados**
Pessoa indicada pelo controlador ou operador para atuar como canal de comunicação entre a organização, os titulares dos dados e a ANPD. Exigido pela LGPD para organizações que tratam dados pessoais em larga escala.

**SLA: Service Level Agreement (Acordo de Nível de Serviço)**
Acordo contratual que define os padrões mínimos de desempenho do fornecedor (disponibilidade da plataforma, tempo de resposta, etc.) e as consequências do descumprimento (multas, rescisão).

**Inexigibilidade de Licitação**
Modalidade de contratação direta prevista no art. 74 da Lei nº 14.133/2021, utilizada quando a competição é inviável: por exemplo, quando a solução de IA é comprovadamente exclusiva de um único fornecedor.

**Pregão Eletrônico**
Modalidade licitatória para bens e serviços comuns, com disputa de lances em sistema eletrônico. Adequada para soluções de IA cuja especificação pode ser objetivamente definida.

**CPSI: Contratação Pré-Comercial para Solução Inovadora**
Instrumento legal que permite ao poder público financiar pesquisa e desenvolvimento de soluções que ainda não existem no mercado, com ciclos de teste e critérios de go/no-go antes de cada nova fase de financiamento.

---

## Conceitos Pedagógicos

**Aprendizado Adaptativo**
Modelo de ensino em que a sequência de atividades, o nível de dificuldade e os conteúdos são ajustados automaticamente pela IA com base no desempenho e histórico de cada aluno.

**Tutoria Inteligente (ITS: Intelligent Tutoring System)**
Sistema de IA que mantém conversas pedagógicas flexíveis, ajustando linguagem, ritmo e dificuldade de acordo com as necessidades e o histórico de cada aluno. Pode oferecer feedback formativo imediato.

**Feedback Formativo**
Devolutiva sobre o processo de aprendizagem, não apenas sobre o resultado final. Um sistema de IA com feedback formativo explica por que uma resposta está incorreta e sugere como melhorar.

**Letramento Algorítmico**
Capacidade de gestores e professores de reconhecer, questionar e supervisionar ativamente as soluções de IA adquiridas. Não é expertise técnica em IA: é a capacidade de usar a IA de forma crítica, segura e pedagogicamente intencional.

**Intencionalidade Pedagógica**
Princípio segundo o qual a adoção de IA deve ser guiada por um propósito pedagógico claro: a IA é meio, não fim. Uma adoção sem intencionalidade tende a reproduzir práticas existentes sem agregar valor.

---

*Aliança de IA para a Educação | Instituto Jataí | 2026*
