#!/usr/bin/env python3
"""
Exemplo de uso da aplicação Meu Bairro Melhor
Este script demonstra como usar a API da aplicação
"""

import requests
import json
from datetime import datetime

# Configuração da API
BASE_URL = "http://localhost:5000"
API_URL = f"{BASE_URL}/api"

def exemplo_criar_usuario():
    """Exemplo de como criar um usuário"""
    print("👤 Criando usuário de exemplo...")
    
    user_data = {
        "name": "João Silva",
        "email": "joao@exemplo.com",
        "password": "123456"
    }
    
    response = requests.post(f"{BASE_URL}/register", json=user_data)
    
    if response.status_code == 200:
        data = response.json()
        if data.get('success'):
            print("✅ Usuário criado com sucesso!")
            return True
        else:
            print(f"❌ Erro: {data.get('message')}")
    else:
        print(f"❌ Erro HTTP: {response.status_code}")
    
    return False

def exemplo_fazer_login():
    """Exemplo de como fazer login"""
    print("🔐 Fazendo login...")
    
    login_data = {
        "email": "joao@exemplo.com",
        "password": "123456"
    }
    
    response = requests.post(f"{BASE_URL}/login", json=login_data)
    
    if response.status_code == 200:
        data = response.json()
        if data.get('success'):
            print("✅ Login realizado com sucesso!")
            return True
        else:
            print(f"❌ Erro: {data.get('message')}")
    else:
        print(f"❌ Erro HTTP: {response.status_code}")
    
    return False

def exemplo_buscar_propostas():
    """Exemplo de como buscar propostas"""
    print("📋 Buscando propostas...")
    
    response = requests.get(f"{API_URL}/proposals")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Encontradas {data.get('total', 0)} propostas")
        
        for proposal in data.get('proposals', [])[:3]:  # Mostrar apenas as 3 primeiras
            print(f"  📌 {proposal['title']} - {proposal['votes_count']} votos")
        
        return data.get('proposals', [])
    else:
        print(f"❌ Erro HTTP: {response.status_code}")
        return []

def exemplo_criar_proposta():
    """Exemplo de como criar uma proposta"""
    print("📝 Criando proposta de exemplo...")
    
    proposal_data = {
        "title": "Instalação de semáforo na Rua Principal",
        "description": "A Rua Principal precisa de um semáforo no cruzamento com a Avenida Central para melhorar o trânsito e a segurança dos pedestres.",
        "category": "transporte",
        "address": "Rua Principal, 123 - Centro",
        "latitude": -23.550520,
        "longitude": -46.633308,
        "priority": "high"
    }
    
    response = requests.post(f"{BASE_URL}/criar-proposta", json=proposal_data)
    
    if response.status_code == 200:
        data = response.json()
        if data.get('success'):
            print(f"✅ Proposta criada com sucesso! ID: {data.get('id')}")
            return data.get('id')
        else:
            print(f"❌ Erro: {data.get('message')}")
    else:
        print(f"❌ Erro HTTP: {response.status_code}")
    
    return None

def exemplo_votar_proposta(proposal_id):
    """Exemplo de como votar em uma proposta"""
    print(f"👍 Votando na proposta {proposal_id}...")
    
    response = requests.post(f"{BASE_URL}/votar/{proposal_id}")
    
    if response.status_code == 200:
        data = response.json()
        if data.get('success'):
            print(f"✅ Voto {'adicionado' if data.get('voted') else 'removido'}! Total: {data.get('votes_count')} votos")
        else:
            print(f"❌ Erro: {data.get('message')}")
    else:
        print(f"❌ Erro HTTP: {response.status_code}")

def exemplo_comentar_proposta(proposal_id):
    """Exemplo de como comentar em uma proposta"""
    print(f"💬 Comentando na proposta {proposal_id}...")
    
    comment_data = {
        "content": "Excelente proposta! Essa rua realmente precisa de um semáforo para melhorar a segurança."
    }
    
    response = requests.post(f"{BASE_URL}/comentar/{proposal_id}", json=comment_data)
    
    if response.status_code == 200:
        data = response.json()
        if data.get('success'):
            print("✅ Comentário adicionado com sucesso!")
        else:
            print(f"❌ Erro: {data.get('message')}")
    else:
        print(f"❌ Erro HTTP: {response.status_code}")

def exemplo_buscar_estatisticas():
    """Exemplo de como buscar estatísticas"""
    print("📊 Buscando estatísticas...")
    
    response = requests.get(f"{API_URL}/stats")
    
    if response.status_code == 200:
        data = response.json()
        print("✅ Estatísticas obtidas:")
        print(f"  📈 Total de propostas: {data.get('total_proposals', 0)}")
        print(f"  📊 Por status: {data.get('proposals_by_status', {})}")
        print(f"  🏷️  Por categoria: {data.get('proposals_by_category', {})}")
    else:
        print(f"❌ Erro HTTP: {response.status_code}")

def main():
    """Função principal do exemplo"""
    print("🚀 Exemplo de uso da API Meu Bairro Melhor")
    print("=" * 50)
    
    # Verificar se a aplicação está rodando
    try:
        response = requests.get(BASE_URL, timeout=5)
        if response.status_code != 200:
            print("❌ Aplicação não está rodando. Execute 'python run.py' primeiro.")
            return
    except requests.exceptions.RequestException:
        print("❌ Aplicação não está rodando. Execute 'python run.py' primeiro.")
        return
    
    print("✅ Aplicação está rodando!")
    print()
    
    # Executar exemplos
    try:
        # 1. Criar usuário
        exemplo_criar_usuario()
        print()
        
        # 2. Fazer login
        exemplo_fazer_login()
        print()
        
        # 3. Buscar propostas existentes
        propostas = exemplo_buscar_propostas()
        print()
        
        # 4. Criar nova proposta
        nova_proposta_id = exemplo_criar_proposta()
        print()
        
        if nova_proposta_id:
            # 5. Votar na proposta
            exemplo_votar_proposta(nova_proposta_id)
            print()
            
            # 6. Comentar na proposta
            exemplo_comentar_proposta(nova_proposta_id)
            print()
        
        # 7. Buscar estatísticas
        exemplo_buscar_estatisticas()
        print()
        
        print("🎉 Exemplo concluído com sucesso!")
        print("🌐 Acesse a aplicação em: http://localhost:5000")
        
    except Exception as e:
        print(f"❌ Erro durante a execução: {e}")

if __name__ == "__main__":
    main()
