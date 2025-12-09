# DescriçõesIA Pro 🛍️

**Gerador Profissional de Descrições para E-commerce com IA**

SaaS completo para geração automática de descrições otimizadas para marketplaces brasileiros (Shopee, Mercado Livre, OLX, Amazon) utilizando Inteligência Artificial (Google Gemini API).

> **Projeto de Conclusão de Curso** - Inteligência Artificial - Desenvolvimento de SaaS com IA

## 📋 Índice
- [✨ Funcionalidades](#-funcionalidades)
- [🛠️ Tecnologias](#️-tecnologias)
- [🚀 Instalação Local](#-instalação-local)
- [🎯 Como Usar](#-como-usar)
  - [1️⃣ Obtenha sua Chave da API Gemini](#1️⃣-obtenha-sua-chave-da-api-gemini)
  - [2️⃣ Primeiro Acesso ao Sistema](#2️⃣-primeiro-acesso-ao-sistema)
  - [3️⃣ Gerando sua Primeira Descrição](#3️⃣-gerando-sua-primeira-descrição)
  - [4️⃣ Explorando Recursos Avançados](#4️⃣-explorando-recursos-avançados)
- [🏗️ Estrutura do Projeto](#️-estrutura-do-projeto)
- [💰 Modelo de Negócio](#-modelo-de-negócio)
- [🔧 Solução de Problemas](#-solução-de-problemas)
- [👨‍💻 Autor](#-autor)
- [📝 Licença](#-licença)

## ✨ Funcionalidades

### 🤖 Geração Inteligente com IA
| Recurso | Descrição | Benefício |
|---------|-----------|-----------|
| **Google Gemini API** | Modelo de linguagem avançado | Descrições persuasivas e naturais |
| **6 Templates Especializados** | Shopee, Amazon, Redes Sociais, SEO, Copy Persuasivo, Luxo | Adequação perfeita a cada canal |
| **Configuração Avançada** | Ajuste tom, criatividade, tamanho, palavras-chave | Personalização total do resultado |
| **Otimização SEO Automática** | Inserção inteligente de palavras-chave | Maior visibilidade nos marketplaces |

### 👤 Sistema Completo de Usuários
| Recurso | Plano Free | Plano Pro |
|---------|------------|-----------|
| **Descrições/mês** | 5 | Ilimitadas |
| **Templates** | 3 básicos | 10+ profissionais |
| **Histórico** | Últimas 10 | Ilimitado |
| **Exportação** | .txt apenas | .txt, .html, .pdf |
| **Analytics** | Básico | Avançado com gráficos |

### 💼 Pronto para Negócios
- **Modelo Freemium**: Converte usuários gratuitos em pagantes
- **Calculadora de ROI**: Mostra economia real de tempo e dinheiro
- **Sistema de Pagamento Simulado**: Fluxo completo de checkout
- **Multi-formatos de Exportação**: Pronto para qualquer plataforma

## 🛠️ Tecnologias

**Stack Principal:**
```yaml
Backend:
  - Python 3.9+
  - Streamlit (Interface web)
  - SQLite (Banco de dados)
  - Google Gemini API (IA)

Bibliotecas Críticas:
  - streamlit: Interface do usuário
  - google-genai: Integração com Gemini
  - pandas: Processamento de dados
  - plotly: Visualizações interativas
  - python-dotenv: Gerenciamento de segredos
```

## 🚀 Instalação Local

### Pré-requisitos
- **Python 3.9 ou superior** ([Download](https://www.python.org/downloads/))
- **Conta Google** (para obter chave da API)
- **Git** (opcional, para clonar o repositório)

### Passo a Passo

1. **Clone o repositório**
```bash
# Clone o projeto
git clone https://github.com/seuusuario/descricoesia-pro.git

# Acesse a pasta do projeto
cd descricoesia-pro
```

2. **Instale as dependências**
```bash
# Método recomendado (usando venv)
python -m venv venv

# No Windows:
venv\Scripts\activate

# No Mac/Linux:
source venv/bin/activate

# Instale os pacotes
pip install -r requirements.txt
```

3. **Configure a chave da API Gemini**
```bash
# Copie o arquivo de exemplo
cp .env.example .env

# Edite o arquivo .env e adicione sua chave
# Abra no editor de sua preferência
```

4. **Execute a aplicação**
```bash
streamlit run app.py
```

5. **Acesse no navegador**
- Abra: [http://localhost:8501](http://localhost:8501)

## 🎯 Como Usar

### 1️⃣ Obtenha sua Chave da API Gemini

**Passo a Passo Detalhado:**

1. **Acesse o Google AI Studio**
   - Vá para: [https://aistudio.google.com/apikey](https://aistudio.google.com/apikey)
   - Faça login com sua conta Google

2. **Crie um novo projeto**
   ```text
   ✅ Clique em "Get API Key" (Obter chave da API)
   ✅ Clique em "Create API Key" (Criar chave da API)
   ✅ Selecione "Create API key in new project" 
   ✅ Dê um nome ao projeto: "DescriçõesIA Pro"
   ```

3. **Copie sua chave**
   - A chave terá formato: `AIzaSyD...` (aproximadamente 40 caracteres)
   - ⚠️ **Importante**: Nunca compartilhe esta chave publicamente!

4. **Configure os limites (recomendado)**
   ```text
   No Google Cloud Console:
   1. Acesse "API & Services" > "Quotas"
   2. Aumente os limites se necessário
   3. Plano gratuito: 60 requisições/minuto
   ```

### 2️⃣ Primeiro Acesso ao Sistema

**Tela de Login:**
```text
📌 Primeira vez?
1. Clique em "Criar Conta"
2. Insira: Email válido + Senha (mínimo 6 caracteres)
3. Aceite os termos
4. Clique em "Criar Conta"

📌 Já tem conta?
1. Insira email e senha
2. Clique em "Entrar"
```

**Configuração Inicial:**
```text
✅ Após login:
1. Na barra lateral esquerda, cole sua chave da API no campo "Chave da API Gemini"
2. Escolha o modelo (recomendado: gemini-2.5-flash)
3. Ajuste a criatividade (0.7 é um bom valor)
```

### 3️⃣ Gerando sua Primeira Descrição

**Passo a Passo Detalhado:**

1. **Acesse a aba "🚀 Gerar Nova"**
   ```text
   ➡️ Localizada no topo da página
   ```

2. **Preencha as informações básicas:**
   ```yaml
   Campo                | Exemplo de Preenchimento
   -------------------- | --------------------------
   Nome do Produto      | "Tênis Esportivo Nike Air Max 270 Masculino"
   Categoria            | Selecionar: "Roupas e Moda"
   Tom da Descrição     | Selecionar: "Persuasivo/Vendedor"
   ```

3. **Configure as opções avançadas:**
   ```text
   Clique em "⚙️ Configurações Avançadas"
   
   Recomendações:
   • Tamanho: "Média (150 palavras)"
   • Template: "Shopee/Mercado Livre" 
   • Formato: "Texto simples"
   • Marcar: "Incluir hashtags"
   ```

4. **Adicione palavras-chave (opcional mas recomendado):**
   ```text
   Exemplo: "confortável, amortecimento, corrida, leve, durável"
   ```

5. **Gere a descrição:**
   ```text
   Clique no botão verde: "✨ Gerar Descrição com IA"
   ⏳ Aguarde 5-10 segundos
   ✅ Descrição aparecerá abaixo
   ```

6. **Copie e use:**
   ```text
   Opções disponíveis:
   • Selecione o texto e copie (Ctrl+C)
   • Clique em "📋 Copiar" para ter o texto formatado
   • Use "💾 Exportar como .txt" para salvar arquivo
   ```

### 4️⃣ Explorando Recursos Avançados

**📋 Histórico de Descrições:**
```text
Local: Aba "📋 Histórico"
Funcionalidades:
• Veja todas descrições geradas
• Filtre por data, categoria, template
• Copie descrições anteriores com um clique
• Exclua descrições antigas
```

**📊 Analytics (Plano Pro):**
```text
Local: Aba "📊 Analytics"
Métricas disponíveis:
• Total de descrições geradas
• Gráfico de uso por dia
• Categorias mais usadas
• Templates preferidos
• Exportação de relatórios
```

**💎 Upgrade de Plano:**
```text
Local: Aba "💎 Upgrade"
Processo:
1. Compare planos Free vs Pro
2. Clique em "👉 Upgrade para Pro"
3. Simule pagamento (cartão, PIX, etc.)
4. Confirmação instantânea
```

**📞 Suporte e Validação:**
```text
Local: Aba "📞 Suporte"
Recursos:
• Casos de sucesso reais
• Calculadora de ROI
• Lista de espera para novos recursos
• Contato com suporte
```

## 🏗️ Estrutura do Projeto

```
descricoesia-pro/
├── 📁 Módulos da Aplicação
│   ├── database.py          # Banco de dados SQLite (usuários, descrições)
│   ├── auth.py              # Sistema de login/cadastro (SHA-256)
│   ├── templates.py         # 6 templates especializados
│   ├── utils.py             # Funções auxiliares (exportação, analytics)
│   └── upgrade.py           # Sistema de planos e pagamentos
├── 📁 Dados
│   └── descricoes.db       # Banco de dados SQLite (não versionado)
├── 📄 Arquivos Principais
│   ├── app.py              # Aplicação Streamlit (ponto de entrada)
│   ├── requirements.txt    # Dependências Python
│   ├── .env.example        # Modelo para variáveis de ambiente
│   └── README.md          # Esta documentação
└── 📁 Screenshots          # Imagens para documentação
```

## 💰 Modelo de Negócio

### **Plano Free** (R$ 0/mês)
```yaml
Público-alvo: Pequenos vendedores, testadores
Limite: 5 descrições por mês
Recursos: Templates básicos, histórico limitado
Conversão estimada: 15% para Pro
```

### **Plano Pro** (R$ 29/mês)
```yaml
Público-alvo: Lojistas ativos, empreendedores
Recursos: Descrições ilimitadas, todos templates, analytics
CAC (Custo de Aquisição): ~R$ 50
LTV (Valor Vitalício): ~R$ 350
```

### **Plano Enterprise** (Sob consulta)
```yaml
Público-alvo: Grandes e-commerces, marketplaces
Recursos: API dedicada, integração, suporte 24/7
Ticket médio: R$ 299/mês
```

### **Projeção Financeira (Ano 1)**
```text
Usuários Free: 1.000
Conversão para Pro: 15% = 150 usuários
MRR (Monthly Recurring Revenue): 150 × R$29 = R$4.350/mês
ARR (Annual Recurring Revenue): R$52.200/ano
```

## 🔧 Solução de Problemas

### **Erro Comum: "429 - Quota Exceeded"**
```text
Sintoma: "Erro 429: You exceeded your current quota"
Causa: Limite da API gratuita (60 requisições/minuto)

Solução:
1. Aguarde 60 minutos (o limite é por hora)
2. Ative faturamento no Google Cloud:
   • Acesse https://console.cloud.google.com
   • Vá em "Billing" > "Account Management"
   • Adicione método de pagamento
   • Plano recomendado: "Pay as you go" (R$ 0.0005/1K tokens)
```

### **Erro: "API key not valid"**
```bash
# Verifique sua chave:
echo $GEMINI_API_KEY  # No terminal

# No Windows:
echo %GEMINI_API_KEY%

# Solução:
# 1. Gere nova chave em https://aistudio.google.com/apikey
# 2. Atualize no arquivo .env
# 3. Reinicie o Streamlit
```

### **Banco de dados não cria tabelas**
```bash
# Execute manualmente:
python -c "
from modules.database import Database
db = Database()
print('✅ Banco inicializado')
"

# Se falhar, verifique permissões:
chmod 755 data/  # Linux/Mac
```

### **Streamlit não encontra módulos**
```bash
# Certifique-se da estrutura correta:
ls -la modules/
# Deve mostrar: database.py, auth.py, etc.

# Execute da raiz do projeto:
cd /caminho/completo/para/descricoesia-pro
streamlit run app.py
```

### **Performance lenta**
```text
Melhorias possíveis:
1. Use modelo mais leve: "gemini-2.5-flash-lite"
2. Reduza temperatura para 0.5
3. Use conexão estável de internet
4. Limite histórico para 50 registros
```

## 👨‍💻 Autor

**Seu Nome**  
🎓 Aluno do Curso de Inteligência Artificial - Desenvolvimento de SaaS com IA  
📧 isabelacoelhoo@gmail.com

## 📝 Licença

Este projeto foi desenvolvido exclusivamente para fins educacionais como **Trabalho de Conclusão de Curso** de Inteligência Artificial.

**Avisos Importantes:**
- ⚠️ Uso educacional e demonstrativo apenas
- 🔒 Nunca exponha chaves de API publicamente
- 📊 Dados de usuários são armazenados localmente (SQLite)
- 🚫 Não use descrições geradas sem revisão humana

---