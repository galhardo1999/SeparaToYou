# Product Requirements Document (PRD)
## SeparaToYou - Sistema de Separação Automática de Fotos por Reconhecimento Facial

---

### **Informações do Documento**
- **Versão:** 1.0
- **Data:** Janeiro 2025
- **Autor:** Alexandre Galhardo
- **Status:** Ativo
- **Última Atualização:** Janeiro 2025

---

## **1. Visão Geral do Produto**

### **1.1 Resumo Executivo**
O **SeparaToYou** é uma aplicação desktop desenvolvida em Python que utiliza tecnologia de reconhecimento facial para automatizar o processo de separação e organização de fotografias por pessoa identificada. O sistema é especialmente projetado para ambientes educacionais, eventos e organizações que precisam classificar grandes volumes de fotos de forma eficiente e precisa.

### **1.2 Problema a Ser Resolvido**
- **Problema Principal:** Separação manual de milhares de fotos por pessoa é um processo extremamente demorado e propenso a erros
- **Dor do Cliente:** Professores, organizadores de eventos e fotógrafos gastam horas organizando fotos manualmente
- **Impacto:** Perda de produtividade, erros de classificação e frustração dos usuários

### **1.3 Proposta de Valor**
- **Automação Completa:** Reduz o tempo de separação de fotos de horas para minutos
- **Alta Precisão:** Utiliza algoritmos avançados de reconhecimento facial (face_recognition e DeepFace)
- **Interface Intuitiva:** Design simples e amigável para usuários não técnicos
- **Relatórios Detalhados:** Geração automática de relatórios em Excel com estatísticas completas
- **Flexibilidade:** Suporte a processamento single-core e multi-core para diferentes tipos de hardware

---

## **2. Objetivos do Produto**

### **2.1 Objetivos Primários**
1. **Automatizar 95%** do processo de separação de fotos por pessoa
2. **Reduzir em 90%** o tempo necessário para organização de fotos
3. **Alcançar 85%** de precisão na identificação facial
4. **Processar até 10.000 fotos** em uma única sessão

### **2.2 Objetivos Secundários**
1. Gerar relatórios detalhados de distribuição de fotos
2. Suportar múltiplos formatos de imagem
3. Implementar sistema de backup e recuperação
4. Oferecer modo premium com funcionalidades avançadas

### **2.3 Métricas de Sucesso**
- **Taxa de Precisão:** ≥ 85% de identificações corretas
- **Performance:** Processar 100 fotos/minuto em hardware médio
- **Usabilidade:** Usuário consegue usar o sistema sem treinamento
- **Confiabilidade:** 99% de uptime durante processamento

---

## **3. Público-Alvo**

### **3.1 Usuário Primário**
- **Perfil:** Professores e coordenadores educacionais
- **Necessidades:** Organizar fotos de eventos escolares, formaturas, excursões
- **Características:** Conhecimento básico de informática, foco em eficiência
- **Volume:** 500-5.000 fotos por evento

### **3.2 Usuário Secundário**
- **Perfil:** Fotógrafos profissionais e organizadores de eventos
- **Necessidades:** Classificar fotos de casamentos, festas, eventos corporativos
- **Características:** Usuários mais técnicos, exigem alta qualidade
- **Volume:** 1.000-10.000 fotos por evento

### **3.3 Usuário Terciário**
- **Perfil:** Famílias e usuários domésticos
- **Necessidades:** Organizar fotos pessoais e familiares
- **Características:** Conhecimento limitado de tecnologia
- **Volume:** 100-1.000 fotos

---

## **4. Funcionalidades do Sistema**

### **4.1 Funcionalidades Principais**

#### **4.1.1 Separação Automática de Fotos**
- **Descrição:** Identifica rostos em fotos e separa por pessoa
- **Entrada:** Pasta com fotos gerais + pasta com fotos de referência dos alunos
- **Saída:** Pastas organizadas por nome de pessoa + pasta de não identificados
- **Algoritmos:** face_recognition (dlib) e DeepFace
- **Precisão:** Tolerância ajustável (0.4-0.6)
- **Formatos Suportados:** JPG, JPEG, PNG, WEBP, BMP, TIFF

