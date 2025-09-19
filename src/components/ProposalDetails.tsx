import React, { useState } from 'react';
import { 
  ArrowLeft, 
  ThumbsUp, 
  MessageCircle, 
  MapPin, 
  Calendar, 
  User,
  Tag,
  AlertCircle,
  Send
} from 'lucide-react';
import { Proposal, Comment } from '../types';
import { categories } from '../data/categories';

interface ProposalDetailsProps {
  proposal: Proposal;
  onBack: () => void;
  onVote: (proposalId: string) => void;
  onComment: (proposalId: string, comment: string) => void;
  hasUserVoted?: boolean;
  comments: Comment[];
}

export const ProposalDetails: React.FC<ProposalDetailsProps> = ({
  proposal,
  onBack,
  onVote,
  onComment,
  hasUserVoted = false,
  comments
}) => {
  const [newComment, setNewComment] = useState('');
  const [showCommentForm, setShowCommentForm] = useState(false);

  const category = categories.find(cat => cat.id === proposal.category);

  const getStatusBadge = (status: string) => {
    const statusConfig = {
      pending: { color: 'bg-yellow-100 text-yellow-800 border-yellow-200', text: 'Pendente', icon: '⏳' },
      approved: { color: 'bg-blue-100 text-blue-800 border-blue-200', text: 'Aprovado', icon: '✅' },
      in_progress: { color: 'bg-purple-100 text-purple-800 border-purple-200', text: 'Em Andamento', icon: '🚧' },
      completed: { color: 'bg-green-100 text-green-800 border-green-200', text: 'Concluído', icon: '🎉' },
      rejected: { color: 'bg-red-100 text-red-800 border-red-200', text: 'Rejeitado', icon: '❌' }
    };

    const config = statusConfig[status as keyof typeof statusConfig];
    return (
      <span className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium border ${config.color}`}>
        <span className="mr-1">{config.icon}</span>
        {config.text}
      </span>
    );
  };

  const getPriorityBadge = (priority: string) => {
    const priorityConfig = {
      low: { color: 'bg-gray-100 text-gray-800', text: 'Baixa', icon: '⬇️' },
      medium: { color: 'bg-yellow-100 text-yellow-800', text: 'Média', icon: '➡️' },
      high: { color: 'bg-red-100 text-red-800', text: 'Alta', icon: '⬆️' }
    };

    const config = priorityConfig[priority as keyof typeof priorityConfig];
    return (
      <span className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium ${config.color}`}>
        <span className="mr-1">{config.icon}</span>
        {config.text}
      </span>
    );
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('pt-BR', {
      day: '2-digit',
      month: 'long',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const handleSubmitComment = (e: React.FormEvent) => {
    e.preventDefault();
    if (newComment.trim()) {
      onComment(proposal.id, newComment);
      setNewComment('');
      setShowCommentForm(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      {/* Header */}
      <div className="flex items-center space-x-4">
        <button
          onClick={onBack}
          className="p-2 text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded-md transition-colors"
        >
          <ArrowLeft className="w-5 h-5" />
        </button>
        <h1 className="text-2xl font-bold text-gray-900">Detalhes da Proposta</h1>
      </div>

      {/* Main Content */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden">
        {/* Proposal Header */}
        <div className="px-6 py-8 border-b border-gray-200">
          <div className="flex items-start justify-between mb-4">
            <div className="flex-1">
              <h2 className="text-2xl font-bold text-gray-900 mb-3">{proposal.title}</h2>
              <div className="flex items-center space-x-4 text-sm text-gray-500 mb-4">
                <div className="flex items-center space-x-1">
                  <User className="w-4 h-4" />
                  <span>Por {proposal.author_name}</span>
                </div>
                <div className="flex items-center space-x-1">
                  <Calendar className="w-4 h-4" />
                  <span>{formatDate(proposal.created_at)}</span>
                </div>
              </div>
            </div>
            <div className="flex flex-col items-end space-y-2">
              {getStatusBadge(proposal.status)}
              {getPriorityBadge(proposal.priority)}
            </div>
          </div>

          <div className="flex items-center space-x-4 mb-4">
            {category && (
              <div className="flex items-center space-x-2">
                <Tag className="w-4 h-4 text-gray-400" />
                <span
                  className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium"
                  style={{
                    backgroundColor: `${category.color}20`,
                    color: category.color
                  }}
                >
                  {category.name}
                </span>
              </div>
            )}
            <div className="flex items-center space-x-1 text-sm text-gray-500">
              <MapPin className="w-4 h-4" />
              <span>{proposal.address}</span>
            </div>
          </div>

          <p className="text-gray-700 leading-relaxed">{proposal.description}</p>
        </div>

        {/* Actions */}
        <div className="px-6 py-4 bg-gray-50 border-b border-gray-200">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-6">
              <button
                onClick={() => onVote(proposal.id)}
                className={`flex items-center space-x-2 px-4 py-2 rounded-md text-sm font-medium transition-all ${
                  hasUserVoted
                    ? 'bg-blue-100 text-blue-700 hover:bg-blue-200'
                    : 'text-gray-600 hover:text-blue-600 hover:bg-blue-50'
                }`}
              >
                <ThumbsUp className={`w-5 h-5 ${hasUserVoted ? 'fill-current' : ''}`} />
                <span>{proposal.votes_count} {proposal.votes_count === 1 ? 'voto' : 'votos'}</span>
              </button>
              
              <button
                onClick={() => setShowCommentForm(!showCommentForm)}
                className="flex items-center space-x-2 px-4 py-2 rounded-md text-sm font-medium text-gray-600 hover:text-blue-600 hover:bg-blue-50 transition-colors"
              >
                <MessageCircle className="w-5 h-5" />
                <span>{proposal.comments_count} {proposal.comments_count === 1 ? 'comentário' : 'comentários'}</span>
              </button>
            </div>
            
            {proposal.status === 'pending' && (
              <div className="flex items-center space-x-2 text-sm text-yellow-600">
                <AlertCircle className="w-4 h-4" />
                <span>Aguardando análise da prefeitura</span>
              </div>
            )}
          </div>
        </div>

        {/* Comment Form */}
        {showCommentForm && (
          <div className="px-6 py-4 bg-gray-50 border-b border-gray-200">
            <form onSubmit={handleSubmitComment} className="space-y-4">
              <textarea
                value={newComment}
                onChange={(e) => setNewComment(e.target.value)}
                placeholder="Compartilhe sua opinião sobre esta proposta..."
                rows={3}
                className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-1 focus:ring-blue-500 focus:border-blue-500"
              />
              <div className="flex items-center justify-end space-x-3">
                <button
                  type="button"
                  onClick={() => {
                    setShowCommentForm(false);
                    setNewComment('');
                  }}
                  className="px-4 py-2 text-sm font-medium text-gray-600 hover:text-gray-800 transition-colors"
                >
                  Cancelar
                </button>
                <button
                  type="submit"
                  disabled={!newComment.trim()}
                  className="px-4 py-2 bg-blue-600 text-white rounded-md text-sm font-medium hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed flex items-center space-x-2"
                >
                  <Send className="w-4 h-4" />
                  <span>Comentar</span>
                </button>
              </div>
            </form>
          </div>
        )}

        {/* Comments */}
        {comments.length > 0 && (
          <div className="px-6 py-6">
            <h3 className="text-lg font-medium text-gray-900 mb-4">
              Comentários ({comments.length})
            </h3>
            <div className="space-y-6">
              {comments.map((comment) => (
                <div key={comment.id} className="flex space-x-4">
                  <div className="flex-shrink-0">
                    <div className="w-10 h-10 bg-gray-200 rounded-full flex items-center justify-center">
                      <User className="w-5 h-5 text-gray-500" />
                    </div>
                  </div>
                  <div className="flex-1">
                    <div className="flex items-center space-x-2 mb-2">
                      <span className="font-medium text-gray-900">{comment.author_name}</span>
                      <span className="text-sm text-gray-500">
                        {formatDate(comment.created_at)}
                      </span>
                    </div>
                    <p className="text-gray-700 leading-relaxed">{comment.content}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {comments.length === 0 && (
          <div className="px-6 py-8 text-center">
            <MessageCircle className="w-12 h-12 text-gray-300 mx-auto mb-4" />
            <p className="text-gray-500">Ainda não há comentários nesta proposta.</p>
            <p className="text-sm text-gray-400">Seja o primeiro a compartilhar sua opinião!</p>
          </div>
        )}
      </div>
    </div>
  );
};