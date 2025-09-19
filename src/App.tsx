import React, { useState, useMemo, useEffect } from 'react';
import { Header } from './components/Header';
import { LoginForm } from './components/LoginForm';
import { RegisterForm } from './components/RegisterForm';
import { Sidebar } from './components/Sidebar';
import { ProposalCard } from './components/ProposalCard';
import { Map } from './components/Map';
import { CreateProposalForm } from './components/CreateProposalForm';
import { Dashboard } from './components/Dashboard';
import { ProposalDetails } from './components/ProposalDetails';
import { mockProposals } from './data/mockData';
import { Proposal, Comment } from './types';
import { Search, Grid, List } from 'lucide-react';

function App() {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [currentView, setCurrentView] = useState('home');
  const [authView, setAuthView] = useState<'login' | 'register' | null>(null);
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [statusFilter, setStatusFilter] = useState('all');
  const [searchTerm, setSearchTerm] = useState('');
  const [viewMode, setViewMode] = useState<'grid' | 'list'>('grid');
  const [proposals, setProposals] = useState<Proposal[]>(mockProposals);
  const [selectedProposal, setSelectedProposal] = useState<Proposal | null>(null);
  const [selectedProposalId, setSelectedProposalId] = useState<string | null>(null);
  const [votedProposals, setVotedProposals] = useState<Set<string>>(new Set());
  const [comments, setComments] = useState<Comment[]>([]);
  
  // Mock current user
  const [currentUser, setCurrentUser] = useState<{ name: string; avatar?: string } | null>(null);

  // Initialize comments with mock data
  useEffect(() => {
    const mockComments: Comment[] = [
      {
        id: '1',
        proposal_id: '1',
        user_id: 'user1',
        author_name: 'Ana Costa',
        content: 'Excelente proposta! Essa rua realmente precisa de mais iluminação para aumentar a segurança.',
        created_at: '2025-01-11T09:30:00Z'
      },
      {
        id: '2',
        proposal_id: '1',
        user_id: 'user2',
        author_name: 'Carlos Santos',
        content: 'Concordo completamente. Já presenciei alguns assaltos nesta região por conta da má iluminação.',
        created_at: '2025-01-11T14:15:00Z'
      }
    ];
    setComments(mockComments);
  }, []);

  // Filter proposals
  const filteredProposals = useMemo(() => {
    return proposals.filter(proposal => {
      const matchesCategory = selectedCategory === 'all' || proposal.category === selectedCategory;
      const matchesStatus = statusFilter === 'all' || proposal.status === statusFilter;
      const matchesSearch = searchTerm === '' || 
        proposal.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
        proposal.description.toLowerCase().includes(searchTerm.toLowerCase()) ||
        proposal.address.toLowerCase().includes(searchTerm.toLowerCase());
      
      return matchesCategory && matchesStatus && matchesSearch;
    });
  }, [proposals, selectedCategory, statusFilter, searchTerm]);

  // Handlers
  const handleLogin = (email: string, password: string) => {
    // Mock login - in real app, this would call an API
    setCurrentUser({ name: email.split('@')[0], avatar: '' });
    setAuthView(null);
  };

  const handleRegister = (name: string, email: string, password: string) => {
    // Mock register - in real app, this would call an API
    setCurrentUser({ name, avatar: '' });
    setAuthView(null);
  };

  const handleLogout = () => {
    setCurrentUser(null);
    setCurrentView('home');
  };

  const handleVote = (proposalId: string) => {
    if (!currentUser) {
      setAuthView('login');
      return;
    }

    setProposals(prev => prev.map(proposal => {
      if (proposal.id === proposalId) {
        const hasVoted = votedProposals.has(proposalId);
        const newVotesCount = hasVoted 
          ? Math.max(0, proposal.votes_count - 1)
          : proposal.votes_count + 1;
        
        // Update voted proposals set
        const newVotedProposals = new Set(votedProposals);
        if (hasVoted) {
          newVotedProposals.delete(proposalId);
        } else {
          newVotedProposals.add(proposalId);
        }
        setVotedProposals(newVotedProposals);
        
        return {
          ...proposal,
          votes_count: newVotesCount
        };
      }
      return proposal;
    }));
  };

  const handleComment = (proposalId: string, comment?: string) => {
    if (!currentUser) {
      setAuthView('login');
      return;
    }

    if (comment) {
      // Add new comment to state
      const newComment: Comment = {
        id: Date.now().toString(),
        proposal_id: proposalId,
        user_id: 'current_user',
        author_name: currentUser.name,
        content: comment,
        created_at: new Date().toISOString()
      };
      
      setComments(prev => [...prev, newComment]);
      
      // Update comments count
      setProposals(prev => prev.map(proposal => 
        proposal.id === proposalId 
          ? { ...proposal, comments_count: proposal.comments_count + 1 }
          : proposal
      ));
    } else {
      // Just open the comments section
      setSelectedProposalId(proposalId);
      setCurrentView('details');
    }
  };

  const handleViewDetails = (proposalId: string) => {
    const proposal = proposals.find(p => p.id === proposalId);
    if (proposal) {
      setSelectedProposal(proposal);
      setCurrentView('details');
    }
  };

  const handleCreateProposal = (proposalData: Omit<Proposal, 'id' | 'votes_count' | 'comments_count' | 'author_id' | 'author_name' | 'created_at' | 'updated_at'>) => {
    if (!currentUser) {
      setAuthView('login');
      return;
    }

    const newProposal: Proposal = {
      ...proposalData,
      id: Date.now().toString(),
      votes_count: 0,
      comments_count: 0,
      author_id: 'current_user',
      author_name: currentUser.name,
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString()
    };
    
    setProposals(prev => [newProposal, ...prev]);
    setCurrentView('home');
  };

  const handleProposalClick = (proposal: Proposal) => {
    setSelectedProposal(proposal);
  };

  const renderContent = () => {
    switch (currentView) {
      case 'map':
        return (
          <div className="space-y-6">
            <div className="flex items-center justify-between">
              <h1 className="text-2xl font-bold text-gray-900">Mapa das Propostas</h1>
              <div className="flex items-center space-x-4">
                <div className="relative">
                  <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
                  <input
                    type="text"
                    placeholder="Buscar propostas..."
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                    className="pl-9 pr-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-1 focus:ring-blue-500"
                  />
                </div>
              </div>
            </div>
            <Map 
              proposals={filteredProposals} 
              onProposalClick={handleProposalClick}
              selectedProposal={selectedProposal}
            />
            {selectedProposal && (
              <div className="mt-6">
                <ProposalCard
                  proposal={selectedProposal}
                  onVote={handleVote}
                  onComment={handleComment}
                  onViewDetails={handleViewDetails}
                  hasUserVoted={votedProposals.has(selectedProposal.id)}
                />
              </div>
            )}
          </div>
        );

      case 'create':
        if (!currentUser) {
          setAuthView('login');
          return null;
        }
        return (
          <div className="space-y-6">
            <h1 className="text-2xl font-bold text-gray-900">Nova Proposta</h1>
            <CreateProposalForm 
              onSubmit={handleCreateProposal}
              onCancel={() => setCurrentView('home')}
            />
          </div>
        );

      case 'reports':
        return <Dashboard proposals={proposals} />;

      case 'details':
        return selectedProposal ? (
          <ProposalDetails
            proposal={selectedProposal}
            onBack={() => {
              setCurrentView('home');
              setSelectedProposal(null);
            }}
            onVote={handleVote}
            onComment={handleComment}
            hasUserVoted={votedProposals.has(selectedProposal.id)}
            comments={comments.filter(c => c.proposal_id === selectedProposal.id)}
          />
        ) : null;

      case 'settings':
        return (
          <div className="space-y-6">
            <h1 className="text-2xl font-bold text-gray-900">Configurações</h1>
            
            {/* User Profile */}
            <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
              <h2 className="text-lg font-medium text-gray-900 mb-4">Perfil do Usuário</h2>
              {currentUser ? (
                <div className="space-y-4">
                  <div className="flex items-center space-x-4">
                    <div className="w-12 h-12 bg-gradient-to-br from-blue-500 to-green-500 rounded-full flex items-center justify-center shadow-md">
                      <span className="text-white text-lg font-medium">
                        {currentUser.name.charAt(0).toUpperCase()}
                      </span>
                    </div>
                    <div>
                      <p className="text-lg font-medium text-gray-900">{currentUser.name}</p>
                      <p className="text-sm text-gray-500">Membro da comunidade</p>
                    </div>
                  </div>
                  <button
                    onClick={handleLogout}
                    className="px-4 py-2 bg-red-600 text-white rounded-md text-sm font-medium hover:bg-red-700 transition-colors"
                  >
                    Sair da Conta
                  </button>
                </div>
              ) : (
                <div className="text-center py-8">
                  <p className="text-gray-600 mb-4">Faça login para acessar suas configurações</p>
                  <button
                    onClick={() => setAuthView('login')}
                    className="px-4 py-2 bg-blue-600 text-white rounded-md text-sm font-medium hover:bg-blue-700 transition-colors"
                  >
                    Fazer Login
                  </button>
                </div>
              )}
            </div>

            {/* App Settings */}
            <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
              <h2 className="text-lg font-medium text-gray-900 mb-4">Configurações da Aplicação</h2>
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="font-medium text-gray-900">Modo de Visualização Padrão</p>
                    <p className="text-sm text-gray-500">Escolha como visualizar as propostas por padrão</p>
                  </div>
                  <div className="flex items-center space-x-1 bg-gray-100 rounded-md p-1">
                    <button
                      onClick={() => setViewMode('grid')}
                      className={`p-2 rounded ${viewMode === 'grid' ? 'bg-white shadow-sm' : 'text-gray-600'}`}
                    >
                      <Grid className="w-4 h-4" />
                    </button>
                    <button
                      onClick={() => setViewMode('list')}
                      className={`p-2 rounded ${viewMode === 'list' ? 'bg-white shadow-sm' : 'text-gray-600'}`}
                    >
                      <List className="w-4 h-4" />
                    </button>
                  </div>
                </div>
                
                <div className="flex items-center justify-between">
                  <div>
                    <p className="font-medium text-gray-900">Filtros Padrão</p>
                    <p className="text-sm text-gray-500">Categoria e status selecionados por padrão</p>
                  </div>
                  <div className="flex items-center space-x-2">
                    <span className="text-sm text-gray-500">
                      {selectedCategory === 'all' ? 'Todas as categorias' : 
                       categories.find(c => c.id === selectedCategory)?.name || 'Todas as categorias'}
                    </span>
                    <span className="text-gray-300">•</span>
                    <span className="text-sm text-gray-500">
                      {statusFilter === 'all' ? 'Todos os status' : 
                       statusFilter === 'pending' ? 'Pendente' :
                       statusFilter === 'approved' ? 'Aprovado' :
                       statusFilter === 'in_progress' ? 'Em Andamento' :
                       statusFilter === 'completed' ? 'Concluído' :
                       statusFilter === 'rejected' ? 'Rejeitado' : 'Todos os status'}
                    </span>
                  </div>
                </div>
              </div>
            </div>

            {/* About */}
            <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
              <h2 className="text-lg font-medium text-gray-900 mb-4">Sobre o Aplicativo</h2>
              <div className="space-y-2 text-sm text-gray-600">
                <p><strong>Versão:</strong> 1.0.0</p>
                <p><strong>Desenvolvido para:</strong> Participação cidadã em melhorias urbanas</p>
                <p><strong>Funcionalidades:</strong> Criação, votação e comentários em propostas</p>
              </div>
            </div>
          </div>
        );

      default:
        return (
          <div className="space-y-6">
            {/* Header */}
            <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
              <div>
                <h1 className="text-2xl font-bold text-gray-900">Propostas da Comunidade</h1>
                <p className="text-gray-600">
                  {filteredProposals.length} {filteredProposals.length === 1 ? 'proposta encontrada' : 'propostas encontradas'}
                </p>
              </div>
              
              <div className="flex items-center space-x-4">
                <div className="relative">
                  <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
                  <input
                    type="text"
                    placeholder="Buscar propostas..."
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                    className="pl-9 pr-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-1 focus:ring-blue-500"
                  />
                </div>
                
                <div className="flex items-center space-x-1 bg-gray-100 rounded-md p-1">
                  <button
                    onClick={() => setViewMode('grid')}
                    className={`p-2 rounded ${viewMode === 'grid' ? 'bg-white shadow-sm' : 'text-gray-600'}`}
                  >
                    <Grid className="w-4 h-4" />
                  </button>
                  <button
                    onClick={() => setViewMode('list')}
                    className={`p-2 rounded ${viewMode === 'list' ? 'bg-white shadow-sm' : 'text-gray-600'}`}
                  >
                    <List className="w-4 h-4" />
                  </button>
                </div>
              </div>
            </div>

            {/* Proposals Grid/List */}
            {filteredProposals.length > 0 ? (
              <div className={`${
                viewMode === 'grid' 
                  ? 'grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6' 
                  : 'space-y-4'
              }`}>
                {filteredProposals.map((proposal) => (
                  <ProposalCard
                    key={proposal.id}
                    proposal={proposal}
                    onVote={handleVote}
                    onComment={handleComment}
                    onViewDetails={handleViewDetails}
                    hasUserVoted={votedProposals.has(proposal.id)}
                  />
                ))}
              </div>
            ) : (
              <div className="text-center py-12">
                <div className="text-gray-400 mb-4">
                  <Search className="w-16 h-16 mx-auto" />
                </div>
                <h3 className="text-lg font-medium text-gray-900 mb-2">Nenhuma proposta encontrada</h3>
                <p className="text-gray-600">Tente ajustar os filtros ou criar uma nova proposta.</p>
                <button
                  onClick={() => setCurrentView('create')}
                  className="mt-4 px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors"
                >
                  Criar Nova Proposta
                </button>
              </div>
            )}
          </div>
        );
    }
  };

  // Show auth forms if needed
  if (authView === 'login') {
    return (
      <LoginForm
        onLogin={handleLogin}
        onSwitchToRegister={() => setAuthView('register')}
        onClose={() => setAuthView(null)}
      />
    );
  }

  if (authView === 'register') {
    return (
      <RegisterForm
        onRegister={handleRegister}
        onSwitchToLogin={() => setAuthView('login')}
        onClose={() => setAuthView(null)}
      />
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 via-white to-blue-50">
      <Header 
        onToggleSidebar={() => setSidebarOpen(!sidebarOpen)}
        currentUser={currentUser}
        onLogin={() => setAuthView('login')}
        onLogout={handleLogout}
      />
      
      <div className="flex">
        <Sidebar
          isOpen={sidebarOpen}
          onClose={() => setSidebarOpen(false)}
          currentView={currentView}
          onViewChange={setCurrentView}
          selectedCategory={selectedCategory}
          onCategoryChange={(category) => {
            setSelectedCategory(category);
            // Return to home when changing category (except when in map view)
            if (currentView !== 'map' && currentView !== 'home') {
              setCurrentView('home');
            }
          }}
          statusFilter={statusFilter}
          onStatusChange={(status) => {
            setStatusFilter(status);
            // Return to home when changing status (except when in map view)
            if (currentView !== 'map' && currentView !== 'home') {
              setCurrentView('home');
            }
          }}
        />
        
        <main className="flex-1 p-6 min-h-screen lg:ml-80">
          {renderContent()}
        </main>
      </div>
    </div>
  );
}

export default App;