#### **4.1.2 Processamento Multi-Core**
- **Descrição:** Utiliza múltiplos núcleos do processador para acelerar o processamento
- **Configuração:** Automática baseada no hardware disponível
- **Otimização:** Pool de processos com batch processing
- **Fallback:** Modo single-core para hardware limitado

#### **4.1.3 Geração de Relatórios**
- **Formato:** Excel (.xlsx)
- **Conteúdo:** 
  - Quantidade total de fotos por pessoa
  - Distribuição por pasta de origem
  - Estatísticas de processamento
  - Fotos não identificadas
- **Exportação:** Salvamento com timestamp automático

#### **4.1.4 Interface Gráfica Intuitiva**
- **Framework:** Tkinter com ttkbootstrap para design moderno
- **Componentes:**
  - Seleção de pastas com botões dedicados
  - Barra de progresso em tempo real
  - Log detalhado de operações
  - Controles de configuração (tolerância, multi-processing)

### **4.2 Funcionalidades Secundárias**

#### **4.2.1 Sistema de Login Premium**
- **Autenticação:** API REST para verificação de usuários premium
- **Controle de Acesso:** Funcionalidades avançadas apenas para usuários pagos
- **Segurança:** Validação de credenciais com timeout

#### **4.2.2 Pré-processamento de Imagens**
- **Redimensionamento:** Otimização automática para melhor performance
- **Validação:** Verificação de integridade de arquivos
- **Tratamento de Erros:** Separação de arquivos corrompidos

#### **4.2.3 Pós-processamento Inteligente**
- **Re-análise:** Segunda tentativa para fotos não identificadas
- **Ajuste de Tolerância:** Configuração automática para melhor precisão
- **Validação de Múltiplos Rostos:** Tratamento especial para fotos com várias pessoas

---

## **5. Requisitos Técnicos**

### **5.1 Requisitos de Sistema**

#### **5.1.1 Hardware Mínimo**
- **Processador:** Intel Core i3 ou AMD equivalente
- **Memória RAM:** 4 GB
- **Armazenamento:** 2 GB livres
- **Sistema Operacional:** Windows 10/11, macOS 10.14+, Linux Ubuntu 18.04+

#### **5.1.2 Hardware Recomendado**
- **Processador:** Intel Core i5/i7 ou AMD Ryzen 5/7
- **Memória RAM:** 8 GB ou superior
- **Armazenamento:** SSD com 5 GB livres
- **GPU:** Opcional para aceleração (CUDA compatível)

### **5.2 Dependências de Software**

#### **5.2.1 Bibliotecas Python**
```
Python >= 3.8
tkinter (incluído no Python)
ttkbootstrap >= 1.10.0
face_recognition >= 1.3.0
Pillow >= 10.0.0
opencv-python >= 4.8.0
pandas >= 2.0.0
openpyxl >= 3.1.0
numpy >= 1.24.0
deepface >= 0.0.79
requests >= 2.31.0
```

#### **5.2.2 Dependências do Sistema**
- **dlib:** Para face_recognition
- **CMake:** Para compilação do dlib
- **Visual Studio Build Tools:** Windows
- **Xcode Command Line Tools:** macOS

### **5.3 Arquitetura do Sistema**

#### **5.3.1 Estrutura de Arquivos**
```
SeparaToYou/
├── main.py                    # Ponto de entrada principal
├── main-login.py             # Versão com sistema de login
├── separaFotosMulti.py       # Motor de processamento principal
├── separaFotosMultiDeepFace.py # Versão com DeepFace
├── fazerRelatorio.py         # Gerador de relatórios
├── backup/                   # Versões anteriores
├── .gitignore               # Configuração Git
└── README.md                # Documentação
```

