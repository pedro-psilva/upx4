#!/usr/bin/env python3
"""
Meu Bairro Melhor - Aplicação Principal
Foco na lógica e funcionalidades
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os
import requests
from sqlalchemy import func, case
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from io import BytesIO

# Criar aplicação Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'sua-chave-secreta-aqui-mude-em-producao'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or 'sqlite:///meu_bairro_melhor.db'
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
    
    # Campos adicionais para perfil completo
    nome_completo = db.Column(db.String(200))
    cpf = db.Column(db.String(14))
    telefone = db.Column(db.String(20))
    endereco = db.Column(db.Text)
    cep = db.Column(db.String(10))
    data_nascimento = db.Column(db.Date)
    
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
    
    # Relacionamentos - usar lazy='joined' para garantir que usuários sejam carregados
    user = db.relationship('User', backref='comments', lazy='joined')
    proposal = db.relationship('Proposal', backref='comments')
    
    @property
    def author_name(self):
        try:
            if self.user:
                return self.user.name if self.user.name else 'Usuário Anônimo'
            return 'Usuário Anônimo'
        except Exception:
            return 'Usuário Anônimo'

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
    
    # Buscar todos os comentários da proposta
    comments = Comment.query.filter_by(proposal_id=id).order_by(Comment.created_at.desc()).all()
    
    # Sincronizar contador de comentários com a contagem real
    real_comments_count = Comment.query.filter_by(proposal_id=id).count()
    if proposal.comments_count != real_comments_count:
        proposal.comments_count = real_comments_count
        db.session.commit()
    
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

@app.route('/perfil', methods=['GET', 'POST'])
@login_required
def perfil():
    if request.method == 'POST':
        # Atualizar dados do usuário
        current_user.nome_completo = request.form.get('nome_completo')
        current_user.cpf = request.form.get('cpf')
        current_user.telefone = request.form.get('telefone')
        current_user.endereco = request.form.get('endereco')
        current_user.cep = request.form.get('cep')
        
        # Processar data de nascimento
        data_nascimento = request.form.get('data_nascimento')
        if data_nascimento:
            current_user.data_nascimento = datetime.strptime(data_nascimento, '%Y-%m-%d').date()
        
        db.session.commit()
        flash('Perfil atualizado com sucesso!', 'success')
        return redirect(url_for('perfil'))
    
    return render_template('perfil.html')

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
        db.session.flush()  # Garante que o comentário tenha ID antes de contar
        
        # Recalcular contador de comentários baseado na contagem real
        proposal.comments_count = Comment.query.filter_by(proposal_id=proposal_id).count()
        
        db.session.commit()
        
        return jsonify({
            'success': True, 
            'message': 'Comentário adicionado com sucesso!',
            'comment': {
                'id': comment.id,
                'content': comment.content,
                'author_name': comment.author_name,
                'created_at': comment.created_at.isoformat()
            },
            'comments_count': proposal.comments_count
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
            'latitude': float(p.latitude),
            'longitude': float(p.longitude),
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

@app.route('/api/map-proposals')
def api_map_proposals():
    """API específica para o mapa - retorna todas as propostas"""
    proposals = Proposal.query.all()
    return jsonify({
        'proposals': [{
            'id': p.id,
            'title': p.title,
            'description': p.description,
            'category': p.category,
            'latitude': float(p.latitude),
            'longitude': float(p.longitude),
            'address': p.address,
            'status': p.status,
            'priority': p.priority,
            'votes_count': p.votes_count,
            'comments_count': p.comments_count,
            'author_name': p.author.name if p.author else 'Anônimo',
            'created_at': p.created_at.isoformat(),
            'updated_at': p.updated_at.isoformat()
        } for p in proposals],
        'total': len(proposals)
    })

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
        except Exception as e:
            db.drop_all()
            db.create_all()

# ===== RELATÓRIOS =====

def obter_dados_relatorio():
    """Coleta todos os dados necessários para o relatório"""
    
    # Estatísticas gerais
    total_propostas = Proposal.query.count()
    total_usuarios = User.query.count()
    total_comentarios = Comment.query.count()
    total_votos = Vote.query.count()
    
    # Propostas por status
    propostas_aprovadas = Proposal.query.filter_by(status='approved').count()
    propostas_pendentes = Proposal.query.filter_by(status='pending').count()
    propostas_em_andamento = Proposal.query.filter_by(status='in_progress').count()
    
    taxa_aprovacao = round((propostas_aprovadas / total_propostas * 100), 1) if total_propostas > 0 else 0
    
    # Propostas por categoria
    propostas_por_categoria = db.session.query(
        Category.name,
        func.count(Proposal.id).label('total'),
        func.sum(case((Proposal.status == 'approved', 1), else_=0)).label('aprovadas'),
        func.sum(case((Proposal.status == 'pending', 1), else_=0)).label('pendentes'),
        func.sum(case((Proposal.status == 'in_progress', 1), else_=0)).label('em_andamento')
    ).join(Proposal, Category.id == Proposal.category)\
     .group_by(Category.id, Category.name).all()
    
    # Propostas recentes (últimas 10)
    propostas_recentes = Proposal.query.order_by(Proposal.created_at.desc()).limit(10).all()
    
    # Comentários em destaque (mais recentes)
    comentarios_destaque = Comment.query.join(User).order_by(
        Comment.created_at.desc()
    ).limit(5).all()
    
    # Usuários mais ativos
    usuarios_ativos = db.session.query(
        User,
        func.count(Proposal.id).label('total_propostas'),
        func.count(Comment.id).label('total_comentarios')
    ).outerjoin(Proposal, User.id == Proposal.author_id)\
     .outerjoin(Comment, User.id == Comment.user_id)\
     .group_by(User.id)\
     .order_by(func.count(Proposal.id).desc())\
     .limit(10).all()
    
    # Propostas mais votadas
    propostas_mais_votadas = Proposal.query.order_by(Proposal.votes_count.desc()).limit(5).all()
    
    # Dados para o cabeçalho
    data_atual = datetime.now().strftime("%d/%m/%Y")
    mes_atual = datetime.now().strftime("%B %Y")
    
    return {
        'data_atual': data_atual,
        'periodo': mes_atual,
        'total_registros': total_propostas + total_comentarios,
        'responsavel': 'Sistema Administrativo',
        'total_propostas': total_propostas,
        'total_usuarios': total_usuarios,
        'total_comentarios': total_comentarios,
        'total_votos': total_votos,
        'propostas_aprovadas': propostas_aprovadas,
        'propostas_pendentes': propostas_pendentes,
        'propostas_em_andamento': propostas_em_andamento,
        'taxa_aprovacao': f"{taxa_aprovacao}%",
        'propostas_por_categoria': propostas_por_categoria,
        'propostas_recentes': propostas_recentes,
        'comentarios_destaque': comentarios_destaque,
        'usuarios_ativos': usuarios_ativos,
        'propostas_mais_votadas': propostas_mais_votadas
    }

@app.route('/relatorios')
@login_required
def relatorios():
    """Página principal de relatórios"""
    dados = obter_dados_relatorio()
    return render_template('relatorios.html', **dados)

@app.route('/relatorios/pdf')
@login_required
def relatorio_pdf():
    """Gerar relatório em PDF usando ReportLab"""
    dados = obter_dados_relatorio()
    
    # Criar buffer para o PDF
    buffer = BytesIO()
    
    # Criar documento PDF
    doc = SimpleDocTemplate(buffer, pagesize=A4, 
                          rightMargin=72, leftMargin=72, 
                          topMargin=72, bottomMargin=18)
    
    # Estilos
    styles = getSampleStyleSheet()
    
    # Estilo personalizado para título
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        spaceAfter=30,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#1f2937')
    )
    
    # Estilo para subtítulos
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Heading2'],
        fontSize=14,
        spaceAfter=12,
        textColor=colors.HexColor('#374151')
    )
    
    # Estilo para parágrafos
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=10,
        spaceAfter=6
    )
    
    # Lista de elementos do PDF
    story = []
    
    # Cabeçalho
    story.append(Paragraph("Relatório de Engajamento Comunitário", title_style))
    story.append(Paragraph("Meu Bairro Melhor - Sistema de Participação Cidadã", styles['Normal']))
    story.append(Paragraph(f"Gerado em: {dados['data_atual']} | Responsável: {dados['responsavel']}", styles['Normal']))
    story.append(Spacer(1, 20))
    
    # Estatísticas Gerais
    story.append(Paragraph("📊 Estatísticas Gerais", subtitle_style))
    
    # Tabela de estatísticas
    stats_data = [
        ['Métrica', 'Valor'],
        ['Total de Propostas', str(dados['total_propostas'])],
        ['Total de Usuários', str(dados['total_usuarios'])],
        ['Total de Comentários', str(dados['total_comentarios'])],
        ['Total de Votos', str(dados['total_votos'])]
    ]
    
    stats_table = Table(stats_data, colWidths=[3*inch, 2*inch])
    stats_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f8fafc')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#374151')),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    story.append(stats_table)
    story.append(Spacer(1, 20))
    
    # Status das Propostas
    story.append(Paragraph("📈 Status das Propostas", subtitle_style))
    
    status_data = [
        ['Status', 'Quantidade', 'Percentual'],
        ['Aprovadas', str(dados['propostas_aprovadas']), dados['taxa_aprovacao']],
        ['Pendentes', str(dados['propostas_pendentes']), f"{round((dados['propostas_pendentes'] / dados['total_propostas'] * 100) if dados['total_propostas'] > 0 else 0, 1)}%"],
        ['Em Andamento', str(dados['propostas_em_andamento']), f"{round((dados['propostas_em_andamento'] / dados['total_propostas'] * 100) if dados['total_propostas'] > 0 else 0, 1)}%"]
    ]
    
    status_table = Table(status_data, colWidths=[2*inch, 1.5*inch, 1.5*inch])
    status_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f8fafc')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#374151')),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    story.append(status_table)
    story.append(Spacer(1, 20))
    
    # Propostas por Categoria
    story.append(Paragraph("🏷️ Propostas por Categoria", subtitle_style))
    
    categoria_data = [['Categoria', 'Total', 'Aprovadas', 'Pendentes', 'Em Andamento']]
    for categoria in dados['propostas_por_categoria']:
        categoria_data.append([
            categoria.name,
            str(categoria.total),
            str(categoria.aprovadas),
            str(categoria.pendentes),
            str(categoria.em_andamento)
        ])
    
    categoria_table = Table(categoria_data, colWidths=[1.5*inch, 0.8*inch, 0.8*inch, 0.8*inch, 0.8*inch])
    categoria_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f8fafc')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#374151')),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE', (0, 1), (-1, -1), 9)
    ]))
    
    story.append(categoria_table)
    story.append(PageBreak())
    
    # Propostas Recentes
    story.append(Paragraph("🆕 Propostas Recentes", subtitle_style))
    
    recentes_data = [['Título', 'Autor', 'Data', 'Status', 'Votos']]
    for proposta in dados['propostas_recentes']:
        recentes_data.append([
            proposta.title[:30] + '...' if len(proposta.title) > 30 else proposta.title,
            (proposta.author.nome_completo or proposta.author.name)[:20],
            proposta.created_at.strftime('%d/%m/%Y'),
            proposta.status.title(),
            str(proposta.votes_count)
        ])
    
    recentes_table = Table(recentes_data, colWidths=[2*inch, 1.2*inch, 0.8*inch, 0.8*inch, 0.5*inch])
    recentes_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f8fafc')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#374151')),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE', (0, 1), (-1, -1), 8)
    ]))
    
    story.append(recentes_table)
    story.append(Spacer(1, 20))
    
    # Propostas Mais Votadas
    story.append(Paragraph("⭐ Propostas Mais Votadas", subtitle_style))
    
    votadas_data = [['Posição', 'Título', 'Votos', 'Comentários', 'Status']]
    for i, proposta in enumerate(dados['propostas_mais_votadas'], 1):
        votadas_data.append([
            f"{i}º",
            proposta.title[:25] + '...' if len(proposta.title) > 25 else proposta.title,
            str(proposta.votes_count),
            str(proposta.comments_count),
            proposta.status.title()
        ])
    
    votadas_table = Table(votadas_data, colWidths=[0.5*inch, 2*inch, 0.6*inch, 0.8*inch, 0.8*inch])
    votadas_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f8fafc')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#374151')),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE', (0, 1), (-1, -1), 8)
    ]))
    
    story.append(votadas_table)
    story.append(Spacer(1, 20))
    
    # Usuários Mais Ativos
    story.append(Paragraph("🏆 Usuários Mais Ativos", subtitle_style))
    
    usuarios_data = [['Posição', 'Nome', 'Email', 'Propostas', 'Comentários']]
    for i, usuario_data in enumerate(dados['usuarios_ativos'], 1):
        usuario = usuario_data[0]
        total_propostas = usuario_data[1]
        total_comentarios = usuario_data[2]
        usuarios_data.append([
            f"{i}º",
            (usuario.nome_completo or usuario.name)[:20],
            usuario.email[:25] + '...' if len(usuario.email) > 25 else usuario.email,
            str(total_propostas),
            str(total_comentarios)
        ])
    
    usuarios_table = Table(usuarios_data, colWidths=[0.5*inch, 1.5*inch, 1.8*inch, 0.8*inch, 0.8*inch])
    usuarios_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f8fafc')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#374151')),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE', (0, 1), (-1, -1), 8)
    ]))
    
    story.append(usuarios_table)
    
    # Rodapé
    story.append(Spacer(1, 30))
    story.append(Paragraph("Meu Bairro Melhor - Sistema de Participação Cidadã", styles['Normal']))
    story.append(Paragraph(f"Relatório gerado automaticamente em {dados['data_atual']}", styles['Normal']))
    story.append(Paragraph("Para mais informações, acesse o sistema ou entre em contato com a administração", styles['Normal']))
    
    # Construir PDF
    doc.build(story)
    
    # Obter conteúdo do buffer
    pdf_content = buffer.getvalue()
    buffer.close()
    
    # Preparar resposta
    response = make_response(pdf_content)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'attachment; filename="relatorio_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf"'
    
    return response

@app.route('/relatorios/personalizado', methods=['GET', 'POST'])
@login_required
def relatorio_personalizado():
    """Relatório com filtros personalizados"""
    if request.method == 'POST':
        # Obter filtros do formulário
        data_inicio = request.form.get('data_inicio')
        data_fim = request.form.get('data_fim')
        categoria = request.form.get('categoria')
        status = request.form.get('status')
        
        # Aplicar filtros na consulta
        query = Proposal.query
        
        if data_inicio:
            query = query.filter(Proposal.created_at >= data_inicio)
        if data_fim:
            query = query.filter(Proposal.created_at <= data_fim)
        if categoria:
            query = query.filter(Proposal.category == categoria)
        if status:
            query = query.filter(Proposal.status == status)
        
        propostas_filtradas = query.all()
        
        # Se solicitado PDF
        if request.form.get('formato') == 'pdf':
            dados = obter_dados_relatorio()
            dados['propostas_recentes'] = propostas_filtradas
            dados['titulo_personalizado'] = f"Relatório Personalizado - {data_inicio} a {data_fim}"
            
            # Usar a mesma lógica do relatório PDF principal
            return relatorio_pdf()
    
    # Buscar categorias para o formulário
    categorias = Category.query.all()
    return render_template('relatorio_personalizado.html', categorias=categorias)

# Filtro personalizado para formatar datas no template
@app.template_filter('strftime')
def strftime_filter(date, format='%d/%m/%Y'):
    """Filtro para formatar datas"""
    if date:
        return date.strftime(format)
    return ''

if __name__ == '__main__':
    # Inicializar banco de dados
    init_database()
    
    # Configurações
    host = os.environ.get('FLASK_HOST', '127.0.0.1')
    port = int(os.environ.get('FLASK_PORT', 5000))
    debug = os.environ.get('FLASK_ENV', 'development') == 'development'
    
    app.run(host=host, port=port, debug=debug)