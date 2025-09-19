# 🚀 Guia de Deploy - Meu Bairro Melhor

## 🌟 **Opção 1: Railway (Recomendado)**

### **Passo a Passo:**

1. **Criar conta no Railway:**
   - Acesse: https://railway.app
   - Faça login com GitHub

2. **Conectar repositório:**
   - Clique em "New Project"
   - Escolha "Deploy from GitHub repo"
   - Selecione seu repositório

3. **Configurar banco de dados:**
   - Clique em "New" → "Database" → "PostgreSQL"
   - Railway criará automaticamente

4. **Configurar variáveis de ambiente:**
   ```
   SECRET_KEY=sua-chave-super-secreta-aqui
   FLASK_ENV=production
   FLASK_HOST=0.0.0.0
   FLASK_PORT=$PORT
   ```

5. **Deploy automático:**
   - Railway fará deploy automaticamente
   - Sua app estará em: `https://seu-projeto.railway.app`

### **Comandos Railway:**
```bash
# Instalar Railway CLI
npm install -g @railway/cli

# Login
railway login

# Deploy local
railway up

# Ver logs
railway logs

# Abrir no navegador
railway open
```

---

## 🌟 **Opção 2: Render**

### **Passo a Passo:**

1. **Criar conta no Render:**
   - Acesse: https://render.com
   - Faça login com GitHub

2. **Criar Web Service:**
   - Clique em "New" → "Web Service"
   - Conecte seu repositório GitHub

3. **Configurações:**
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python run.py`
   - **Python Version**: 3.11

4. **Configurar banco PostgreSQL:**
   - Clique em "New" → "PostgreSQL"
   - Copie a URL de conexão

5. **Variáveis de ambiente:**
   ```
   SECRET_KEY=sua-chave-super-secreta-aqui
   DATABASE_URL=postgresql://user:pass@host:port/db
   FLASK_ENV=production
   FLASK_HOST=0.0.0.0
   FLASK_PORT=10000
   ```

6. **Deploy:**
   - Clique em "Create Web Service"
   - Render fará deploy automaticamente

---

## 🌟 **Opção 3: Heroku**

### **Passo a Passo:**

1. **Instalar Heroku CLI:**
   ```bash
   # Windows
   https://devcenter.heroku.com/articles/heroku-cli
   
   # Linux/Mac
   curl https://cli-assets.heroku.com/install.sh | sh
   ```

2. **Login e criar app:**
   ```bash
   heroku login
   heroku create meu-bairro-melhor
   ```

3. **Configurar banco PostgreSQL:**
   ```bash
   heroku addons:create heroku-postgresql:hobby-dev
   ```

4. **Configurar variáveis:**
   ```bash
   heroku config:set SECRET_KEY=sua-chave-super-secreta
   heroku config:set FLASK_ENV=production
   ```

5. **Deploy:**
   ```bash
   git add .
   git commit -m "Deploy inicial"
   git push heroku main
   ```

---

## 🌟 **Opção 4: Vercel (Frontend)**

### **Para hospedar apenas o frontend:**

1. **Instalar Vercel CLI:**
   ```bash
   npm install -g vercel
   ```

2. **Deploy:**
   ```bash
   vercel
   ```

3. **Configurar variáveis:**
   - Acesse o dashboard do Vercel
   - Configure as variáveis de ambiente

---

## 🔧 **Configurações Importantes**

### **Variáveis de Ambiente Obrigatórias:**
```bash
SECRET_KEY=sua-chave-super-secreta-aqui
FLASK_ENV=production
FLASK_HOST=0.0.0.0
FLASK_PORT=5000  # ou $PORT para Railway/Heroku
```

### **Para PostgreSQL:**
```bash
DATABASE_URL=postgresql://user:password@host:port/database
```

### **Arquivos de Configuração:**
- ✅ `railway.json` - Configuração Railway
- ✅ `Procfile` - Configuração Heroku
- ✅ `runtime.txt` - Versão Python
- ✅ `requirements.txt` - Dependências

---

## 📊 **Comparação das Opções**

| Plataforma | Gratuito | PostgreSQL | Fácil | Domínio |
|------------|----------|------------|-------|---------|
| Railway | ✅ Sim | ✅ Sim | ⭐⭐⭐ | ✅ Sim |
| Render | ✅ Sim | ✅ Sim | ⭐⭐ | ✅ Sim |
| Heroku | ⚠️ Limitado | ✅ Sim | ⭐⭐ | ✅ Sim |
| Vercel | ✅ Sim | ❌ Não | ⭐⭐⭐ | ✅ Sim |

---

## 🎯 **Recomendação Final**

**Para começar: Railway** 🚀
- Mais fácil de usar
- PostgreSQL incluído
- Deploy automático
- Domínio próprio

**Para produção: Render** 🏢
- Mais estável
- Melhor suporte
- Recursos avançados

---

## 🚨 **Dicas Importantes**

1. **Sempre use HTTPS** em produção
2. **Configure SECRET_KEY** forte
3. **Use PostgreSQL** para produção
4. **Configure backup** do banco
5. **Monitore logs** regularmente

**Qual opção você quer tentar primeiro?** 🚀
