---
title: "Entrando no Mercado Brasileiro: Guia para EdTechs Internacionais"
subtitle: "Orientações para empresas estrangeiras que desejam oferecer soluções de IA para redes públicas de educação no Brasil"
author: "Aliança de IA para a Educação"
date: "2026"
persona: edtechs
sub_persona: internacional
tipo: guia
---

# Entrando no Mercado Brasileiro: Guia para EdTechs Internacionais

>
> **Este guia complementa o [Guia para EdTechs](guia-edtechs.md).** Leia o guia principal primeiro: ele cobre procurement, salvaguardas, estudos de caso e orientações que se aplicam a todas as EdTechs. Este documento aborda os desafios **adicionais** enfrentados por empresas internacionais.

---

## 1. Por que o Brasil é Diferente

O Brasil não é um mercado, são **5.570 mercados**. Cada município tem autonomia para contratar suas próprias soluções educacionais. Não existe uma "aprovação nacional" que abra todas as portas. Uma venda para São Paulo não garante entrada em Salvador.

Além disso, o debate brasileiro sobre IA na educação carrega uma preocupação central: **o risco de homogeneização cultural**. A publicação que originou estes materiais alerta explicitamente contra "o predomínio de dados em inglês e de padrões do Norte Global, que gera o risco de apagamento de culturas locais, de regionalismos e de saberes indígenas". Gestores e reguladores estão cada vez mais atentos a esse risco.

Isso não significa que EdTechs internacionais não são bem-vindas. Significa que **demonstrar compromisso genuíno com a adaptação ao contexto brasileiro** não é apenas boa prática, é pré-requisito para credibilidade.

**Dados do mercado:**
- 37% dos alunos e 43% dos professores já usam IA (TIC Educação 2024)
- 15 contratações públicas de IA educacional mapeadas entre 2024-2026, nenhuma com documentação específica de IA
- O Plano Brasileiro de IA (PBIA) tem 6 ações de impacto na educação
- A regulação está em construção (PL 2338/2023, Marco Legal da IA em tramitação)

---

## 2. Presença Jurídica no Brasil

### O requisito fundamental

Para participar de licitações públicas brasileiras, sua empresa precisa de um **CNPJ** (Cadastro Nacional da Pessoa Jurídica), o equivalente ao EIN (EUA), Company Number (UK) ou CIF (UE). Sem CNPJ, não há como assinar contratos com o poder público.

### Três caminhos para estabelecer presença

| Opção | O que é | Timeline | Custo estimado | Quando usar |
|-------|---------|----------|---------------|-------------|
| **Subsidiária (LTDA ou S.A.)** | Empresa brasileira com capital estrangeiro | 2–4 meses | R$ 15–30 mil (honorários + taxas) | Quando há demanda confirmada e intenção de longo prazo |
| **Filial de empresa estrangeira** | Extensão da empresa-mãe no Brasil | 3–6 meses (requer aprovação federal) | R$ 30–50 mil | Quando a empresa quer manter controle centralizado |
| **Parceria com empresa brasileira** | Sem constituição própria; a empresa local é a face jurídica | 1–2 meses (acordo contratual) | R$ 5–15 mil (jurídico do acordo) | Melhor caminho para testar o mercado com baixo risco |

### O que você precisa para constituir uma empresa

- **Contrato social** traduzido e registrado na Junta Comercial do estado
- **Inscrição no CNPJ** junto à Receita Federal
- **Inscrição estadual e municipal** (para ISS e ICMS, conforme o tipo de atividade)
- **Representante legal no Brasil:** pessoa física com CPF, residente no país, com poderes para assinar contratos e responder em processos judiciais
- **Conta bancária em instituição brasileira:** necessária para receber pagamentos públicos em R$
- **Certidões negativas:** após constituição, manter atualizadas: CND (débitos federais), CNDT (débitos trabalhistas), CRF (FGTS)

**Recomendação:** Contrate um escritório jurídico brasileiro especializado em direito empresarial e investimento estrangeiro. O custo se paga rapidamente em tempo economizado e erros evitados.

---

## 3. LGPD para Dados Internacionais

A **Lei Geral de Proteção de Dados (LGPD, Lei 13.709/2018)** é a lei brasileira de proteção de dados, inspirada no GDPR europeu. Ela se aplica a **qualquer tratamento de dados de pessoas localizadas no Brasil**, independentemente de onde os dados são processados ou armazenados.

### Transferência internacional de dados

Se sua solução processa dados fora do Brasil (em servidores nos EUA, Europa ou outro país), os Artigos 33 a 35 da LGPD regulam essa transferência. As bases legais mais relevantes para EdTechs são:

| Base legal | O que significa | Status atual |
|-----------|----------------|-------------|
| **País com nível adequado de proteção** | A ANPD (Autoridade Nacional de Proteção de Dados) reconhece que o país tem proteção equivalente | Lista ainda em construção pela ANPD |
| **Cláusulas contratuais padrão** | Contrato entre exportador e importador de dados com garantias específicas | Alternativa mais utilizada enquanto a lista de países não é definida |
| **Consentimento específico** | Autorização explícita do titular (ou responsável legal, no caso de crianças e adolescentes) | Válida, mas operacionalmente difícil em escala |

