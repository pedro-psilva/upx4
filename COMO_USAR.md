# 🚀 Meu Bairro Melhor - Como Usar

## ⚡ **Execução Rápida**

### 1. Instalar dependências
```bash
pip install -r requirements.txt
```

### 2. Executar aplicação
```bash
python app.py
```

### 3. Acessar aplicação
- **URL**: http://localhost:5000
- **Dashboard**: http://localhost:5000/dashboard
- **Mapa**: http://localhost:5000/mapa

## 🎯 **Funcionalidades Implementadas**

### ✅ **Sistema de Autenticação**
- Login e cadastro de usuários
- Sessões seguras
- Proteção de rotas

### ✅ **Sistema de Propostas**
- Criar propostas de melhorias urbanas
- Categorização (iluminação, arborização, etc.)
- Sistema de prioridades
- Localização no mapa

### ✅ **Sistema de Votação**
- Votar/desvotar em propostas
- Contagem automática de votos
- Prevenção de votos duplicados

### ✅ **Sistema de Comentários**
- Comentar em propostas
- Identificação do autor
- Timestamp automático

### ✅ **Mapa Interativo**
- Visualização das propostas no mapa
- Filtros por categoria e status
- Busca por localização
- Marcadores coloridos

### ✅ **Dashboard e Relatórios**
- Estatísticas gerais
- Gráficos de distribuição
- Propostas recentes
- Relatórios exportáveis

## 🗄️ **Banco de Dados**

**Atual**: SQLite (arquivo local)
- ✅ **Simples**: Funciona automaticamente
- ✅ **Desenvolvimento**: Perfeito para testes
- ✅ **Sem configuração**: Pronto para usar

**Futuro**: PostgreSQL (quando precisar)
- 🚀 **Produção**: Mais robusto
- 📊 **Performance**: Melhor para muitos usuários
- 🔧 **Configuração**: Via variável de ambiente

## 📱 **Interface**

- **Responsiva**: Funciona em desktop, tablet e mobile
- **Modern**: Tailwind CSS
- **Interativa**: JavaScript para mapas e formulários
- **Intuitiva**: Fácil de usar

## 🔧 **Estrutura do Projeto**

```
meu-bairro-melhor-UPX5/
├── app.py                 # Aplicação principal
├── requirements.txt       # Dependências
├── templates/            # Templates HTML
│   ├── base.html         # Template base
│   ├── index.html        # Página principal
│   ├── mapa.html         # Mapa interativo
│   ├── dashboard.html    # Dashboard
│   └── ...
└── README.md             # Documentação
```

## 🎮 **Como Testar**

1. **Execute**: `python app.py`
2. **Acesse**: http://localhost:5000
3. **Cadastre-se** na plataforma
4. **Crie uma proposta** de melhoria
5. **Vote** em propostas existentes
6. **Comente** nas propostas
7. **Visualize** no mapa
8. **Veja** o dashboard

## 🚨 **Solução de Problemas**

### Erro de importação:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Erro de banco de dados:
```bash
rm meu_bairro_melhor.db
python app.py
```

### Porta em uso:
```bash
set FLASK_PORT=5001
python app.py
```

## 🎉 **Pronto!**

Sua aplicação está funcionando perfeitamente! 

**Foco na lógica e funcionalidades** - o banco de dados será configurado quando necessário.

**Execute `python app.py` e comece a testar!** 🚀