#### **5.3.2 Fluxo de Dados**
1. **Entrada:** Seleção de pastas pelo usuário
2. **Carregamento:** Leitura de fotos de referência
3. **Processamento:** Análise facial e comparação
4. **Classificação:** Separação em pastas por pessoa
5. **Relatório:** Geração de estatísticas
6. **Saída:** Estrutura organizada + relatório Excel

---

## **6. Experiência do Usuário (UX)**

### **6.1 Jornada do Usuário**

#### **6.1.1 Fluxo Principal**
1. **Inicialização:** Usuário abre o SeparaToYou
2. **Configuração:** Seleciona pasta de fotos gerais
3. **Referência:** Seleciona pasta com fotos de identificação
4. **Destino:** Define pasta de saída
5. **Configuração:** Ajusta tolerância e modo de processamento
6. **Execução:** Inicia processamento e acompanha progresso
7. **Resultado:** Visualiza fotos organizadas e relatório

#### **6.1.2 Tratamento de Erros**
- **Pastas Inválidas:** Mensagens claras de erro
- **Fotos Corrompidas:** Separação automática em pasta específica
- **Falhas de Processamento:** Log detalhado para debugging
- **Cancelamento:** Interrupção segura do processamento

### **6.2 Interface do Usuário**

#### **6.2.1 Tela Principal (Dashboard)**
- **Layout:** Centralizado com botões principais
- **Elementos:**
  - Título e subtítulo do aplicativo
  - Botão "Separar Fotos de Alunos"
  - Botão "Relatório de Alunos"
  - Rodapé com créditos

#### **6.2.2 Tela de Processamento**
- **Layout:** Formulário vertical com seções organizadas
- **Elementos:**
  - Campos de seleção de pastas
  - Controles de configuração
  - Área de log com scroll
  - Barra de progresso
  - Botões de ação (Iniciar/Cancelar)

#### **6.2.3 Tela de Relatórios**
- **Layout:** Interface de duas colunas
- **Elementos:**
  - Seleção de pastas
  - Área de visualização do relatório
  - Botão de exportação para Excel

---

## **7. Casos de Uso**

### **7.1 Caso de Uso Principal: Separação de Fotos Escolares**

#### **Ator:** Professor/Coordenador
#### **Pré-condições:**
- Sistema instalado e funcionando
- Pasta com fotos do evento disponível
- Fotos de identificação dos alunos organizadas

#### **Fluxo Principal:**
1. Professor abre o SeparaToYou
2. Clica em "Separar Fotos de Alunos"
3. Seleciona pasta com todas as fotos do evento
4. Seleciona pasta com fotos de identificação dos alunos
5. Define pasta de saída para fotos organizadas
6. Ajusta tolerância para 0.5 (padrão)
7. Marca opção de multi-processing se disponível
8. Clica em "Iniciar Processamento"
9. Acompanha progresso através da barra e log
10. Aguarda conclusão do processamento
11. Verifica fotos organizadas nas pastas criadas

#### **Pós-condições:**
- Fotos separadas por aluno em pastas individuais
- Fotos não identificadas em pasta específica
- Log completo do processamento disponível

#### **Fluxos Alternativos:**
- **7a.** Se hardware limitado, mantém processamento single-core
- **9a.** Se necessário cancelar, clica em "Cancelar" e processamento para
- **11a.** Se muitas fotos não identificadas, executa pós-processamento

### **7.2 Caso de Uso Secundário: Geração de Relatório**

#### **Ator:** Professor/Administrador
#### **Pré-condições:**
- Fotos já processadas e organizadas
- Pasta de saída com estrutura criada

#### **Fluxo Principal:**
1. Usuário clica em "Relatório de Alunos"
2. Seleciona pasta original com todas as fotos
3. Seleciona pasta de saída com fotos organizadas
4. Clica em "Gerar e Salvar Relatório em Excel"
5. Sistema processa e exibe relatório na tela
6. Define local e nome para salvar arquivo Excel
7. Confirma salvamento

#### **Pós-condições:**
- Arquivo Excel gerado com estatísticas completas
- Relatório visualizado na interface

---

## **8. Requisitos Não-Funcionais**