### Proteção reforçada para crianças e adolescentes

O Art. 14 da LGPD estabelece que dados de **crianças e adolescentes** devem ser tratados com **proteção máxima**. Isso significa:
- Consentimento **explícito** de pais ou responsáveis legais
- Coleta apenas de dados **estritamente necessários** para a finalidade pedagógica
- Proibição de uso para fins de publicidade, perfilamento comportamental ou comercialização
- Exclusão obrigatória dos dados após o fim do vínculo educacional

### Recomendação prática

Considere hospedar dados de alunos brasileiros em **data centers localizados no Brasil** (AWS São Paulo, Azure Brasil Sul, GCP Southamerica-east1). Isso:
- Elimina questões sobre transferência internacional
- Demonstra compromisso com soberania de dados (preocupação crescente no Brasil)
- Simplifica a conformidade contratual
- Pode ser exigido em editais

**Você precisará de um DPA (Data Processing Agreement)**, acordo de processamento de dados, com cada rede de ensino contratante, especificando: quais dados são tratados, onde ficam armazenados, quem pode acessá-los, e o que acontece com eles ao fim do contrato.

---

## 4. Adaptação Cultural e Pedagógica

### BNCC: o que é e por que bloqueia sua entrada sem alinhamento

A **Base Nacional Comum Curricular (BNCC)** é o documento que define as aprendizagens essenciais que todos os alunos brasileiros devem desenvolver ao longo da educação básica. Ela organiza:

- **10 competências gerais** (pensamento crítico, repertório cultural, comunicação, etc.)
- **Áreas de conhecimento** por etapa (Educação Infantil, Ensino Fundamental, Ensino Médio)
- **Habilidades específicas** por ano/série, codificadas (ex.: EF05MA01 = Ensino Fundamental, 5º ano, Matemática, habilidade 01)

**Uma solução de IA educacional que não se alinha à BNCC é praticamente invendável para redes públicas.** Gestores precisam demonstrar que investimentos em tecnologia contribuem para os objetivos curriculares nacionais. Se sua solução foi desenvolvida com base no Common Core (EUA), National Curriculum (UK) ou outro referencial estrangeiro, será necessário um **trabalho de mapeamento e adaptação** às habilidades da BNCC.

### Língua portuguesa brasileira

| O que NÃO funciona | O que funciona |
|--------------------|----------------|
| Modelos treinados apenas em inglês com tradução automática | Modelos treinados nativamente em português brasileiro (PT-BR) |
| Interface traduzida do inglês ou do português europeu (PT-PT) | Interface concebida em PT-BR, com terminologia pedagógica brasileira |
| Feedback gerado em linguagem acadêmica formal | Feedback acessível, adaptado ao contexto escolar brasileiro |
| Dados de treinamento exclusivamente do "Norte Global" | Dados que incluam diversidade regional brasileira |

**Atenção:** O português europeu (PT-PT) e o português brasileiro (PT-BR) diferem significativamente em vocabulário, gramática e pronúncia. Uma solução em PT-PT será percebida como estrangeira e pouco natural.

### Contexto educacional brasileiro

Sua solução precisa funcionar na **realidade** das escolas públicas brasileiras, não em um cenário idealizado:

- **Turmas de 35 a 45 alunos:** muito maiores que a média OCDE
- **Infraestrutura precária:** muitas escolas sem internet estável ou com poucos dispositivos
- **Dupla jornada docente:** professores frequentemente trabalham em 2 ou 3 escolas
- **Diversidade radical:** na mesma rede pública convivem escolas urbanas bem equipadas e escolas rurais sem conectividade, populações indígenas, quilombolas e imigrantes
- **Desigualdade socioeconômica:** o aluno que mais precisa de apoio é frequentemente o que menos tem acesso à tecnologia

### Riscos de viés cultural

Gestores e reguladores brasileiros estão atentos ao risco de que soluções estrangeiras perpetuem **normas pedagógicas do "Norte Global"**. Especificamente:

- **Testes de vieses** devem incluir categorias demográficas brasileiras: raça (conforme classificação do IBGE: branca, preta, parda, amarela, indígena), gênero, regionalismo (Nordeste vs. Sul, por exemplo), classe socioeconômica
- **Referências culturais** nos conteúdos devem incluir contextos brasileiros (não apenas europeus ou norte-americanos)
- **Padrões de avaliação** devem respeitar a pedagogia brasileira, que valoriza formação integral e pensamento crítico (não apenas desempenho em testes padronizados)

---

## 5. Estratégias de Entrada no Mercado

### Opção A: Parceria com EdTech brasileira (recomendada para começar)

A forma **mais rápida e segura** de entrar no mercado. A EdTech brasileira traz:
- CNPJ, certidões e habilitação jurídica
- Conhecimento do processo de licitação e relação com secretarias
- Entendimento do contexto pedagógico e cultural
- Credibilidade local e rede de contatos

Vocês trazem: tecnologia, capital, experiência internacional, escala.

