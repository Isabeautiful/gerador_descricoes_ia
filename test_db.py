# test_db.py
import sqlite3
import os

print("🔍 Testando configuração do SQLite...")

# 1. Verificar se a pasta data existe
if not os.path.exists('data'):
    print("❌ Pasta 'data' não encontrada. Criando...")
    os.makedirs('data')
    print("✅ Pasta 'data' criada")

# 2. Tentar criar/conectar ao banco
try:
    conn = sqlite3.connect('data/descricoes.db')
    cursor = conn.cursor()
    
    # Criar tabela de teste
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS test_table (
            id INTEGER PRIMARY KEY,
            message TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Inserir um registro
    cursor.execute("INSERT INTO test_table (message) VALUES (?)", 
                   ("✅ Banco de dados funcionando!",))
    conn.commit()
    
    # Ler o registro
    cursor.execute("SELECT * FROM test_table")
    result = cursor.fetchall()
    
    print(f"✅ Banco de dados criado com sucesso!")
    print(f"📊 Registro inserido: {result}")
    
    conn.close()
    
except Exception as e:
    print(f"❌ Erro ao configurar banco de dados: {e}")
    print("💡 Verifique permissões de escrita na pasta")