### **8.1 Performance**
- **Tempo de Resposta:** Interface deve responder em < 200ms
- **Throughput:** Processar mínimo de 50 fotos/minuto em hardware médio
- **Escalabilidade:** Suportar até 10.000 fotos em uma sessão
- **Uso de Memória:** Máximo 2GB de RAM durante processamento

### **8.2 Confiabilidade**
- **Disponibilidade:** 99% de uptime durante operação
- **Recuperação:** Sistema deve se recuperar de falhas sem perda de dados
- **Integridade:** Fotos originais nunca devem ser modificadas ou perdidas
- **Backup:** Log completo de todas as operações

### **8.3 Usabilidade**
- **Facilidade de Uso:** Usuário deve conseguir usar sem treinamento
- **Acessibilidade:** Interface clara com feedback visual adequado
- **Documentação:** Help integrado e mensagens de erro claras
- **Internacionalização:** Suporte inicial em português

### **8.4 Segurança**
- **Privacidade:** Fotos processadas localmente, sem envio para servidores
- **Autenticação:** Sistema de login seguro para versão premium
- **Integridade:** Validação de arquivos para evitar corrupção
- **Logs:** Registro seguro de atividades sem exposição de dados sensíveis

### **8.5 Compatibilidade**
- **Sistemas Operacionais:** Windows 10/11, macOS 10.14+, Linux Ubuntu 18.04+
- **Formatos de Arquivo:** JPG, JPEG, PNG, WEBP, BMP, TIFF
- **Hardware:** Suporte a arquiteturas x86_64 e ARM64
- **Resolução:** Funcional em resoluções de 1024x768 até 4K

---

## **9. Limitações e Restrições**

### **9.1 Limitações Técnicas**
- **Qualidade de Imagem:** Fotos muito escuras ou borradas podem não ser processadas
- **Ângulo Facial:** Rostos de perfil ou com oclusões têm menor precisão
- **Resolução Mínima:** Fotos com menos de 100x100 pixels podem ser rejeitadas
- **Formato RAW:** Não suporta formatos RAW de câmeras profissionais

### **9.2 Limitações de Hardware**
- **Processamento:** Hardware muito antigo pode ter performance limitada
- **Memória:** Sistemas com menos de 4GB RAM podem ter problemas
- **Armazenamento:** Necessário espaço livre equivalente ao dobro do tamanho das fotos

### **9.3 Limitações de Uso**
- **Conectividade:** Versão premium requer conexão com internet para autenticação
- **Licenciamento:** Uso comercial pode requerer licença específica
- **Suporte:** Suporte técnico limitado para versão gratuita

---

## **10. Roadmap e Evolução**

### **10.1 Versão Atual (1.0)**
- ✅ Separação automática de fotos
- ✅ Processamento single/multi-core
- ✅ Geração de relatórios Excel
- ✅ Interface gráfica básica
- ✅ Sistema de login premium

### **10.2 Próximas Versões**

#### **Versão 1.1 (Q2 2025)**
- 🔄 Migração para PyQt6/PySide6
- 🔄 Interface moderna com tema escuro
- 🔄 Drag & drop para seleção de pastas
- 🔄 Preview de imagens na interface

#### **Versão 1.2 (Q3 2025)**
- 📋 Suporte a formatos RAW
- 📋 Integração com cloud storage
- 📋 Backup automático de configurações
- 📋 Histórico de processamentos

#### **Versão 2.0 (Q4 2025)**
- 📋 API REST para automação
- 📋 Processamento em lote via linha de comando
- 📋 Suporte a GPU para aceleração
- 📋 Machine Learning para melhoria contínua

### **10.3 Funcionalidades Futuras**
- **Reconhecimento de Objetos:** Separação por objetos além de pessoas
- **Análise de Emoções:** Classificação por expressões faciais
- **Detecção de Duplicatas:** Identificação automática de fotos similares
- **Edição Básica:** Correção automática de cor e brilho
- **Integração Social:** Compartilhamento direto em redes sociais

---

## **11. Critérios de Aceitação**

