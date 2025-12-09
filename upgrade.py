import streamlit as st
from datetime import datetime

def show_upgrade_page(user_id, user_plan, db):
    """Exibe página de upgrade de plano"""
    
    st.title("💎 Faça Upgrade do Seu Plano")
    
    # Mostrar plano atual
    st.header("Seu Plano Atual")
    col_current1, col_current2, col_current3 = st.columns([1, 2, 1])
    
    with col_current2:
        if user_plan == 'free':
            st.error("**🎯 Plano Gratuito**")
            descricoes_usadas = db.get_user_description_count(user_id)
            st.progress(min(descricoes_usadas / 5, 1.0))
            st.caption(f"{descricoes_usadas}/5 descrições usadas")
        elif user_plan == 'pro':
            st.success("**🚀 Plano Pro**")
            st.metric("Descrições geradas", db.get_user_description_count(user_id))
        else:
            st.info("**🏢 Plano Enterprise**")
    
    st.divider()
    
    # Mostrar opções de planos
    st.header("Escolha Seu Novo Plano")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("🎯 Gratuito")
        st.write("""
        - 5 descrições/mês
        - 3 templates básicos
        - Histórico de 10 descrições
        - Exportação .txt
        - Suporte por email
        """)
        st.write("**R$ 0/mês**")
        
        if user_plan == 'free':
            st.button("Plano Atual ✓", disabled=True, use_container_width=True)
        else:
            if st.button("Voltar para Gratuito", use_container_width=True):
                db.update_user_plan(user_id, 'free')
                st.session_state.user_plan = 'free'
                st.success("Plano alterado para Gratuito!")
                st.rerun()
    
    with col2:
        st.subheader("🚀 Pro")
        st.write("""
        - **Descrições ILIMITADAS**
        - 10+ templates profissionais
        - Histórico ilimitado
        - Exportação .txt, .html, .pdf
        - Analytics avançados
        - Suporte prioritário
        - Remoção de marca d'água
        """)
        st.write("**R$ 29/mês**")
        
        if user_plan == 'pro':
            st.button("Plano Atual ✓", disabled=True, use_container_width=True)
        else:
            if st.button("👉 Upgrade para Pro", type="primary", use_container_width=True):
                # Simular pagamento
                simulate_payment(user_id, 'pro', 29.90, db)
    
    with col3:
        st.subheader("🏢 Enterprise")
        st.write("""
        - API dedicada
        - +20 templates premium
        - Integração com marketplaces
        - Analytics em tempo real
        - Suporte 24/7
        - Treinamento da equipe
        - Dashboard personalizado
        """)
        st.write("**R$ 299/mês**")
        
        if user_plan == 'enterprise':
            st.button("Plano Atual ✓", disabled=True, use_container_width=True)
        else:
            if st.button("Solicitar Enterprise", use_container_width=True):
                show_enterprise_form()
    
    st.divider()
    
    # Calculadora de ROI
    st.header("📈 Veja Seu Retorno")
    
    col_roi1, col_roi2 = st.columns(2)
    
    with col_roi1:
        produtos_mes = st.slider(
            "Produtos que você vende por mês",
            min_value=1,
            max_value=100,
            value=10
        )
        
        tempo_por_produto = st.slider(
            "Horas gastas por descrição",
            min_value=0.5,
            max_value=5.0,
            value=2.0,
            step=0.5
        )
    
    with col_roi2:
        valor_hora = st.number_input(
            "Valor da sua hora (R$)",
            min_value=20,
            max_value=200,
            value=50
        )
        
        # Calcular economia
        horas_mes = produtos_mes * tempo_por_produto
        economia_mes = horas_mes * valor_hora
        economia_ano = economia_mes * 12
        
        st.metric("Economia mensal", f"R$ {economia_mes:,.2f}")
        st.metric("Economia anual", f"R$ {economia_ano:,.2f}")
        
        if economia_mes > 29.90:
            st.success(f"**ROI de {(economia_mes / 29.90 - 1) * 100:.0f}% por mês!**")
    
    st.divider()
    
    # Métodos de pagamento
    st.header("💳 Métodos de Pagamento")
    
    payment_cols = st.columns(4)
    
    with payment_cols[0]:
        st.image("https://upload.wikimedia.org/wikipedia/commons/b/ba/Stripe_Logo%2C_revised_2016.svg", width=80)
        st.caption("Cartão de Crédito")
    
    with payment_cols[1]:
        st.image("https://upload.wikimedia.org/wikipedia/commons/0/01/PayPal_Logo_2014.svg", width=80)
        st.caption("PayPal")
    
    with payment_cols[2]:
        st.image("https://upload.wikimedia.org/wikipedia/commons/0/04/Pix_payment_method_logo.svg", width=80)
        st.caption("Pix")
    
    with payment_cols[3]:
        st.image("https://upload.wikimedia.org/wikipedia/commons/7/78/MercadoPago_2019_logo.svg", width=80)
        st.caption("Mercado Pago")
    
    st.caption("*Pagamento recorrente mensal. Cancele a qualquer momento.*")

