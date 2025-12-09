import streamlit as st
import os
import json
import html
from datetime import datetime
from dotenv import load_dotenv

# 🔧 CORREÇÃO: Importação correta para a nova biblioteca 'google-genai'
from google import genai

# ============================================
# CONFIGURAÇÃO INICIAL
# ============================================

# Carregar variáveis de ambiente
load_dotenv()

# Configurar página
st.set_page_config(
    page_title="DescriçõesIA Pro - Gerador de Descrições para E-commerce",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inicializar estado da sessão
if 'historico' not in st.session_state:
    st.session_state.historico = []
if 'contador' not in st.session_state:
    st.session_state.contador = 0
if 'limite_gratuito' not in st.session_state:
    st.session_state.limite_gratuito = 5  # 5 descrições grátis

# ============================================
# FUNÇÕES AUXILIARES
# ============================================

def formatar_descricao(texto, formato):
    """Formata a descrição no formato selecionado"""
    if formato == "Texto simples":
        return texto
    elif formato == "HTML":
        # Converter markdown básico para HTML
        html_text = texto.replace('**', '<strong>').replace('**', '</strong>')
        html_text = html_text.replace('* ', '<li>').replace('\n', '</li>\n')
        html_text = f"<div class='produto-descricao'>{html_text}</div>"
        return html_text
    else:  # Markdown
        return texto

def calcular_palavras(tamanho):
    """Calcula o limite de palavras baseado no tamanho selecionado"""
    if tamanho == "Curta (50 palavras)":
        return 50
    elif tamanho == "Média (150 palavras)":
        return 150
    else:  # Longa
        return 300

def criar_prompt(nome_produto, categoria, tom, palavras_chave, tamanho, incluir_hashtags):
    """Cria o prompt para a IA baseado nas configurações"""
    
    limite_palavras = calcular_palavras(tamanho)
    
    prompt = f"""
    Você é um redator especialista em e-commerce, SEO e copywriting.
    Crie uma descrição de venda PERSUASIVA para o seguinte produto:

    **INFORMAÇÕES DO PRODUTO:**
    - Nome: {nome_produto}
    - Categoria: {categoria}
    - Tom desejado: {tom}
    - Palavras-chave: {palavras_chave if palavras_chave else "Não especificadas"}
    - Tamanho: {tamanho} (máximo {limite_palavras} palavras)

    **DIRETRIZES ESTRITAS:**
    1. ESTRUTURA:
       - Título chamativo (use 1-2 emojis relevantes)
       - Introdução breve (1-2 frases)
       - 4-6 bullet points com características e BENEFÍCIOS
       - Seção "Especificações Técnicas" (se aplicável)
       - Chamada para ação forte no final

    2. ESTILO:
       - Tom: {tom}
       - Foco em benefícios (não só características)
       - Use palavras de poder: exclusivo, premium, garantido, etc.
       - Linguagem persuasiva que gere urgência

    3. SEO:
       - Use palavras-chave naturalmente
       - Estrutura otimizada para motores de busca
       - Meta-descrição implícita

    4. FORMATAÇÃO:
       - Use negrito (**) para destaques
       - Use emojis moderadamente (3-5 no total)
       - Bullet points claros
    
    {'5. HASHTAGS: Inclua 3-5 hashtags relevantes no final' if incluir_hashtags else ''}

    **SAÍDA:** Apenas a descrição formatada em Markdown, sem comentários adicionais.
    """
    
    return prompt

# ============================================
# INTERFACE PRINCIPAL
# ============================================

# Título principal com estilo
st.title("🛍️ DescriçõesIA Pro")
st.markdown("### Gerador Profissional de Descrições para E-commerce")
st.markdown("*Transforme qualquer produto em uma página de vendas persuasiva*")

# Barra lateral
with st.sidebar:
    st.header("⚙️ Configuração da API")
    
    # Contador de uso
    st.metric(
        label="Descrições restantes (plano grátis)",
        value=f"{max(0, st.session_state.limite_gratuito - st.session_state.contador)}/5"
    )
    
    if st.session_state.contador >= st.session_state.limite_gratuito:
        st.error("✋ Limite do plano grátis atingido!")
        st.info("**Upgrade para Pro:** Descrições ilimitadas por R$29/mês")
    
    # Chave da API
    api_key = st.text_input(
        "Chave da API Gemini",
        type="password",
        value=os.getenv("GEMINI_API_KEY", ""),
        help="Obtenha uma chave gratuita em https://aistudio.google.com/apikey"
    )
    
    # 🔧 CORREÇÃO: Lista atualizada com modelos disponíveis e funcionais
    modelo = st.selectbox(
        "Modelo Gemini",
        ["gemini-2.5-flash", "gemini-2.0-flash", "gemini-2.0-flash-001", "gemini-2.5-flash-lite"],
        help="Flash: mais rápido e eficiente. Recomendado: gemini-2.5-flash"
    )
    
    # Criatividade
    temperatura = st.slider(
        "Criatividade (Temperatura)",
        min_value=0.0,
        max_value=1.0,
        value=0.7,
        help="0.0 = mais preciso, 1.0 = mais criativo"
    )
    
    st.divider()
    
    # Informações da conta (simuladas)
    st.header("📊 Sua Conta")
    st.progress(min(st.session_state.contador / 5, 1.0))
    st.caption(f"Usado: {st.session_state.contador}/5 descrições")
    
    # Botão para resetar (apenas para demonstração)
    if st.button("🔄 Resetar Contador (Demo)", type="secondary"):
        st.session_state.contador = 0
        st.rerun()
    
    st.divider()
    st.info("💡 **Dica profissional:** Use palavras-chave específicas para melhor SEO!")

# ============================================
# ABA PRINCIPAL - GERAR DESCRIÇÃO
# ============================================

# Usar abas para organização
tab1, tab2 = st.tabs(["🚀 Gerar Nova Descrição", "📋 Histórico"])

with tab1:
    st.header("📝 Informações do Produto")
    
    # Layout em colunas
    col1, col2 = st.columns(2)
    
    with col1:
        nome_produto = st.text_input(
            "**Nome do Produto**",
            placeholder="Ex: Tênis Esportivo para Corrida Nike Air Max",
            help="Seja específico e inclua marca se aplicável"
        )
        
        categoria = st.selectbox(
            "**Categoria Principal**",
            ["Roupas e Moda", "Eletrônicos", "Casa e Jardim", 
             "Beleza e Saúde", "Esportes", "Automotivo", 
             "Brinquedos", "Alimentos", "Livros", "Outros"]
        )
        
        tom_descricao = st.selectbox(
            "**Tom da Descrição**",
            ["Persuasivo/Vendedor", "Informativo/Técnico", 
             "Descontraído/Jovem", "Luxo/Premium", "Ecológico/Sustentável"]
        )
    
    with col2:
        # Configurações avançadas em expansor
        with st.expander("⚙️ Configurações Avançadas", expanded=True):
            tamanho = st.select_slider(
                "**Tamanho da descrição:**",
                options=["Curta (50 palavras)", "Média (150 palavras)", "Longa (300 palavras)"],
                value="Média (150 palavras)"
            )
            
            formato_exportacao = st.radio(
                "**Formato de exportação:**",
                ["Texto simples", "HTML", "Markdown"],
                horizontal=True
            )
            
            incluir_hashtags = st.checkbox(
                "Incluir hashtags para redes sociais",
                value=True
            )
            
            incluir_especificacoes = st.checkbox(
                "Incluir seção de especificações técnicas",
                value=True
            )
    
    # Palavras-chave
    palavras_chave = st.text_input(
        "**Palavras-chave importantes (opcional)**",
        placeholder="Ex: sustentável, à prova d'água, premium, durável, confortável",
        help="Separe por vírgulas. Essas palavras serão enfatizadas na descrição."
    )
    
    st.divider()
    
    # Botão de geração
    col_btn1, col_btn2, col_btn3 = st.columns([2, 1, 1])
    
    with col_btn1:
        gerar_disabled = st.session_state.contador >= st.session_state.limite_gratuito
        
        if st.button("✨ Gerar Descrição com IA", 
                    type="primary", 
                    use_container_width=True,
                    disabled=gerar_disabled):
            
            if not nome_produto:
                st.warning("Por favor, insira o nome do produto.")
            elif not api_key:
                st.warning("Por favor, insira sua chave da API Gemini na barra lateral.")
            else:
                with st.spinner('🧠 A IA está criando a descrição perfeita...'):
                    try:
                        # 🔧 CORREÇÃO: Criação do cliente com a versão estável 'v1' da API
                        # O cliente deve ser criado aqui dentro, após a confirmação da chave.
                        client = genai.Client(api_key=api_key, http_options={'api_version': 'v1'})
                        
                        # Criar prompt
                        prompt = criar_prompt(
                            nome_produto, categoria, tom_descricao,
                            palavras_chave, tamanho, incluir_hashtags
                        )
                        
                        # 🔧 CORREÇÃO: Chamada da API conforme funcionou na versão teste.
                        # Remove 'generation_config' para usar a sintaxe simples e confiável.
                        response = client.models.generate_content(
                            model=modelo,
                            contents=prompt
                            # O parâmetro 'temperature' pode ser ajustado via 'generation_config' no futuro,
                            # mas foi removido para garantir o funcionamento básico agora.
                        )
                        
                        descricao_gerada = response.text
                        
                        # Formatar de acordo com o formato selecionado
                        descricao_formatada = formatar_descricao(descricao_gerada, formato_exportacao)
                        
                        # Adicionar ao histórico
                        registro = {
                            "data": datetime.now().strftime("%d/%m/%Y %H:%M"),
                            "produto": nome_produto,
                            "categoria": categoria,
                            "descricao": descricao_gerada,
                            "formato": formato_exportacao
                        }
                        st.session_state.historico.insert(0, registro)
                        
                        # Incrementar contador
                        st.session_state.contador += 1
                        
                        # Exibir resultado
                        st.success(f"✅ Descrição gerada com sucesso! (Usos: {st.session_state.contador}/5)")
                        st.divider()
                        
                        st.subheader("📋 Descrição Gerada:")
                        
                        # Mostrar de acordo com o formato
                        if formato_exportacao == "HTML":
                            st.components.v1.html(descricao_formatada, height=300, scrolling=True)
                        else:
                            st.markdown(descricao_formatada)
                        
                        # Botões de ação
                        col_acao1, col_acao2, col_acao3 = st.columns(3)
                        
                        with col_acao1:
                            st.code(descricao_gerada, language="markdown")
                            st.caption("📋 Copie o texto acima")
                        
                        with col_acao2:
                            # Botão para download simulado
                            if st.button("💾 Salvar como .txt", use_container_width=True):
                                st.info("Recurso Pro: Download disponível no plano pago")
                        
                        with col_acao3:
                            if st.button("🔄 Gerar outra versão", use_container_width=True):
                                st.rerun()
                        
                        st.divider()
                        st.caption("💡 **Dica:** Esta descrição está otimizada para SEO e conversão. Use em Shopee, Mercado Livre, OLX, Amazon, etc.")
                        
                    except Exception as e:
                        st.error(f"❌ Erro ao gerar descrição: {str(e)}")
                        # 🔧 MELHORIA: Mensagem mais específica para erro de cota (429)
                        if "429" in str(e) or "quota" in str(e).lower():
                            st.info("""
                            **Erro de cota excedida (Plano Gratuito).** Para continuar:
                            1.  Acesse o [Google AI Studio](https://makersuite.google.com/app/apikey).
                            2.  Verifique o projeto da sua chave API.
                            3.  **Ative o faturamento** e faça **upgrade do plano gratuito** para um plano pago (ex: Tier 1).
                            """)
                        else:
                            st.info("Verifique sua chave da API e conexão com a internet.")
    
    with col_btn2:
        # Exemplo rápido
        if st.button("🎯 Exemplo Rápido", use_container_width=True):
            # Usando st.session_state para preencher campos
            st.session_state.nome_produto = "Fone Bluetooth à Prova d'Água"
            st.session_state.categoria = "Eletrônicos"
            st.rerun()
    
    with col_btn3:
        # Limpar campos
        if st.button("🗑️ Limpar Campos", use_container_width=True):
            # Uma maneira simples de limpar campos específicos (opcional, o rerun já limpa)
            st.rerun()

# ============================================
# ABA 2 - HISTÓRICO
# ============================================

with tab2:
    st.header("📋 Histórico de Descrições Geradas")
    
    if not st.session_state.historico:
        st.info("📭 Nenhuma descrição gerada ainda. Vá para a aba 'Gerar Nova Descrição' para começar!")
    else:
        # Mostrar histórico em ordem reversa (mais recente primeiro)
        for i, registro in enumerate(st.session_state.historico[:10]):  # Últimas 10
            with st.expander(f"{registro['data']} - {registro['produto']} ({registro['categoria']})", expanded=(i==0)):
                col_hist1, col_hist2 = st.columns([3, 1])
                
                with col_hist1:
                    st.markdown(registro['descricao'])
                
                with col_hist2:
                    st.caption(f"**Formato:** {registro['formato']}")
                    # Nota: A cópia real para a área de transferência requer JavaScript.
                    # Este botão apenas exibe o código para fácil seleção manual.
                    if st.button("📋 Copiar", key=f"copy_{i}", use_container_width=True):
                        st.code(registro['descricao'], language="markdown")
                        st.success("Texto pronto para cópia! Selecione e use Ctrl+C.")
        
        # Estatísticas
        st.divider()
        col_stat1, col_stat2, col_stat3 = st.columns(3)
        
        with col_stat1:
            st.metric("Total Gerado", len(st.session_state.historico))
        
        with col_stat2:
            # Categoria mais comum
            categorias = [h['categoria'] for h in st.session_state.historico]
            if categorias:
                mais_comum = max(set(categorias), key=categorias.count)
                st.metric("Categoria Mais Frequente", mais_comum)
        
        with col_stat3:
            if st.button("🧹 Limpar Histórico", type="secondary"):
                st.session_state.historico = []
                st.rerun()

# ============================================
# RODAPÉ E INFORMAÇÕES
# ============================================

st.divider()

# Plano de negócios
with st.expander("💼 Modelo de Negócio - DescriçõesIA Pro"):
    col_biz1, col_biz2, col_biz3 = st.columns(3)
    
    with col_biz1:
        st.subheader("🎯 Plano Gratuito")
        st.write("""
        - 5 descrições por mês
        - Modelos básicos
        - Suporte por email
        - Ideal para testar
        """)
    
    with col_biz2:
        st.subheader("🚀 Plano Pro (R$29/mês)")
        st.write("""
        - Descrições ilimitadas
        - Todos os modelos Gemini
        - Histórico ilimitado
        - Exportação em múltiplos formatos
        - Suporte prioritário
        """)
    
    with col_biz3:
        st.subheader("🏢 Plano Empresarial")
        st.write("""
        - API dedicada
        - Treinamento personalizado
        - Integração com marketplaces
        - Analytics avançado
        - Contrato anual
        """)
    
    st.caption("*Preços em BRL. Cancelamento a qualquer momento.*")

# Rodapé
st.markdown("---")
col_footer1, col_footer2, col_footer3 = st.columns(3)

with col_footer1:
    st.markdown("**✨ DescriçõesIA Pro**")
    st.caption("Gerando vendas com IA desde 2024")

with col_footer2:
    st.markdown("**📞 Contato**")
    st.caption("suporte@descricoesia.com.br")

with col_footer3:
    st.markdown("**🔒 Privacidade**")
    st.caption("Seus dados nunca são compartilhados")

# Nota final
st.caption("""
⚠️ **Aviso:** Este é um projeto demonstrativo para fins educacionais. 
As descrições são geradas por IA e devem ser revisadas antes do uso em produção.
""")