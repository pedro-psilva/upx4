# 🚀 Configuração para Produção - Meu Bairro Melhor

## ⚠️ **IMPORTANTE: Leia antes de fazer deploy!**

Este guia contém as configurações essenciais para colocar a aplicação em produção de forma segura.

## 🔒 **Configurações de Segurança Obrigatórias**

### 1. **Variáveis de Ambiente**
```bash
# OBRIGATÓRIO: Chave secreta forte (gere uma nova!)
export SECRET_KEY="sua-chave-super-secreta-de-pelo-menos-32-caracteres"

# OBRIGATÓRIO: Banco de dados PostgreSQL
export DATABASE_URL="postgresql://usuario:senha@localhost:5432/meu_bairro_melhor"

# Configurações do Flask
export FLASK_ENV="production"
export FLASK_APP="wsgi.py"
```

### 2. **Gerar Chave Secreta Segura**
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

## 🗄️ **Banco de Dados PostgreSQL**

### Instalação (Ubuntu/Debian):
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo -u postgres createdb meu_bairro_melhor
sudo -u postgres createuser --interactive
```

### Configuração:
```sql
-- Conectar como postgres
sudo -u postgres psql

-- Criar usuário e banco
CREATE USER meu_bairro_user WITH PASSWORD 'senha_super_segura';
CREATE DATABASE meu_bairro_melhor OWNER meu_bairro_user;
GRANT ALL PRIVILEGES ON DATABASE meu_bairro_melhor TO meu_bairro_user;
\q
```

## 🚀 **Deploy com Gunicorn**

### 1. **Instalar dependências:**
```bash
pip install -r requirements.txt
```

### 2. **Executar com Gunicorn:**
```bash
# Desenvolvimento
gunicorn --config gunicorn.conf.py wsgi:app

# Produção (com mais workers)
gunicorn --workers 4 --bind 0.0.0.0:8000 wsgi:app
```

### 3. **Com systemd (recomendado):**
```bash
# Criar arquivo de serviço
sudo nano /etc/systemd/system/meu-bairro-melhor.service
```

Conteúdo do arquivo:
```ini
[Unit]
Description=Meu Bairro Melhor
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/path/to/meu-bairro-melhor-UPX5
Environment="PATH=/path/to/venv/bin"
Environment="SECRET_KEY=sua-chave-secreta"
Environment="DATABASE_URL=postgresql://usuario:senha@localhost:5432/meu_bairro_melhor"
Environment="FLASK_ENV=production"
ExecStart=/path/to/venv/bin/gunicorn --config gunicorn.conf.py wsgi:app
Restart=always

[Install]
WantedBy=multi-user.target
```

Ativar serviço:
```bash
sudo systemctl daemon-reload
sudo systemctl enable meu-bairro-melhor
sudo systemctl start meu-bairro-melhor
sudo systemctl status meu-bairro-melhor
```

## 🔒 **Nginx (Proxy Reverso)**

### Configuração do Nginx:
```nginx
server {
    listen 80;
    server_name seu-dominio.com;
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    # Servir arquivos estáticos diretamente
    location /static {
        alias /path/to/meu-bairro-melhor-UPX5/static;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

## 🔐 **HTTPS com Let's Encrypt**

### 1. **Instalar Certbot:**
```bash
sudo apt install certbot python3-certbot-nginx
```

### 2. **Obter certificado:**
```bash
sudo certbot --nginx -d seu-dominio.com
```

### 3. **Renovação automática:**
```bash
sudo crontab -e
# Adicionar linha:
0 12 * * * /usr/bin/certbot renew --quiet
```

## 📊 **Monitoramento**

### 1. **Logs do Gunicorn:**
```bash
sudo journalctl -u meu-bairro-melhor -f
```

### 2. **Logs do Nginx:**
```bash
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

## 🚨 **Checklist de Segurança**

- [ ] ✅ Chave secreta forte configurada
- [ ] ✅ Banco PostgreSQL configurado
- [ ] ✅ HTTPS habilitado
- [ ] ✅ Firewall configurado
- [ ] ✅ Logs de segurança ativados
- [ ] ✅ Backup do banco configurado
- [ ] ✅ Monitoramento ativo
- [ ] ✅ Atualizações de segurança automáticas

## 🔄 **Backup do Banco**

### Script de backup automático:
```bash
#!/bin/bash
# backup.sh
DATE=$(date +%Y%m%d_%H%M%S)
pg_dump $DATABASE_URL > backup_$DATE.sql
# Manter apenas os últimos 7 backups
find . -name "backup_*.sql" -mtime +7 -delete
```

### Agendar backup:
```bash
# Adicionar ao crontab
0 2 * * * /path/to/backup.sh
```

## 🎯 **Performance**

### Otimizações recomendadas:
1. **Cache Redis** para sessões
2. **CDN** para arquivos estáticos
3. **Compressão gzip** no Nginx
4. **Pool de conexões** do PostgreSQL

## 📞 **Suporte**

Em caso de problemas:
1. Verificar logs: `sudo journalctl -u meu-bairro-melhor -f`
2. Verificar status: `sudo systemctl status meu-bairro-melhor`
3. Reiniciar serviço: `sudo systemctl restart meu-bairro-melhor`

---

**⚠️ NUNCA use SQLite em produção!**
**⚠️ NUNCA use debug=True em produção!**
**⚠️ SEMPRE use HTTPS em produção!**
