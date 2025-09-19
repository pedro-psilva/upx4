# Meu Bairro Melhor

Uma plataforma colaborativa para participação cidadã em melhorias urbanas, desenvolvida em Python com Flask.

## 🚀 Funcionalidades

- **Mural Digital**: Moradores podem cadastrar sugestões de melhorias urbanas
- **Sistema de Votação**: Usuários podem votar nas propostas que consideram importantes
- **Comentários**: Sistema de comentários para discussão das propostas
- **Mapa Interativo**: Visualização das propostas em um mapa do bairro
- **Relatórios**: Dashboard com estatísticas e relatórios para apresentar às prefeituras
- **Categorização**: Propostas organizadas por categorias (iluminação, arborização, acessibilidade, etc.)
- **Sistema de Status**: Acompanhamento do progresso das propostas (pendente, aprovado, em andamento, concluído)

## 🛠️ Tecnologias Utilizadas

- **Backend**: Python 3.8+, Flask, SQLAlchemy
- **Frontend**: HTML5, CSS3, JavaScript, Tailwind CSS
- **Banco de Dados**: SQLite
- **Mapas**: Leaflet.js
- **Gráficos**: Chart.js
- **Ícones**: Font Awesome

## 📋 Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes do Python)

## 🚀 Instalação

1. **Clone o repositório**:
```bash
git clone <url-do-repositorio>
cd meu-bairro-melhor-UPX5
```

2. **Crie um ambiente virtual** (recomendado):
```bash
python -m venv venv

# No Windows:
venv\Scripts\activate

# No Linux/Mac:
source venv/bin/activate
```

3. **Instale as dependências**:
```bash
pip install -r requirements.txt
```

4. **Execute a aplicação**:
```bash
python init_db.py
```

5. **Acesse a aplicação**:
Abra seu navegador e acesse `http://localhost:5000`

## 📁 Estrutura do Projeto

```
meu-bairro-melhor-UPX5/
├── templates/                 # Templates HTML
│   ├── base.html             # Template base
│   ├── index.html            # Página principal
│   ├── mapa.html             # Página do mapa
│   ├── dashboard.html        # Dashboard de relatórios
│   ├── proposta_detalhes.html # Detalhes da proposta
│   ├── auth/                 # Templates de autenticação
│   └── proposals/            # Templates de propostas
├── models.py                 # Modelos do banco de dados
├── routes.py                 # Rotas da aplicação
├── init_db.py               # Arquivo principal da aplicação
├── requirements.txt         # Dependências Python
└── README.md               # Este arquivo
```

## 🎯 Como Usar

### Para Cidadãos:
1. **Cadastre-se** na plataforma
2. **Navegue** pelas propostas existentes
3. **Vote** nas propostas que considera importantes
4. **Comente** para discutir as propostas
5. **Crie** suas próprias propostas de melhoria
6. **Visualize** as propostas no mapa

### Para Administradores:
1. **Acesse o dashboard** para ver estatísticas
2. **Exporte relatórios** para apresentar às prefeituras
3. **Monitore** o engajamento da comunidade
4. **Acompanhe** o progresso das propostas

## 🔧 Configuração

### Banco de Dados
A aplicação usa SQLite por padrão. O arquivo `meu_bairro_melhor.db` será criado automaticamente na primeira execução.

### Personalização
- **Categorias**: Edite as categorias em `init_db.py`
- **Cores e tema**: Modifique o arquivo `templates/base.html`
- **Configurações**: Ajuste as configurações em `init_db.py`

## 📊 Funcionalidades Principais

### 1. Sistema de Propostas
- Criação de propostas com título, descrição e localização
- Categorização por tipo de melhoria
- Sistema de prioridades (baixa, média, alta)
- Status de acompanhamento

### 2. Sistema de Votação
- Usuários podem votar/desvotar em propostas
- Contagem automática de votos
- Prevenção de votos duplicados

### 3. Sistema de Comentários
- Comentários em propostas
- Identificação do autor
- Timestamp automático

### 4. Mapa Interativo
- Visualização das propostas no mapa
- Filtros por categoria, status e prioridade
- Busca por localização
- Marcadores coloridos por categoria

### 5. Dashboard e Relatórios
- Estatísticas gerais
- Gráficos de distribuição
- Relatórios exportáveis
- Propostas recentes

## 🔒 Segurança

- Senhas são criptografadas usando Werkzeug
- Sessões seguras com Flask-Login
- Validação de dados de entrada
- Proteção contra CSRF

## 🚀 Deploy

### Para Produção:
1. Configure uma chave secreta segura
2. Use um banco de dados PostgreSQL ou MySQL
3. Configure um servidor web (Nginx + Gunicorn)
4. Configure HTTPS
5. Configure variáveis de ambiente

### Exemplo com Gunicorn:
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 init_db:app
```

## 🤝 Contribuição

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 📞 Suporte

Para suporte, entre em contato através de:
- Email: suporte@meubairromelhor.com
- Issues no GitHub

## 🎉 Agradecimentos

- Comunidade Flask
- Desenvolvedores do Tailwind CSS
- Equipe do Leaflet.js
- Todos os contribuidores do projeto

---

**Desenvolvido com ❤️ para melhorar nossos bairros**