def simulate_payment(user_id, plan, amount, db):
    """Simula um pagamento e atualiza o plano do usuário"""
    
    with st.spinner("Processando pagamento..."):
        # Simular processamento
        import time
        time.sleep(2)
        
        # Registrar pagamento no banco
        db.record_payment(user_id, plan, amount)
        
        # Atualizar plano do usuário
        db.update_user_plan(user_id, plan)
        st.session_state.user_plan = plan
        
        st.success(f"""
        ✅ Pagamento processado com sucesso!
        
        **Plano {plan.upper()} ativado!**
        - Valor: R$ {amount:.2f}
        - Data: {datetime.now().strftime('%d/%m/%Y')}
        - Próxima cobrança: {(datetime.now().replace(day=28) if datetime.now().day > 28 else datetime.now()).strftime('%d/%m/%Y')}
        
        **Recursos agora disponíveis:**
        {'- Descrições ilimitadas' if plan == 'pro' else ''}
        {'- Todos os templates' if plan == 'pro' else ''}
        {'- Analytics avançados' if plan == 'pro' else ''}
        
        Obrigado por fazer upgrade! 🎉
        """)
        
        # Mostrar recibo
        with st.expander("📄 Ver Recibo", expanded=True):
            st.code(f"""
            ==================================
            DESCRIÇÕESIA PRO - RECIBO
            ==================================
            Cliente: {st.session_state.user_email}
            Plano: {plan.upper()}
            Valor: R$ {amount:.2f}
            Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}
            ID da Transação: TX{datetime.now().strftime('%Y%m%d%H%M%S')}
            Status: APROVADO
            ==================================
            """)
        
        st.balloons()

def show_enterprise_form():
    """Exibe formulário para plano Enterprise"""
    
    st.info("""
    **Plano Enterprise - Personalizado para sua empresa**
    
    Para o plano Enterprise, entre em contato com nossa equipe de vendas
    para uma demonstração personalizada e proposta comercial.
    """)
    
    with st.form("enterprise_form"):
        st.subheader("📞 Solicitar Contato")
        
        nome_empresa = st.text_input("Nome da Empresa")
        nome_contato = st.text_input("Nome do Contato")
        telefone = st.text_input("Telefone")
        funcionarios = st.number_input("Número de funcionários", min_value=1, max_value=1000)
        necessidade = st.text_area("Descreva sua necessidade")
        
        if st.form_submit_button("Enviar Solicitação", type="primary"):
            st.success("""
            ✅ Solicitação enviada com sucesso!
            
            Nossa equipe entrará em contato em até 24 horas úteis
            para agendar uma demonstração personalizada.
            
            **Contato:** vendas@descricoesia.com.br
            **Telefone:** (11) 99999-9999
            """)