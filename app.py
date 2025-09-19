#!/usr/bin/env python3
"""
Meu Bairro Melhor - Aplicação Principal
Foco na lógica e funcionalidades
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os
import requests
import json

# Criar aplicação Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'sua-chave-secreta-aqui'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///meu_bairro_melhor.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar extensões
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Por favor, faça login para acessar esta página.'

# Modelos do banco de dados
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    password_hash = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Category(db.Model):
    id = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    icon = db.Column(db.String(50))
    color = db.Column(db.String(7))
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'icon': self.icon,
            'color': self.color
        }

class Proposal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), db.ForeignKey('category.id'), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    address = db.Column(db.String(300), nullable=False)
    status = db.Column(db.String(20), default='pending')
    priority = db.Column(db.String(10), default='medium')
    votes_count = db.Column(db.Integer, default=0)
    comments_count = db.Column(db.Integer, default=0)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    author = db.relationship('User', backref='proposals')
    category_obj = db.relationship('Category', backref='proposals')
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'category': self.category,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'address': self.address,
            'status': self.status,
            'priority': self.priority,
            'votes_count': self.votes_count,
            'comments_count': self.comments_count,
            'author_name': self.author.name if self.author else 'Anônimo',
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class Vote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    proposal_id = db.Column(db.Integer, db.ForeignKey('proposal.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    user = db.relationship('User', backref='votes')
    proposal = db.relationship('Proposal', backref='votes')
    
    __table_args__ = (db.UniqueConstraint('proposal_id', 'user_id', name='unique_vote'),)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    proposal_id = db.Column(db.Integer, db.ForeignKey('proposal.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    user = db.relationship('User', backref='comments')
    proposal = db.relationship('Proposal', backref='comments')
    
    @property
    def author_name(self):
        return self.user.name if self.user else 'Usuário Anônimo'

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

# ===== FUNÇÕES DE BUSCA =====

def buscar_cep(cep):
    """Buscar dados do CEP usando ViaCEP"""
    try:
        # Limpar CEP (remover caracteres não numéricos)
        cep_limpo = ''.join(filter(str.isdigit, cep))
        
        if len(cep_limpo) != 8:
            return {'erro': 'CEP deve ter 8 dígitos'}
        
        url = f"https://viacep.com.br/ws/{cep_limpo}/json/"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            if 'erro' in data:
                return {'erro': 'CEP não encontrado'}
            
            return {
                'sucesso': True,
                'cep': data['cep'],
                'logradouro': data['logradouro'],
                'bairro': data['bairro'],
                'cidade': data['localidade'],
                'estado': data['uf'],
                'endereco_completo': f"{data['logradouro']}, {data['bairro']}, {data['localidade']} - {data['uf']}"
            }
        else:
            return {'erro': 'Erro ao consultar CEP'}
            
    except requests.exceptions.RequestException:
        return {'erro': 'Erro de conexão com ViaCEP'}
    except Exception as e:
        return {'erro': f'Erro inesperado: {str(e)}'}

def buscar_endereco(endereco):
    """Buscar coordenadas do endereço usando Nominatim"""
    try:
        url = "https://nominatim.openstreetmap.org/search"
        params = {
            'q': f"{endereco}, Brasil",
            'format': 'json',
            'limit': 5,
            'addressdetails': 1,
            'countrycodes': 'br'
        }
        headers = {
            'User-Agent': 'MeuBairroMelhor/1.0'
        }
        
        response = requests.get(url, params=params, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            if not data:
                return {'erro': 'Endereço não encontrado'}
            
            resultados = []
            for item in data:
                resultados.append({
                    'endereco': item['display_name'],
                    'latitude': float(item['lat']),
                    'longitude': float(item['lon']),
                    'tipo': item.get('type', ''),
                    'importancia': item.get('importance', 0)
                })
            
            return {
                'sucesso': True,
                'resultados': resultados
            }
        else:
            return {'erro': 'Erro ao consultar endereço'}
            
    except requests.exceptions.RequestException:
        return {'erro': 'Erro de conexão com Nominatim'}
    except Exception as e:
        return {'erro': f'Erro inesperado: {str(e)}'}

# ===== ROTAS PRINCIPAIS =====

@app.route('/')
def index():
    """Página principal - lista de propostas"""
    page = request.args.get('page', 1, type=int)
    category = request.args.get('category', 'all')
    status = request.args.get('status', 'all')
    search = request.args.get('search', '')
    
    # Construir query
    query = Proposal.query
    
    if category != 'all':
        query = query.filter(Proposal.category == category)
    
    if status != 'all':
        query = query.filter(Proposal.status == status)
    
    if search:
        query = query.filter(
            Proposal.title.contains(search) |
            Proposal.description.contains(search) |
            Proposal.address.contains(search)
        )
    
    proposals = query.order_by(Proposal.created_at.desc()).paginate(
        page=page, per_page=12, error_out=False
    )
    
    categories = Category.query.all()
    
    return render_template('index.html', 
                         proposals=proposals, 
                         categories=categories,
                         current_category=category,
                         current_status=status,
                         current_search=search)

@app.route('/mapa')
def mapa():
    """Página do mapa interativo"""
    proposals = Proposal.query.all()
    categories_raw = Category.query.all()
    
    # Converter categorias para dicionários antes de passar para o template
    categories = [{
        'id': cat.id,
        'name': cat.name,
        'icon': cat.icon,
        'color': cat.color
    } for cat in categories_raw]
    
    return render_template('mapa.html', proposals=proposals, categories=categories)

@app.route('/dashboard')
@login_required
def dashboard():
    """Dashboard com relatórios"""
    total_proposals = Proposal.query.count()
    
    # Converter lista de tuplas em dicionário com valores padrão
    proposals_by_status_raw = db.session.query(
        Proposal.status, 
        db.func.count(Proposal.id)
    ).group_by(Proposal.status).all()
    
    # Inicializar com valores padrão
    proposals_by_status = {
        'pending': 0,
        'approved': 0,
        'in_progress': 0,
        'completed': 0,
        'rejected': 0
    }
    
    # Atualizar com valores reais do banco
    for status, count in proposals_by_status_raw:
        proposals_by_status[status] = count
    
    # Categorias - converter para dicionário
    proposals_by_category_raw = db.session.query(
        Category.name,
        db.func.count(Proposal.id)
    ).join(Proposal).group_by(Category.name).all()
    proposals_by_category = dict(proposals_by_category_raw)
    
    recent_proposals = Proposal.query.order_by(
        Proposal.created_at.desc()
    ).limit(5).all()
    
    return render_template('dashboard.html',
                         total_proposals=total_proposals,
                         proposals_by_status=proposals_by_status,
                         proposals_by_category=proposals_by_category,
                         recent_proposals=recent_proposals)

@app.route('/proposta/<int:id>')
def proposta_detalhes(id):
    """Página de detalhes de uma proposta"""
    proposal = Proposal.query.get_or_404(id)
    comments = Comment.query.filter_by(proposal_id=id).order_by(Comment.created_at.desc()).all()
    
    # Verificar se o usuário já votou
    user_voted = False
    if current_user.is_authenticated:
        vote = Vote.query.filter_by(
            proposal_id=id, 
            user_id=current_user.id
        ).first()
        user_voted = vote is not None
    
    return render_template('proposta_detalhes.html',
                         proposal=proposal,
                         comments=comments,
                         user_voted=user_voted)

# ===== AUTENTICAÇÃO =====

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        
        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            login_user(user)
            return jsonify({'success': True, 'message': 'Login realizado com sucesso!'})
        else:
            return jsonify({'success': False, 'message': 'Email ou senha incorretos'})
    
    return render_template('auth/login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        
        if User.query.filter_by(email=email).first():
            return jsonify({'success': False, 'message': 'Email já cadastrado'})
        
        user = User(name=name, email=email)
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        login_user(user)
        return jsonify({'success': True, 'message': 'Cadastro realizado com sucesso!'})
    
    return render_template('auth/register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

# ===== PROPOSTAS =====

@app.route('/criar-proposta', methods=['GET', 'POST'])
@login_required
def criar_proposta():
    if request.method == 'POST':
        data = request.get_json()
        
        proposal = Proposal(
            title=data.get('title'),
            description=data.get('description'),
            category=data.get('category'),
            latitude=float(data.get('latitude')),
            longitude=float(data.get('longitude')),
            address=data.get('address'),
            priority=data.get('priority', 'medium'),
            author_id=current_user.id
        )
        
        db.session.add(proposal)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Proposta criada com sucesso!', 'id': proposal.id})
    
    categories = Category.query.all()
    return render_template('proposals/criar.html', categories=categories)

@app.route('/votar/<int:proposal_id>', methods=['POST'])
@login_required
def votar(proposal_id):
    try:
        proposal = Proposal.query.get_or_404(proposal_id)
        
        existing_vote = Vote.query.filter_by(
            proposal_id=proposal_id,
            user_id=current_user.id
        ).first()
        
        if existing_vote:
            db.session.delete(existing_vote)
            proposal.votes_count = max(0, proposal.votes_count - 1)
            voted = False
        else:
            vote = Vote(proposal_id=proposal_id, user_id=current_user.id)
            db.session.add(vote)
            proposal.votes_count += 1
            voted = True
        
        db.session.commit()
        return jsonify({'success': True, 'voted': voted, 'votes_count': proposal.votes_count})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'Erro ao votar: {str(e)}'}), 500

@app.route('/comentar/<int:proposal_id>', methods=['POST'])
@login_required
def comentar(proposal_id):
    try:
        data = request.get_json()
        content = data.get('content')
        
        if not content or not content.strip():
            return jsonify({'success': False, 'message': 'Comentário não pode estar vazio'})
        
        proposal = Proposal.query.get_or_404(proposal_id)
        
        comment = Comment(
            proposal_id=proposal_id,
            user_id=current_user.id,
            content=content.strip()
        )
        
        db.session.add(comment)
        proposal.comments_count += 1
        db.session.commit()
        
        return jsonify({
            'success': True, 
            'message': 'Comentário adicionado com sucesso!',
            'comment': {
                'id': comment.id,
                'content': comment.content,
                'author_name': comment.author_name,
                'created_at': comment.created_at.isoformat()
            }
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'Erro ao adicionar comentário: {str(e)}'}), 500

# ===== APIs =====

@app.route('/api/proposals')
def api_proposals():
    """API para buscar propostas"""
    page = request.args.get('page', 1, type=int)
    category = request.args.get('category', 'all')
    status = request.args.get('status', 'all')
    search = request.args.get('search', '')
    
    query = Proposal.query
    
    if category != 'all':
        query = query.filter(Proposal.category == category)
    
    if status != 'all':
        query = query.filter(Proposal.status == status)
    
    if search:
        query = query.filter(
            Proposal.title.contains(search) |
            Proposal.description.contains(search) |
            Proposal.address.contains(search)
        )
    
    proposals = query.order_by(Proposal.created_at.desc()).paginate(
        page=page, per_page=12, error_out=False
    )
    
    return jsonify({
        'proposals': [{
            'id': p.id,
            'title': p.title,
            'description': p.description,
            'category': p.category,
            'latitude': p.latitude,
            'longitude': p.longitude,
            'address': p.address,
            'status': p.status,
            'priority': p.priority,
            'votes_count': p.votes_count,
            'comments_count': p.comments_count,
            'author_name': p.author.name,
            'created_at': p.created_at.isoformat(),
            'updated_at': p.created_at.isoformat()
        } for p in proposals.items],
        'total': proposals.total,
        'pages': proposals.pages,
        'current_page': proposals.page,
        'has_next': proposals.has_next,
        'has_prev': proposals.has_prev
    })

@app.route('/api/categories')
def api_categories():
    """API para listar categorias"""
    categories = Category.query.all()
    return jsonify([{
        'id': c.id,
        'name': c.name,
        'icon': c.icon,
        'color': c.color
    } for c in categories])

# ===== INICIALIZAÇÃO =====

# ===== ENDPOINTS DE API PARA BUSCA =====

@app.route('/api/buscar-cep', methods=['POST'])
def api_buscar_cep():
    """API para buscar dados do CEP"""
    data = request.get_json()
    cep = data.get('cep', '').strip()
    
    if not cep:
        return jsonify({'erro': 'CEP é obrigatório'}), 400
    
    resultado = buscar_cep(cep)
    return jsonify(resultado)

@app.route('/api/buscar-endereco', methods=['POST'])
def api_buscar_endereco():
    """API para buscar coordenadas do endereço"""
    data = request.get_json()
    endereco = data.get('endereco', '').strip()
    
    if not endereco:
        return jsonify({'erro': 'Endereço é obrigatório'}), 400
    
    resultado = buscar_endereco(endereco)
    return jsonify(resultado)

@app.route('/api/buscar-propostas', methods=['GET'])
def api_buscar_propostas():
    """API para buscar propostas por localização"""
    latitude = request.args.get('lat', type=float)
    longitude = request.args.get('lng', type=float)
    raio = request.args.get('raio', 1.0, type=float)  # raio em km
    
    if not latitude or not longitude:
        return jsonify({'erro': 'Latitude e longitude são obrigatórios'}), 400
    
    # Buscar propostas próximas (simplificado - em produção usar PostGIS)
    propostas = Proposal.query.all()
    propostas_proximas = []
    
    for proposta in propostas:
        # Cálculo simples de distância (em produção usar fórmula de Haversine)
        distancia = ((proposta.latitude - latitude) ** 2 + (proposta.longitude - longitude) ** 2) ** 0.5
        if distancia <= raio:
            propostas_proximas.append(proposta.to_dict())
    
    return jsonify({
        'sucesso': True,
        'propostas': propostas_proximas,
        'total': len(propostas_proximas)
    })

def init_database():
    """Inicializar banco de dados com dados padrão"""
    with app.app_context():
        try:
            # Tentar criar todas as tabelas
            db.create_all()
            
            # Verificar se as categorias existem
            try:
                category_count = Category.query.count()
            except Exception:
                # Se houver erro, recriar as tabelas
                db.drop_all()
                db.create_all()
                category_count = 0
            
            # Criar categorias padrão se não existirem
            if category_count == 0:
                categories_data = [
                    {'id': 'iluminacao', 'name': 'Iluminação', 'icon': 'lightbulb', 'color': '#F59E0B'},
                    {'id': 'arborizacao', 'name': 'Arborização', 'icon': 'tree-pine', 'color': '#10B981'},
                    {'id': 'acessibilidade', 'name': 'Acessibilidade', 'icon': 'accessibility', 'color': '#8B5CF6'},
                    {'id': 'seguranca', 'name': 'Segurança', 'icon': 'shield', 'color': '#EF4444'},
                    {'id': 'transporte', 'name': 'Transporte', 'icon': 'bus', 'color': '#2563EB'},
                    {'id': 'lazer', 'name': 'Lazer', 'icon': 'playground', 'color': '#06B6D4'},
                    {'id': 'infraestrutura', 'name': 'Infraestrutura', 'icon': 'construction', 'color': '#64748B'},
                    {'id': 'outros', 'name': 'Outros', 'icon': 'more-horizontal', 'color': '#6B7280'}
                ]
                
                for cat_data in categories_data:
                    category = Category(**cat_data)
                    db.session.add(category)
                
                db.session.commit()
                print("✅ Categorias padrão criadas!")
        except Exception as e:
            print(f"❌ Erro ao inicializar banco: {e}")
            print("🔄 Tentando recriar banco...")
            db.drop_all()
            db.create_all()
            print("✅ Banco recriado com sucesso!")

if __name__ == '__main__':
    print("🚀 Iniciando Meu Bairro Melhor...")
    
    # Inicializar banco de dados
    init_database()
    
    # Configurações
    host = os.environ.get('FLASK_HOST', '127.0.0.1')
    port = int(os.environ.get('FLASK_PORT', 5000))
    debug = os.environ.get('FLASK_ENV', 'development') == 'development'
    
    print(f"🌐 Servidor rodando em: http://{host}:{port}")
    print(f"🔧 Modo debug: {'Ativado' if debug else 'Desativado'}")
    print("📊 Dashboard: http://{}:{}/dashboard".format(host, port))
    print("🗺️  Mapa: http://{}:{}/mapa".format(host, port))
    print("\nPressione Ctrl+C para parar")
    
    app.run(host=host, port=port, debug=debug)