### **11.1 Funcionalidades Principais**
- [ ] Sistema processa 1000 fotos em menos de 20 minutos
- [ ] Precisão de identificação superior a 85%
- [ ] Interface responsiva durante todo o processamento
- [ ] Relatórios Excel gerados corretamente
- [ ] Sistema funciona em Windows, macOS e Linux

### **11.2 Qualidade e Performance**
- [ ] Zero crashes durante processamento normal
- [ ] Uso de memória não excede 2GB
- [ ] Fotos originais permanecem intactas
- [ ] Log completo de todas as operações
- [ ] Cancelamento funciona corretamente

### **11.3 Usabilidade**
- [ ] Usuário consegue usar sem manual
- [ ] Mensagens de erro são claras e acionáveis
- [ ] Progresso é visível em tempo real
- [ ] Interface funciona em resoluções baixas
- [ ] Tempo de resposta da UI < 200ms

---

## **12. Riscos e Mitigações**

### **12.1 Riscos Técnicos**

#### **Alto Risco**
- **Problema:** Baixa precisão de reconhecimento facial
- **Impacto:** Usuários insatisfeitos, classificação incorreta
- **Mitigação:** Múltiplos algoritmos, ajuste de tolerância, pós-processamento

#### **Médio Risco**
- **Problema:** Performance inadequada em hardware limitado
- **Impacto:** Experiência ruim, abandono do produto
- **Mitigação:** Otimizações, modo single-core, requisitos claros

### **12.2 Riscos de Negócio**

#### **Alto Risco**
- **Problema:** Concorrência de soluções cloud
- **Impacto:** Perda de market share
- **Mitigação:** Foco em privacidade, processamento local

#### **Médio Risco**
- **Problema:** Mudanças em bibliotecas de dependência
- **Impacto:** Quebra de funcionalidade
- **Mitigação:** Versionamento fixo, testes automatizados

### **12.3 Riscos de Compliance**

#### **Médio Risco**
- **Problema:** Regulamentações de privacidade (LGPD/GDPR)
- **Impacto:** Restrições de uso, problemas legais
- **Mitigação:** Processamento local, política de privacidade clara

---

## **13. Métricas e KPIs**

### **13.1 Métricas de Produto**
- **Taxa de Precisão:** % de fotos classificadas corretamente
- **Velocidade de Processamento:** Fotos processadas por minuto
- **Taxa de Conclusão:** % de sessões completadas com sucesso
- **Uso de Recursos:** Consumo médio de CPU e RAM

### **13.2 Métricas de Usuário**
- **Tempo de Primeira Utilização:** Tempo até primeira separação bem-sucedida
- **Frequência de Uso:** Sessões por usuário por mês
- **Taxa de Retenção:** % de usuários que retornam após primeira utilização
- **Net Promoter Score (NPS):** Satisfação e recomendação

### **13.3 Métricas Técnicas**
- **Tempo de Startup:** Tempo para carregar a aplicação
- **Taxa de Erro:** % de crashes ou falhas
- **Cobertura de Testes:** % de código coberto por testes
- **Tempo de Build:** Tempo para gerar executável

---

## **14. Conclusão**

O **SeparaToYou** representa uma solução inovadora e prática para um problema real enfrentado por educadores, fotógrafos e organizadores de eventos. Com sua combinação de tecnologia avançada de reconhecimento facial e interface intuitiva, o sistema tem potencial para transformar significativamente o processo de organização de fotografias.

### **Próximos Passos**
1. **Validação:** Testes com usuários reais em ambiente educacional
2. **Otimização:** Melhorias de performance baseadas em feedback
3. **Expansão:** Desenvolvimento de funcionalidades avançadas
4. **Comercialização:** Estratégia de go-to-market para versão premium

### **Contato**
- **Desenvolvedor:** Alexandre Galhardo
- **Email:** [contato@separatoyou.com]
- **Versão do Documento:** 1.0
- **Data de Criação:** Janeiro 2025

---

*Este documento é um produto vivo e será atualizado conforme a evolução do produto e feedback dos usuários.*