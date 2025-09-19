import { Category } from '../types';

export const categories: Category[] = [
  {
    id: 'iluminacao',
    name: 'Iluminação',
    icon: 'lightbulb',
    color: '#F59E0B',
    description: 'Melhoria da iluminação pública'
  },
  {
    id: 'arborizacao',
    name: 'Arborização',
    icon: 'tree-pine',
    color: '#10B981',
    description: 'Plantio de árvores e áreas verdes'
  },
  {
    id: 'acessibilidade',
    name: 'Acessibilidade',
    icon: 'accessibility',
    color: '#8B5CF6',
    description: 'Melhorias para pessoas com deficiência'
  },
  {
    id: 'seguranca',
    name: 'Segurança',
    icon: 'shield',
    color: '#EF4444',
    description: 'Segurança pública e equipamentos'
  },
  {
    id: 'transporte',
    name: 'Transporte',
    icon: 'bus',
    color: '#2563EB',
    description: 'Transporte público e mobilidade'
  },
  {
    id: 'lazer',
    name: 'Lazer',
    icon: 'playground',
    color: '#06B6D4',
    description: 'Espaços de lazer e recreação'
  },
  {
    id: 'infraestrutura',
    name: 'Infraestrutura',
    icon: 'construction',
    color: '#64748B',
    description: 'Pavimentação, saneamento e obras'
  },
  {
    id: 'outros',
    name: 'Outros',
    icon: 'more-horizontal',
    color: '#6B7280',
    description: 'Outras melhorias urbanas'
  }
];