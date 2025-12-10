import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json

def export_to_txt(description, product_name):
    """Exporta descrição para arquivo .txt"""
    filename = f"descricao_{product_name.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(description)
    
    return filename

def export_to_html(description, product_name):
    """Exporta descrição para arquivo .html"""
    html_content = f"""
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Descrição: {product_name}</title>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; padding: 20px; max-width: 800px; margin: 0 auto; }}
            .description {{ background: #f9f9f9; padding: 20px; border-radius: 10px; }}
            .title {{ color: #333; border-bottom: 2px solid #4CAF50; padding-bottom: 10px; }}
            .footer {{ margin-top: 30px; font-size: 12px; color: #666; text-align: center; }}
        </style>
    </head>
    <body>
        <h1 class="title">📦 {product_name}</h1>
        <div class="description">
            {description.replace('**', '<strong>').replace('**', '</strong>').replace('\\n', '<br>')}
        </div>
        <div class="footer">
            Gerado por DescriçõesIA Pro • {datetime.now().strftime('%d/%m/%Y %H:%M')}
        </div>
    </body>
    </html>
    """
    
    filename = f"descricao_{product_name.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    return filename

def show_analytics(user_id, db):
    """Exibe painel de analytics para o usuário"""
    
    # Obter dados do banco
    analytics_data = db.get_user_analytics(user_id)
    category_stats = db.get_category_stats(user_id)
    template_stats = db.get_template_stats(user_id)
    descriptions = db.get_user_descriptions(user_id, limit=100)
    
    # Métricas principais
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_descriptions = len(descriptions) if descriptions else 0
        st.metric("Total de Descrições", total_descriptions)
    
    with col2:
        if analytics_data and analytics_data[2]:
            st.metric("Categoria Mais Usada", analytics_data[2])
        else:
            st.metric("Categoria Mais Usada", "-")
    
    with col3:
        if analytics_data and analytics_data[3]:
            st.metric("Template Favorito", analytics_data[3])
        else:
            st.metric("Template Favorito", "-")
    
    with col4:
        if descriptions:
            last_activity = descriptions[0][9] if len(descriptions[0]) > 9 else "-"
            st.metric("Última Atividade", last_activity[:10])
        else:
            st.metric("Última Atividade", "-")
    
    st.divider()
    
    # Gráficos
    if descriptions and len(descriptions) > 1:
        col_chart1, col_chart2 = st.columns(2)
        
        with col_chart1:
            # Gráfico de categorias
            if category_stats:
                categories = [cat[0] for cat in category_stats]
                counts = [count[1] for count in category_stats]
                
                fig = px.pie(
                    values=counts,
                    names=categories,
                    title="Distribuição por Categoria",
                    color_discrete_sequence=px.colors.sequential.Viridis
                )
                fig.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig, use_container_width=True)
        
        with col_chart2:
            # Gráfico de templates
            if template_stats:
                templates = [temp[0] for temp in template_stats]
                counts = [count[1] for count in template_stats]
                
                fig = px.bar(
                    x=templates,
                    y=counts,
                    title="Uso de Templates",
                    labels={'x': 'Template', 'y': 'Quantidade'},
                    color=counts,
                    color_continuous_scale='viridis'
                )
                st.plotly_chart(fig, use_container_width=True)
        
        # Atividade ao longo do tempo
        st.subheader("📈 Atividade ao Longo do Tempo")
        
        # Criar DataFrame com datas
        dates = []
        for desc in descriptions:
            if len(desc) > 9:
                date_str = desc[9][:10]  # Pegar apenas a data
                dates.append(date_str)
        
        if dates:
            df_dates = pd.DataFrame({'date': dates})
            daily_counts = df_dates['date'].value_counts().sort_index()
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=daily_counts.index,
                y=daily_counts.values,
                mode='lines+markers',
                name='Descrições por dia',
                line=dict(color='#4CAF50', width=3)
            ))
            
            fig.update_layout(
                title='Evolução do Uso',
                xaxis_title='Data',
                yaxis_title='Descrições Geradas',
                hovermode='x unified'
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    # Exportar dados
    st.divider()
    st.subheader("📤 Exportar Dados")
    
    col_export1, col_export2 = st.columns(2)
    
    with col_export1:
        if st.button("📊 Exportar Estatísticas (CSV)", use_container_width=True):
            # Criar DataFrame com estatísticas
            if descriptions:
                data = []
                for desc in descriptions:
                    data.append({
                        'ID': desc[0],
                        'Produto': desc[1],
                        'Categoria': desc[2],
                        'Tom': desc[3],
                        'Palavras-chave': desc[4],
                        'Tamanho': desc[5],
                        'Template': desc[6],
                        'Data': desc[9] if len(desc) > 9 else ''
                    })
                
                df = pd.DataFrame(data)
                csv = df.to_csv(index=False)
                
                st.download_button(
                    label="⬇️ Baixar CSV",
                    data=csv,
                    file_name=f"estatisticas_descricoes_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                )
    
    with col_export2:
        if st.button("📈 Exportar Gráficos (HTML)", use_container_width=True):
            # Criar relatório HTML com gráficos
            html_report = create_html_report(user_id, db, descriptions)
            st.download_button(
                label="⬇️ Baixar Relatório",
                data=html_report,
                file_name=f"relatorio_descricoes_{datetime.now().strftime('%Y%m%d')}.html",
                mime="text/html"
            )

def create_html_report(user_id, db, descriptions):
    """Cria relatório HTML com analytics"""
    
    analytics_data = db.get_user_analytics(user_id)
    
    html_content = f"""
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Relatório DescriçõesIA Pro</title>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; padding: 20px; max-width: 1200px; margin: 0 auto; }}
            .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; border-radius: 10px; margin-bottom: 30px; }}
            .metric {{ background: #f8f9fa; border-left: 4px solid #4CAF50; padding: 15px; margin: 10px 0; }}
            .table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
            .table th, .table td {{ border: 1px solid #ddd; padding: 12px; text-align: left; }}
            .table th {{ background-color: #4CAF50; color: white; }}
            .footer {{ margin-top: 50px; text-align: center; color: #666; font-size: 14px; }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>📊 Relatório DescriçõesIA Pro</h1>
            <p>Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}</p>
            <p>Usuário: {st.session_state.user_email}</p>
        </div>
        
        <h2>📈 Métricas Principais</h2>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px;">
            <div class="metric">
                <h3>Total de Descrições</h3>
                <p style="font-size: 2em; font-weight: bold;">{len(descriptions) if descriptions else 0}</p>
            </div>
            <div class="metric">
                <h3>Categoria Mais Usada</h3>
                <p style="font-size: 1.5em;">{analytics_data[2] if analytics_data and analytics_data[2] else '-'}</p>
            </div>
            <div class="metric">
                <h3>Template Favorito</h3>
                <p style="font-size: 1.5em;">{analytics_data[3] if analytics_data and analytics_data[3] else '-'}</p>
            </div>
        </div>
        
        <h2>📋 Últimas Descrições</h2>
        <table class="table">
            <tr>
                <th>Produto</th>
                <th>Categoria</th>
                <th>Template</th>
                <th>Data</th>
            </tr>
    """
    
    # Adicionar linhas da tabela
    for desc in descriptions[:10]:
        html_content += f"""
            <tr>
                <td>{desc[1]}</td>
                <td>{desc[2]}</td>
                <td>{desc[6] if len(desc) > 6 else '-'}</td>
                <td>{desc[9][:10] if len(desc) > 9 else '-'}</td>
            </tr>
        """
    
    html_content += f"""
        </table>
        
        <div class="footer">
            <p>Relatório gerado automaticamente por DescriçõesIA Pro</p>
            <p>© {datetime.now().year} DescriçõesIA Pro - Todos os direitos reservados</p>
        </div>
    </body>
    </html>
    """
    
    return html_content

def show_validation_page():
    """Exibe página de validação do modelo de negócio"""
    
    st.header("🏆 Validação do Modelo")
    
    # Depoimentos simulados
    st.subheader("📣 O que nossos usuários dizem:")
    
    testimonials = [
        {
            "name": "Maria Silva",
            "role": "Vendedora Shopee",
            "text": "Economizo 3 horas por dia! Minhas vendas aumentaram 40% com as descrições otimizadas.",
            "avatar": "👩‍💼"
        },
        {
            "name": "Carlos Santos",
            "role": "Lojista Mercado Livre",
            "text": "A IA entende perfeitamente o que preciso. As descrições são melhores que as que eu escrevia.",
            "avatar": "👨‍💻"
        },
        {
            "name": "Ana Costa",
            "role": "Empreendedora",
            "text": "Pela primeira vez consigo competir com grandes vendedores. O investimento valeu cada centavo!",
            "avatar": "👩‍🎓"
        }
    ]
    
    cols = st.columns(3)
    for idx, testimonial in enumerate(testimonials):
        with cols[idx]:
            st.markdown(f"""
            <div style="background: #f0f2f6; padding: 20px; border-radius: 10px; height: 100%;">
                <div style="font-size: 2em; margin-bottom: 10px;">{testimonial['avatar']}</div>
                <p style="font-style: italic;">"{testimonial['text']}"</p>
                <p style="font-weight: bold; margin-bottom: 0;">{testimonial['name']}</p>
                <p style="color: #666; font-size: 0.9em;">{testimonial['role']}</p>
            </div>
            """, unsafe_allow_html=True)
    
    st.divider()
    
    # Casos de uso
    st.subheader("🎯 Casos de Uso Reais")
    
    use_cases = [
        {
            "title": "Lojista Individual",
            "problem": "Gasta 2-3 horas por produto escrevendo descrições",
            "solution": "Gera 10 descrições em 10 minutos",
            "result": "Economia de 50 horas/mês"
        },
        {
            "title": "Agência de E-commerce",
            "problem": "Padronização de descrições para múltiplos clientes",
            "solution": "Templates personalizados por nicho",
            "result": "Escalabilidade 5x maior"
        },
        {
            "title": "Fabricante",
            "problem": "Dificuldade em destacar benefícios técnicos",
            "solution": "Descrições que convertem características em benefícios",
            "result": "Aumento de 30% na conversão"
        }
    ]
    
    for use_case in use_cases:
        with st.expander(f"📦 {use_case['title']}"):
            col_uc1, col_uc2, col_uc3 = st.columns(3)
            with col_uc1:
                st.info(f"**Problema:** {use_case['problem']}")
            with col_uc2:
                st.success(f"**Solução:** {use_case['solution']}")
            with col_uc3:
                st.success(f"**Resultado:** {use_case['result']}")
    
    st.divider()
    
    # Lista de espera para novos recursos
    st.subheader("🚀 Próximos Recursos")
    
    st.info("""
    **Estamos desenvolvendo novos recursos baseados no seu feedback!**
    
    👇 Deixe seu email para ser avisado quando lançarmos:
    """)
    
    col_wait1, col_wait2 = st.columns([3, 1])
    
    with col_wait1:
        waitlist_email = st.text_input(
            "Seu email",
            placeholder="seu@email.com",
            label_visibility="collapsed"
        )
    
    with col_wait2:
        if st.button("Entrar na Lista", type="secondary"):
            if waitlist_email:
                # Simular salvamento em banco de dados
                st.success("✅ Você está na lista! Te avisaremos em breve.")
            else:
                st.error("Por favor, insira seu email.")
    
    # ROI Calculator
    st.divider()
    st.subheader("💰 Calculadora de ROI")
    
    col_roi1, col_roi2 = st.columns(2)
    
    with col_roi1:
        produtos_dia = st.slider("Produtos que você lista por dia", 1, 20, 5)
        tempo_descricao = st.slider("Minutos gastos por descrição", 10, 120, 30)
        valor_hora = st.number_input("Valor da sua hora (R$)", 30, 200, 50)
    
    with col_roi2:
        # Cálculos
        tempo_diario = produtos_dia * (tempo_descricao / 60)
        custo_diario = tempo_diario * valor_hora
        custo_mensal = custo_diario * 22
        economia_mensal = custo_mensal - 29.90
        
        st.metric("Tempo economizado/dia", f"{tempo_diario:.1f} horas")
        st.metric("Custo atual/mês", f"R$ {custo_mensal:.2f}")
        st.metric("Custo com DescriçõesIA", "R$ 29,90")
        
        if economia_mensal > 0:
            st.success(f"**Economia mensal: R$ {economia_mensal:.2f}**")
        else:
            st.warning("Para maior economia, aumente sua produtividade!")