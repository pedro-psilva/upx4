# 🚀 Instruções Rápidas - Meu Bairro Melhor

## ⚡ Execução Rápida

### 1. Instalar dependências
```bash
pip install -r requirements.txt
```

### 2. Executar aplicação
```bash
python run.py
```

### 3. Acessar aplicação
- **URL**: http://localhost:5000
- **Dashboard**: http://localhost:5000/dashboard
- **Mapa**: http://localhost:5000/mapa

## 🎯 Funcionalidades Principais

### Para Usuários:
1. **Cadastrar-se** na plataforma
2. **Criar propostas** de melhorias urbanas
3. **Votar** nas propostas existentes
4. **Comentar** nas propostas
5. **Visualizar** propostas no mapa

### Para Administradores:
1. **Acessar dashboard** com estatísticas
2. **Exportar relatórios** para prefeituras
3. **Monitorar** engajamento da comunidade

## 📱 Interface

- **Responsiva**: Funciona em desktop, tablet e mobile
- **Mapa interativo**: Visualização das propostas no mapa
- **Filtros**: Por categoria, status e prioridade
- **Busca**: Por texto e localização

## 🔧 Configuração

### Variáveis de Ambiente:
```bash
export FLASK_ENV=development  # ou production
export FLASK_HOST=127.0.0.1
export FLASK_PORT=5000
export SECRET_KEY=sua-chave-secreta
```

### Banco de Dados:
- **Desenvolvimento**: SQLite (arquivo local)
- **Produção**: PostgreSQL ou MySQL

## 🐳 Docker (Opcional)

### Executar com Docker:
```bash
docker-compose up -d
```

### Parar aplicação:
```bash
docker-compose down
```

## 📊 Exemplo de Uso

### Testar API:
```bash
python exemplo_uso.py
```

### Endpoints principais:
- `GET /` - Página principal
- `GET /mapa` - Mapa interativo
- `GET /dashboard` - Dashboard de relatórios
- `POST /register` - Cadastro de usuário
- `POST /login` - Login
- `POST /criar-proposta` - Criar proposta
- `POST /votar/<id>` - Votar em proposta
- `POST /comentar/<id>` - Comentar em proposta

## 🚨 Solução de Problemas

### Erro de importação:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Erro de banco de dados:
```bash
rm meu_bairro_melhor.db
python run.py
```

### Porta em uso:
```bash
export FLASK_PORT=5001
python run.py
```

## 📞 Suporte

- **Documentação**: README.md
- **Exemplo**: exemplo_uso.py
- **Configuração**: config.py

---

**🎉 Pronto! Sua aplicação está rodando!**
