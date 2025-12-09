import sqlite3
import os
import streamlit as st

class Database:
    def __init__(self, db_name='data/descricoes.db'):
        """Inicializa a conexão com o banco de dados SQLite"""
        try:
            # Criar diretório se não existir
            os.makedirs(os.path.dirname(db_name), exist_ok=True)
            
            # Conectar ao banco
            self.conn = sqlite3.connect(db_name, check_same_thread=False)
            self.cursor = self.conn.cursor()
            
            # Criar todas as tabelas
            self.create_tables()
            
            st.success("✅ Banco de dados conectado com sucesso!")
            print(f"🗄️  Banco de dados: {os.path.abspath(db_name)}")
            
        except Exception as e:
            st.error(f"❌ Erro ao conectar ao banco: {str(e)}")
            raise
    
    def create_tables(self):
        """Cria TODAS as tabelas necessárias"""
        
        # Tabela de usuários
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                plan TEXT DEFAULT 'free',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Tabela de descrições
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS descriptions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                product_name TEXT NOT NULL,
                category TEXT NOT NULL,
                tone TEXT NOT NULL,
                keywords TEXT,
                size TEXT,
                template TEXT,
                description TEXT NOT NULL,
                formato TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # Tabela de analytics (simplificada)
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS analytics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                total_descriptions INTEGER DEFAULT 0,
                most_used_category TEXT,
                last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        self.conn.commit()
        print("📋 Tabelas criadas/verificadas")
    
    # ========== MÉTODOS PARA USUÁRIOS ==========
    
    def add_user(self, email, password_hash, plan='free'):
        """Adiciona um novo usuário"""
        try:
            self.cursor.execute('''
                INSERT INTO users (email, password_hash, plan) 
                VALUES (?, ?, ?)
            ''', (email, password_hash, plan))
            self.conn.commit()
            user_id = self.cursor.lastrowid
            print(f"👤 Usuário criado: {email} (ID: {user_id})")
            return user_id
        except sqlite3.IntegrityError:
            return None  # Email já existe
    
    def get_user(self, email):
        """Obtém um usuário pelo email"""
        self.cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
        return self.cursor.fetchone()
    
    def get_user_by_id(self, user_id):
        """Obtém um usuário pelo ID"""
        self.cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
        return self.cursor.fetchone()
    
    # ========== MÉTODOS PARA DESCRIÇÕES ==========
    
    def save_description(self, user_id, product_name, category, tone, keywords, 
                         size, template, description, formato):
        """Salva uma descrição gerada"""
        try:
            self.cursor.execute('''
                INSERT INTO descriptions 
                (user_id, product_name, category, tone, keywords, size, template, description, formato)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (user_id, product_name, category, tone, keywords, size, 
                  template, description, formato))
            self.conn.commit()
            
            # Atualizar analytics
            self._update_analytics(user_id, category)
            
            desc_id = self.cursor.lastrowid
            print(f"📝 Descrição salva: {product_name} (ID: {desc_id})")
            return desc_id
            
        except Exception as e:
            print(f"❌ Erro ao salvar descrição: {e}")
            return None
    
    def get_user_descriptions(self, user_id, limit=20):
        """Obtém descrições de um usuário"""
        self.cursor.execute('''
            SELECT * FROM descriptions 
            WHERE user_id = ? 
            ORDER BY created_at DESC 
            LIMIT ?
        ''', (user_id, limit))
        return self.cursor.fetchall()
    
    def get_user_description_count(self, user_id):
        """Conta descrições de um usuário"""
        self.cursor.execute('SELECT COUNT(*) FROM descriptions WHERE user_id = ?', (user_id,))
        return self.cursor.fetchone()[0]
    
    # ========== MÉTODOS AUXILIARES ==========
    
    def _update_analytics(self, user_id, category):
        """Atualiza estatísticas do usuário"""
        try:
            # Verificar se já existe registro
            self.cursor.execute('SELECT * FROM analytics WHERE user_id = ?', (user_id,))
            existing = self.cursor.fetchone()
            
            if existing:
                # Atualizar
                self.cursor.execute('''
                    UPDATE analytics 
                    SET total_descriptions = total_descriptions + 1,
                        most_used_category = ?,
                        last_activity = CURRENT_TIMESTAMP
                    WHERE user_id = ?
                ''', (category, user_id))
            else:
                # Criar novo
                self.cursor.execute('''
                    INSERT INTO analytics (user_id, total_descriptions, most_used_category)
                    VALUES (?, 1, ?)
                ''', (user_id, category))
            
            self.conn.commit()
            
        except Exception as e:
            print(f"⚠️ Erro em analytics: {e}")
    
    def close(self):
        """Fecha a conexão"""
        self.conn.close()