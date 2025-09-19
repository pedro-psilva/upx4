# 🗄️ Configuração do Banco de Dados

## 📋 **Opções de Banco de Dados**

### **1. Desenvolvimento (SQLite) - Padrão**
```bash
# Já configurado! Funciona automaticamente
python run.py
```

### **2. Produção (PostgreSQL) - Recomendado**

#### **Instalação do PostgreSQL:**

**Windows:**
1. Baixe o PostgreSQL: https://www.postgresql.org/download/windows/
2. Instale com as configurações padrão
3. Anote a senha do usuário `postgres`

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo -u postgres psql
```

**macOS:**
```bash
brew install postgresql
brew services start postgresql
```

#### **Configuração do Banco:**

1. **Criar banco de dados:**
```sql
-- Conectar como postgres
sudo -u postgres psql

-- Criar banco e usuário
CREATE DATABASE meu_bairro_melhor;
CREATE USER meu_bairro_user WITH PASSWORD 'sua_senha_aqui';
GRANT ALL PRIVILEGES ON DATABASE meu_bairro_melhor TO meu_bairro_user;
\q
```

2. **Configurar variável de ambiente:**
```bash
# Windows
set DATABASE_URL=postgresql://meu_bairro_user:sua_senha_aqui@localhost:5432/meu_bairro_melhor

# Linux/Mac
export DATABASE_URL=postgresql://meu_bairro_user:sua_senha_aqui@localhost:5432/meu_bairro_melhor
```

3. **Executar aplicação:**
```bash
python run.py
```

## 🚀 **Opções de Deploy**

### **Heroku (Gratuito)**
```bash
# Instalar Heroku CLI
# Criar app
heroku create meu-bairro-melhor

# Configurar banco PostgreSQL
heroku addons:create heroku-postgresql:hobby-dev

# Deploy
git add .
git commit -m "Deploy inicial"
git push heroku main
```

### **Railway (Gratuito)**
```bash
# Instalar Railway CLI
npm install -g @railway/cli

# Login e deploy
railway login
railway init
railway up
```

### **Render (Gratuito)**
1. Conecte seu repositório GitHub
2. Configure as variáveis de ambiente
3. Deploy automático

## 🔧 **Configurações Avançadas**

### **Variáveis de Ambiente (.env)**
```bash
# Criar arquivo .env
SECRET_KEY=sua-chave-super-secreta-aqui
DATABASE_URL=postgresql://user:password@localhost:5432/meu_bairro_melhor
FLASK_ENV=production
FLASK_HOST=0.0.0.0
FLASK_PORT=5000
```

### **Docker com PostgreSQL**
```yaml
# docker-compose.yml
version: '3.8'
services:
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: meu_bairro_melhor
      POSTGRES_USER: meu_bairro_user
      POSTGRES_PASSWORD: sua_senha_aqui
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  web:
    build: .
    environment:
      DATABASE_URL: postgresql://meu_bairro_user:sua_senha_aqui@db:5432/meu_bairro_melhor
    depends_on:
      - db
    ports:
      - "5000:5000"

volumes:
  postgres_data:
```

## 📊 **Comparação de Bancos**

| Banco | Desenvolvimento | Produção | Custo | Performance |
|-------|----------------|----------|-------|-------------|
| SQLite | ✅ Excelente | ❌ Limitado | Gratuito | Baixa |
| PostgreSQL | ✅ Bom | ✅ Excelente | Gratuito | Alta |
| MySQL | ✅ Bom | ✅ Bom | Gratuito | Alta |
| MongoDB | ✅ Bom | ✅ Bom | Pago | Média |

## 🎯 **Recomendação Final**

- **Desenvolvimento**: SQLite (já configurado)
- **Produção**: PostgreSQL (recomendado)
- **Deploy**: Heroku ou Railway (gratuito)

**A aplicação funciona perfeitamente com SQLite para desenvolvimento e testes!** 🚀
