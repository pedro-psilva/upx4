import React from 'react';
import { 
  ThumbsUp, 
  MessageCircle, 
  MapPin, 
  Clock, 
  User,
  Lightbulb,
  TreePine,
  Users,
  Shield,
  Bus,
  Construction,
  MoreHorizontal
} from 'lucide-react';
import { Proposal } from '../types';
import { categories } from '../data/categories';

interface ProposalCardProps {
  proposal: Proposal;
  onVote: (proposalId: string) => void;
  onComment: (proposalId: string) => void;
  onViewDetails: (proposalId: string) => void;
  hasUserVoted?: boolean;
}

const iconMap = {
  'lightbulb': Lightbulb,
  'tree-pine': TreePine,
  'accessibility': Users,
  'shield': Shield,
  'bus': Bus,
  'playground': Users,
  'construction': Construction,
  'more-horizontal': MoreHorizontal
};

export const ProposalCard: React.FC<ProposalCardProps> = ({
  proposal,
  onVote,
  onComment,
  onViewDetails,
  hasUserVoted = false
}) => {
  const category = categories.find(cat => cat.id === proposal.category);
  const CategoryIcon = category ? iconMap[category.icon as keyof typeof iconMap] : MoreHorizontal;

  const getStatusBadge = (status: string) => {
    const statusConfig = {
      pending: { color: 'bg-yellow-100 text-yellow-800', text: 'Pendente' },
      approved: { color: 'bg-blue-100 text-blue-800', text: 'Aprovado' },
      in_progress: { color: 'bg-purple-100 text-purple-800', text: 'Em Andamento' },
      completed: { color: 'bg-green-100 text-green-800', text: 'Concluído' },
      rejected: { color: 'bg-red-100 text-red-800', text: 'Rejeitado' }
    };

    const config = statusConfig[status as keyof typeof statusConfig];
    return (
      <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${config.color}`}>
        {config.text}
      </span>
    );
  };

  const getPriorityBadge = (priority: string) => {
    const priorityConfig = {
      low: { color: 'bg-gray-100 text-gray-800', text: 'Baixa' },
      medium: { color: 'bg-yellow-100 text-yellow-800', text: 'Média' },
      high: { color: 'bg-red-100 text-red-800', text: 'Alta' }
    };

    const config = priorityConfig[priority as keyof typeof priorityConfig];
    return (
      <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${config.color}`}>
        {config.text}
      </span>
    );
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('pt-BR', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric'
    });
  };

  return (
    <div className="bg-white rounded-2xl shadow-sm border border-gray-200 hover:shadow-xl hover:border-gray-300 transition-all duration-300 fade-in transform hover:scale-[1.02]">
      <div className="p-6">
        {/* Header */}
        <div className="flex items-start justify-between mb-4">
          <div className="flex items-start space-x-3">
            <div
              className="w-10 h-10 rounded-xl flex items-center justify-center shadow-md"
              style={{ backgroundColor: `${category?.color}20` }}
            >
              {CategoryIcon && (
                <CategoryIcon
                  className="w-5 h-5"
                  style={{ color: category?.color }}
                />
              )}
            </div>
            <div className="flex-1 min-w-0">
              <h3 className="text-lg font-medium text-gray-900 mb-1 line-clamp-2">
                {proposal.title}
              </h3>
              <div className="flex items-center space-x-2 text-sm text-gray-500">
                <User className="w-4 h-4" />
                <span>{proposal.author_name}</span>
                <span>•</span>
                <Clock className="w-4 h-4" />
                <span>{formatDate(proposal.created_at)}</span>
              </div>
            </div>
          </div>
          <div className="flex flex-col items-end space-y-2">
            {getStatusBadge(proposal.status)}
            {getPriorityBadge(proposal.priority)}
          </div>
        </div>

        {/* Description */}
        <p className="text-gray-600 mb-4 line-clamp-3">
          {proposal.description}
        </p>

        {/* Location */}
        <div className="flex items-center text-sm text-gray-500 mb-4">
          <MapPin className="w-4 h-4 mr-1" />
          <span>{proposal.address}</span>
        </div>

        {/* Category */}
        {category && (
          <div className="mb-4">
            <span
              className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium shadow-sm"
              style={{
                backgroundColor: `${category.color}20`,
                color: category.color
              }}
            >
              {category.name}
            </span>
          </div>
        )}

        {/* Actions */}
        <div className="flex items-center justify-between pt-4 border-t border-gray-100">
          <div className="flex items-center space-x-4">
            <button
              onClick={() => onVote(proposal.id)}
              className={`flex items-center space-x-2 px-4 py-2 rounded-xl text-sm font-medium transition-all transform hover:scale-105 ${
                hasUserVoted
                  ? 'bg-gradient-to-r from-blue-100 to-blue-200 text-blue-700 hover:from-blue-200 hover:to-blue-300 shadow-md'
                  : 'text-gray-600 hover:text-blue-600 hover:bg-blue-50 border border-gray-200 hover:border-blue-200'
              }`}
            >
              <ThumbsUp className={`w-4 h-4 ${hasUserVoted ? 'fill-current' : ''}`} />
              <span>{proposal.votes_count}</span>
            </button>
            <button
              onClick={() => onComment(proposal.id)}
              className="flex items-center space-x-2 px-4 py-2 rounded-xl text-sm font-medium text-gray-600 hover:text-blue-600 hover:bg-blue-50 border border-gray-200 hover:border-blue-200 transition-all transform hover:scale-105"
            >
              <MessageCircle className="w-4 h-4" />
              <span>{proposal.comments_count}</span>
            </button>
          </div>
          <button
            onClick={() => onViewDetails(proposal.id)}
            className="px-6 py-2 bg-gradient-to-r from-blue-600 to-green-600 text-white rounded-xl text-sm font-medium hover:from-blue-700 hover:to-green-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-all transform hover:scale-105 shadow-md"
          >
            Ver Detalhes
          </button>
        </div>
      </div>
    </div>
  );
};