**Onde encontrar parceiros:**
- **ABEdTech** (Associação Brasileira de EdTechs): [abredtech.org](https://abredtech.org)
- **Bett Brasil:** maior evento de tecnologia educacional da América Latina (anual, em São Paulo)
- **Undime** (União dos Dirigentes Municipais de Educação): eventos regionais
- **Aliança de IA para a Educação:** [iaparaeducacao.org.br](http://iaparaeducacao.org.br)

**Atenção ao acordo de parceria:** Defina com clareza: propriedade intelectual, divisão de receita, responsabilidades contratuais e pedagógicas, cláusula de saída, e quem responde perante a rede contratante em caso de falha.

### Opção B: Parceria com organização intermediária

Organizações como **Sebrae, universidades e fundações** já atuam como intermediários entre EdTechs e redes públicas. O caso de Itajá/RN (R$ 15 mil, 4 meses, via Sebrae) demonstra que é possível entrar com **escopo de MVP e investimento baixo**, validando o product-market fit antes de escalar.

Vantagem: a organização intermediária já tem credibilidade junto aos municípios e pode facilitar o processo de credenciamento.

### Opção C: Subsidiária própria

Mais controle, mas mais investimento e tempo. Recomendável quando:
- Já há demanda confirmada ou contratos em negociação
- O volume de negócios justifica o custo fixo (R$ 200 mil+/ano com estrutura mínima)
- Há intenção estratégica de longo prazo no mercado brasileiro

**Dica:** Contrate um(a) gestor(a) local com experiência em vendas B2G (business-to-government) em educação. O conhecimento de como navegar secretarias, editais e prazos orçamentários é insubstituível.

### Caminho recomendado

```
Parceria / Intermediário → Piloto em 1-2 municípios → Validação de impacto
    → Decisão: escalar via parceria OU constituir subsidiária
```

---

## 6. Tributação e Finanças

### Impostos que incidem sobre EdTechs estrangeiras

| Imposto | Alíquota | Incidência | Quem paga |
|---------|----------|-----------|-----------|
| **ISS** (Imposto sobre Serviços) | 2–5% | Faturamento de serviços | Sua empresa (via CNPJ brasileiro) |
| **IRRF** (Imposto de Renda Retido na Fonte) | 15–25% | Remessas de lucros ao exterior | Retido pelo pagador brasileiro |
| **PIS/COFINS** | ~9,25% (regime não-cumulativo) | Faturamento | Sua empresa |
| **IOF** | 0,38% (câmbio) | Operações de câmbio (envio de recursos ao exterior) | Na operação de câmbio |

### Impacto prático

Se você fatura R$ 100 mil em um contrato público:
- ISS (~5%): R$ 5 mil
- PIS/COFINS (~9,25%): R$ 9.250
- IRRF na remessa (~15%): aplicado sobre o lucro remetido ao exterior
- **Resultado:** A tributação + câmbio podem reduzir a receita líquida em **30–40%** em relação ao valor bruto do contrato

### Outros pontos financeiros

- Contratos públicos são **sempre em Reais (R$)**, e o risco cambial é do fornecedor
- Prazos de pagamento: **30 a 90 dias** após liquidação (confirmação de que o serviço foi prestado)
- Planeje capital de giro para suportar esse ciclo
- **Recomendação:** Contrate um contador brasileiro desde o início. O custo (R$ 1.000–3.000/mês) se paga em conformidade e economia tributária.

---

## 7. Checklist Específico para EdTechs Internacionais

Use este checklist **em complemento ao [Checklist geral de EdTechs](checklist-edtechs.md)**, que cobre prontidão pedagógica, técnica, de privacidade e transparência.

### Presença jurídica
- [ ] Estratégia de entrada definida (parceria, intermediário ou subsidiária)
- [ ] CNPJ ativo (próprio ou via parceiro)
- [ ] Representante legal no Brasil designado
- [ ] Certidões negativas em dia (CND, CNDT, CRF)
- [ ] Conta bancária brasileira aberta

### Dados e privacidade
- [ ] Estratégia de hospedagem de dados definida (preferencialmente em data centers no Brasil)
- [ ] Mecanismo de transferência internacional de dados conforme LGPD Arts. 33-35
- [ ] DPA (Data Processing Agreement) modelo preparado
- [ ] Consentimento parental adaptado ao contexto brasileiro (em PT-BR)

### Adaptação cultural e pedagógica
- [ ] Solução em português brasileiro nativo (PT-BR), não tradução de inglês ou PT-PT
- [ ] Alinhamento à BNCC mapeado e documentado
- [ ] Dados de treinamento incluem conteúdo em PT-BR e contexto brasileiro
- [ ] Testes de vieses realizados com categorias demográficas brasileiras (IBGE)
- [ ] Solução testada em cenários de baixa conectividade

### Finanças e tributação
- [ ] Contador brasileiro contratado
- [ ] Estrutura tributária mapeada (ISS, PIS/COFINS, IRRF, IOF)
- [ ] Modelo de preços em R$ compatível com orçamentos públicos
- [ ] Capital de giro planejado para ciclos de pagamento de 30-90 dias

