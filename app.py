import streamlit as st
import os
import json
import html
from datetime import datetime
from dotenv import load_dotenv

# 🔧 Importações corretas
from google import genai

# 🔧 NOVAS IMPORTAÇÕES
import database as db
import auth
import utils
import templates as temp
from upgrade import show_upgrade_page

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

# Inicializar banco de dados
if 'db' not in st.session_state:
    st.session_state.db = db.Database()

# Inicializar estado da sessão
if 'user_id' not in st.session_state:
    st.session_state.user_id = None
if 'user_email' not in st.session_state:
    st.session_state.user_email = None
if 'user_plan' not in st.session_state:
    st.session_state.user_plan = 'free'
if 'historico' not in st.session_state:
    st.session_state.historico = []

# Inicializar campos do formulário
if 'nome_produto' not in st.session_state:
    st.session_state.nome_produto = ''
if 'categoria' not in st.session_state:
    st.session_state.categoria = 'Eletrônicos'
if 'tom_descricao' not in st.session_state:
    st.session_state.tom_descricao = 'Persuasivo/Vendedor'
if 'palavras_chave' not in st.session_state:
    st.session_state.palavras_chave = ''
if 'tamanho' not in st.session_state:
    st.session_state.tamanho = 'Média (150 palavras)'
if 'template_selecionado' not in st.session_state:
    st.session_state.template_selecionado = 'default'
if 'formato_exportacao' not in st.session_state:
    st.session_state.formato_exportacao = 'Texto simples'
if 'incluir_hashtags' not in st.session_state:
    st.session_state.incluir_hashtags = True
if 'incluir_especificacoes' not in st.session_state:
    st.session_state.incluir_especificacoes = True

# ============================================
# FUNÇÕES AUXILIARES
# ============================================

def formatar_descricao(texto, formato):
    """Formata a descrição no formato selecionado"""
    if formato == "Texto simples":
        return texto
    elif formato == "HTML":
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

