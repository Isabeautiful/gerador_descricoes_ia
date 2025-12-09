#!/usr/bin/env python3
"""
Script para inicializar e testar o banco de dados
"""

import sys
import os

# Adicionar o diretório atual ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

print("=" * 50)
print("INICIALIZAÇÃO DO BANCO DE DADOS")
print("=" * 50)

try:
    from database import Database
    
    # Criar instância do banco
    db = Database('data/descricoes.db')
    
    # Verificar tabelas criadas
    db.cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = db.cursor.fetchall()
    
    print(f"\n✅ Banco inicializado com sucesso!")
    print(f"📍 Local: {os.path.abspath('data/descricoes.db')}")
    print(f"📋 Tabelas encontradas ({len(tables)}):")
    
    for table in tables:
        db.cursor.execute(f"SELECT COUNT(*) FROM {table[0]}")
        count = db.cursor.fetchone()[0]
        print(f"   • {table[0]}: {count} registros")
    
    # Testar inserção de usuário de exemplo
    import hashlib
    test_hash = hashlib.sha256("senha_teste".encode()).hexdigest()
    user_id = db.add_user("teste@exemplo.com", test_hash)
    
    if user_id:
        print(f"\n👤 Usuário teste criado (ID: {user_id})")
    
    db.close()
    print("\n🎉 Todos os testes passaram! O banco está pronto.")
    print("\n💡 Agora execute: streamlit run app.py")
    
except Exception as e:
    print(f"\n❌ ERRO: {e}")
    print("\n🔧 Soluções:")
    print("1. Verifique permissões na pasta: chmod 755 data")
    print("2. Execute com: python3 init_database.py")
    print("3. Verifique se o SQLite está instalado")