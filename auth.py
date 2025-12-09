import streamlit as st
import hashlib
import re
from database import Database

def hash_password(password):
    """Cria hash da senha usando SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def validate_email(email):
    """Valida formato de email"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password(password):
    """Valida força da senha"""
    if len(password) < 6:
        return False, "A senha deve ter pelo menos 6 caracteres"
    return True, ""

def show_auth_page():
    """Exibe página de login/registro"""
    
    # Verificar se já estamos na página de auth
    if 'auth_page' not in st.session_state:
        st.session_state.auth_page = 'login'  # 'login' ou 'register'
    
    # Inicializar banco de dados
    if 'db' not in st.session_state:
        st.session_state.db = Database()
    
    # Layout centralizado
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.title("🔐 DescriçõesIA Pro")
        st.markdown("### Faça login para acessar o gerador")
        
        # Seletor de página
        auth_tab = st.radio(
            "",
            ["Entrar", "Criar Conta"],
            horizontal=True,
            label_visibility="collapsed"
        )
        
        if auth_tab == "Entrar":
            show_login_form()
        else:
            show_register_form()
        
        # Seção de informações
        st.divider()
        col_info1, col_info2 = st.columns(2)
        with col_info1:
            st.info("""
            **🎯 Plano Gratuito:**
            - 5 descrições/mês
            - Templates básicos
            - Histórico limitado
            """)
        
        with col_info2:
            st.success("""
            **🚀 Comece agora:**
            1. Crie sua conta
            2. Configure seu produto
            3. Gere descrições incríveis!
            """)

def show_login_form():
    """Exibe formulário de login"""
    
    with st.form("login_form"):
        email = st.text_input("Email", placeholder="seu@email.com")
        password = st.text_input("Senha", type="password")
        
        col1, col2 = st.columns([3, 1])
        with col1:
            remember = st.checkbox("Lembrar-me")
        with col2:
            login_button = st.form_submit_button("Entrar", type="primary")
        
        if login_button:
            if not email or not password:
                st.error("Por favor, preencha todos os campos.")
            elif not validate_email(email):
                st.error("Por favor, insira um email válido.")
            else:
                # Buscar usuário no banco
                user = st.session_state.db.get_user(email)
                if user:
                    user_id, stored_email, stored_hash, plan, created_at = user 
                    if hash_password(password) == stored_hash:
                        # Login bem-sucedido
                        st.session_state.user_id = user_id
                        st.session_state.user_email = email
                        st.session_state.user_plan = plan
                        st.success(f"Bem-vindo de volta, {email}!")
                        st.rerun()
                    else:
                        st.error("Senha incorreta.")
                else:
                    st.error("Usuário não encontrado. Crie uma conta primeiro.")
    
    # Link para recuperar senha
    st.caption("[Esqueci minha senha](#)")

def show_register_form():
    """Exibe formulário de registro"""
    
    with st.form("register_form"):
        email = st.text_input("Email", placeholder="seu@email.com")
        password = st.text_input("Senha", type="password")
        confirm_password = st.text_input("Confirmar Senha", type="password")
        
        # Termos de uso
        accept_terms = st.checkbox(
            "Aceito os Termos de Uso e Política de Privacidade"
        )
        
        col1, col2 = st.columns([3, 1])
        with col2:
            register_button = st.form_submit_button("Criar Conta", type="primary")
        
        if register_button:
            # Validações
            if not email or not password or not confirm_password:
                st.error("Por favor, preencha todos os campos.")
            elif not validate_email(email):
                st.error("Por favor, insira um email válido.")
            elif not accept_terms:
                st.error("Você deve aceitar os Termos de Uso.")
            else:
                is_valid, message = validate_password(password)
                if not is_valid:
                    st.error(message)
                elif password != confirm_password:
                    st.error("As senhas não coincidem.")
                else:
                    # Verificar se usuário já existe
                    existing_user = st.session_state.db.get_user(email)
                    if existing_user:
                        st.error("Este email já está em uso. Tente fazer login.")
                    else:
                        # Criar novo usuário
                        password_hash = hash_password(password)
                        user_id = st.session_state.db.add_user(email, password_hash)
                        
                        if user_id:
                            st.session_state.user_id = user_id
                            st.session_state.user_email = email
                            st.session_state.user_plan = 'free'
                            st.success(f"Conta criada com sucesso! Bem-vindo, {email}!")
                            st.balloons()
                            st.rerun()
                        else:
                            st.error("Erro ao criar conta. Tente novamente.")
    
    # Informações sobre segurança
    st.caption("🔒 Sua senha é criptografada e nunca compartilhada")

def logout_user():
    """Realiza logout do usuário"""
    st.session_state.user_id = None
    st.session_state.user_email = None
    st.session_state.user_plan = 'free'
    st.success("Você saiu da sua conta.")