def criar_prompt(nome_produto, categoria, tom, palavras_chave, tamanho, incluir_hashtags, template_selecionado, incluir_especificacoes):
    """Cria o prompt para a IA baseado nas configurações"""
    
    limite_palavras = calcular_palavras(tamanho)
    
    # Obter instruções específicas do template
    template_info = temp.get_template_instructions(template_selecionado)
    
    prompt = f"""
    Você é um redator especialista em e-commerce, SEO e copywriting.
    Crie uma descrição de venda PERSUASIVA para o seguinte produto:

    **INFORMAÇÕES DO PRODUTO:**
    - Nome: {nome_produto}
    - Categoria: {categoria}
    - Tom desejado: {tom}
    - Palavras-chave: {palavras_chave if palavras_chave else "Não especificadas"}
    - Tamanho: {tamanho} (máximo {limite_palavras} palavras)
    - Template: {template_selecionado}

    **DIRETRIZES ESTRITAS:**
    1. ESTRUTURA:
       - Título chamativo (use 1-2 emojis relevantes)
       - Introdução breve (1-2 frases)
       - 4-6 bullet points com características e BENEFÍCIOS
       {'- Seção "Especificações Técnicas" (se aplicável)' if incluir_especificacoes else ''}
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
    
    **5. TEMPLATE ESPECÍFICO:**
    {template_info}
    
    {'6. HASHTAGS: Inclua 3-5 hashtags relevantes no final' if incluir_hashtags else ''}

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

# Verificar se usuário está logado
if not st.session_state.user_id:
    # Mostrar página de login/registro
    auth.show_auth_page()
else:
    # Usuário logado - mostrar aplicação principal
    # Barra lateral
    with st.sidebar:
        st.header(f"👤 {st.session_state.user_email}")
        st.caption(f"Plano: {st.session_state.user_plan}")
        
        # Contador de uso
        if st.session_state.user_plan == 'free':
            descricoes_usadas = st.session_state.db.get_user_description_count(st.session_state.user_id)
            descricoes_restantes = max(0, 5 - descricoes_usadas)
            st.metric(
                label="Descrições restantes (plano grátis)",
                value=f"{descricoes_restantes}/5"
            )
            
            if descricoes_usadas >= 5:
                st.error("✋ Limite do plano grátis atingido!")
                st.info("**Faça upgrade para Pro para continuar usando!**")
        
        # Chave da API
        api_key = st.text_input(
            "Chave da API Gemini",
            type="password",
            value=os.getenv("GEMINI_API_KEY", ""),
            help="Obtenha uma chave gratuita em https://aistudio.google.com/apikey"
        )
        
        # Modelos disponíveis
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
        
        # Informações da conta
        st.header("📊 Sua Conta")
        if st.session_state.user_plan == 'free':
            descricoes_usadas = st.session_state.db.get_user_description_count(st.session_state.user_id)
            st.progress(min(descricoes_usadas / 5, 1.0))
            st.caption(f"Usado: {descricoes_usadas}/5 descrições")
        else:
            st.info("✅ Plano Pro - Descrições ilimitadas!")
        
        # Botão de logout
        if st.button("🚪 Sair", use_container_width=True):
            auth.logout_user()
            st.rerun()
        
        st.divider()
        st.info("💡 **Dica profissional:** Use palavras-chave específicas para melhor SEO!")

    # ============================================
    # ABA PRINCIPAL - GERAR DESCRIÇÃO
    # ============================================

    # Usar abas para organização
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["🚀 Gerar Nova", "📋 Histórico", "📊 Analytics", "💎 Upgrade", "📞 Suporte"])

    with tab1:
        st.header("📝 Informações do Produto")
        
        # Layout em colunas
        col1, col2 = st.columns(2)
        
        with col1:
            # Listas de opções
            categorias = ["Roupas e Moda", "Eletrônicos", "Casa e Jardim", 
                         "Beleza e Saúde", "Esportes", "Automotivo", 
                         "Brinquedos", "Alimentos", "Livros", "Outros"]
            
            tons = ["Persuasivo/Vendedor", "Informativo/Técnico", 
                   "Descontraído/Jovem", "Luxo/Premium", "Ecológico/Sustentável"]
            
            nome_produto = st.text_input(
                "**Nome do Produto**",
                value=st.session_state.nome_produto,
                placeholder="Ex: Tênis Esportivo para Corrida Nike Air Max",
                help="Seja específico e inclua marca se aplicável"
            )
            
            categoria = st.selectbox(
                "**Categoria Principal**",
                options=categorias,
                index=categorias.index(st.session_state.categoria) if st.session_state.categoria in categorias else 1
            )
            
            tom_descricao = st.selectbox(
                "**Tom da Descrição**",
                options=tons,
                index=tons.index(st.session_state.tom_descricao) if st.session_state.tom_descricao in tons else 0
            )

        with col2:
            # Configurações avançadas em expansor
            with st.expander("⚙️ Configurações Avançadas", expanded=True):
                tamanho_opcoes = ["Curta (50 palavras)", "Média (150 palavras)", "Longa (300 palavras)"]
                tamanho = st.select_slider(
                    "**Tamanho da descrição:**",
                    options=tamanho_opcoes,
                    value=st.session_state.tamanho
                )
                
                # 🔧 NOVO: Seleção de template
                template_opcoes = list(temp.TEMPLATES.keys())
                template_selecionado = st.selectbox(
                    "**Template de descrição:**",
                    options=template_opcoes,
                    index=template_opcoes.index(st.session_state.template_selecionado) if st.session_state.template_selecionado in template_opcoes else 0,
                    format_func=lambda x: temp.TEMPLATES[x]["name"],
                    help="Selecione o template mais adequado para sua necessidade"
                )
                
                formato_opcoes = ["Texto simples", "HTML", "Markdown"]
                formato_exportacao = st.radio(
                    "**Formato de exportação:**",
                    options=formato_opcoes,
                    index=formato_opcoes.index(st.session_state.formato_exportacao) if st.session_state.formato_exportacao in formato_opcoes else 0,
                    horizontal=True
                )
                
                incluir_hashtags = st.checkbox(
                    "Incluir hashtags para redes sociais",
                    value=st.session_state.incluir_hashtags
                )
                
                incluir_especificacoes = st.checkbox(
                    "Incluir seção de especificações técnicas",
                    value=st.session_state.incluir_especificacoes
                )
        
        # Palavras-chave
        palavras_chave = st.text_input(
            "**Palavras-chave importantes (opcional)**",
            value=st.session_state.palavras_chave,
            placeholder="Ex: sustentável, à prova d'água, premium, durável, confortável",
            help="Separe por vírgulas. Essas palavras serão enfatizadas na descrição."
        )
        
        st.divider()
        
        # Botão de geração
        col_btn1, col_btn2, col_btn3 = st.columns([2, 1, 1])
        
        with col_btn1:
            # Verificar limite do plano free
            if st.session_state.user_plan == 'free':
                descricoes_usadas = st.session_state.db.get_user_description_count(st.session_state.user_id)
                gerar_disabled = descricoes_usadas >= 5
            else:
                gerar_disabled = False
            
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
                            # Criar cliente Gemini
                            client = genai.Client(api_key=api_key, http_options={'api_version': 'v1'})
                            
                            # Criar prompt com template
                            prompt = criar_prompt(
                                nome_produto, categoria, tom_descricao,
                                palavras_chave, tamanho, incluir_hashtags, 
                                template_selecionado, incluir_especificacoes
                            )
                            
                            # Chamar a API
                            response = client.models.generate_content(
                                model=modelo,
                                contents=prompt
                            )
                            
                            descricao_gerada = response.text
                            
                            # Formatar de acordo com o formato selecionado
                            descricao_formatada = formatar_descricao(descricao_gerada, formato_exportacao)
                            
                            # Salvar no banco de dados
                            st.session_state.db.save_description(
                                user_id=st.session_state.user_id,
                                product_name=nome_produto,
                                category=categoria,
                                tone=tom_descricao,
                                keywords=palavras_chave,
                                size=tamanho,
                                template=template_selecionado,
                                description=descricao_gerada,
                                formato=formato_exportacao
                            )
                            
                            # Exibir resultado
                            st.success(f"✅ Descrição gerada com sucesso!")
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
                                # Exportação real
                                if st.button("💾 Exportar como .txt", use_container_width=True):
                                    utils.export_to_txt(descricao_gerada, nome_produto)
                                    st.success("Arquivo salvo como descricao.txt")
                            
                            with col_acao3:
                                if st.button("🔄 Gerar outra versão", use_container_width=True):
                                    st.rerun()
                            
                            st.divider()
                            st.caption("💡 **Dica:** Esta descrição está otimizada para SEO e conversão. Use em Shopee, Mercado Livre, OLX, Amazon, etc.")
                            
                        except Exception as e:
                            st.error(f"❌ Erro ao gerar descrição: {str(e)}")
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
                # Atualizar session_state
                st.session_state.nome_produto = "Fone Bluetooth à Prova d'Água com Cancelamento de Ruído"
                st.session_state.categoria = "Eletrônicos"
                st.session_state.tom_descricao = "Persuasivo/Vendedor"
                st.session_state.palavras_chave = "bluetooth, à prova d'água, cancelamento ruído, esportivo, bateria longa"
                st.session_state.tamanho = "Média (150 palavras)"
                st.session_state.template_selecionado = "default"
                st.session_state.formato_exportacao = "Texto simples"
                st.session_state.incluir_hashtags = True
                st.session_state.incluir_especificacoes = True
                
                # Recarregar
                st.rerun()
        
        with col_btn3:
            # Limpar campos - CORRIGIDO
            if st.button("🗑️ Limpar Campos", use_container_width=True):
                # Limpar apenas os campos de entrada (não as configurações padrão)
                st.session_state.nome_produto = ''
                st.session_state.categoria = 'Eletrônicos'
                st.session_state.tom_descricao = 'Persuasivo/Vendedor'
                st.session_state.palavras_chave = ''
                # Mantém as configurações avançadas como padrão
                st.session_state.tamanho = 'Média (150 palavras)'
                st.session_state.template_selecionado = 'default'
                st.session_state.formato_exportacao = 'Texto simples'
                st.session_state.incluir_hashtags = True
                st.session_state.incluir_especificacoes = True
                
                st.rerun()

    # ============================================
    # ABA 2 - HISTÓRICO
    # ============================================

    with tab2:
        st.header("📋 Histórico de Descrições Geradas")
        
        historico = st.session_state.db.get_user_descriptions(st.session_state.user_id)
        
        if not historico:
            st.info("📭 Nenhuma descrição gerada ainda. Vá para a aba 'Gerar Nova Descrição' para começar!")
        else:
            # Mostrar histórico em ordem reversa (mais recente primeiro)
            for i, registro in enumerate(historico[:10]):  # Últimas 10
                with st.expander(f"{registro[7]} - {registro[1]} ({registro[2]})", expanded=(i==0)):
                    col_hist1, col_hist2 = st.columns([3, 1])
                    
                    with col_hist1:
                        st.markdown(registro[6])  # Descrição
                    
                    with col_hist2:
                        st.caption(f"**Template:** {registro[5]}")
                        st.caption(f"**Formato:** {registro[8]}")
                        st.caption(f"**Tamanho:** {registro[4]}")
                        
                        # Botão para copiar
                        if st.button("📋 Copiar", key=f"copy_{i}_{registro[0]}", use_container_width=True):
                            st.code(registro[6], language="markdown")
                            st.success("Texto pronto para cópia! Selecione e use Ctrl+C.")
            
            # Estatísticas
            st.divider()
            col_stat1, col_stat2, col_stat3 = st.columns(3)
            
            with col_stat1:
                st.metric("Total Gerado", len(historico))
            
            with col_stat2:
                # Categoria mais comum
                if historico:
                    categorias = [h[2] for h in historico]
                    mais_comum = max(set(categorias), key=categorias.count)
                    st.metric("Categoria Mais Frequente", mais_comum)
            
            with col_stat3:
                if st.button("🧹 Limpar Histórico", type="secondary"):
                    st.session_state.db.clear_user_history(st.session_state.user_id)
                    st.success("Histórico limpo com sucesso!")
                    st.rerun()

    # ============================================
    # ABA 3 - ANALYTICS
    # ============================================

    with tab3:
        st.header("📊 Analytics e Relatórios")
        
        if st.session_state.user_plan == 'free':
            st.warning("📊 Recursos de Analytics disponíveis apenas no plano Pro!")
            st.info("Faça upgrade para acessar relatórios detalhados e análises avançadas.")
        else:
            # Analytics para plano Pro
            utils.show_analytics(st.session_state.user_id, st.session_state.db)

    # ============================================
    # ABA 4 - UPGRADE
    # ============================================

    with tab4:
        show_upgrade_page(st.session_state.user_id, st.session_state.user_plan, st.session_state.db)

    # ============================================
    # ABA 5 - SUPORTE E VALIDAÇÃO
    # ============================================

    with tab5:
        utils.show_validation_page()

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
        - Analytics avançados
        """)
    
    with col_biz3:
        st.subheader("🏢 Plano Empresarial")
        st.write("""
        - API dedicada
        - Treinamento personalizado
        - Integração com marketplaces
        - Analytics avançado
        - Contrato anual
        - Suporte 24/7
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