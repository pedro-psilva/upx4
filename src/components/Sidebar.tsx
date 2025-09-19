import React from 'react';
import { X, Home, Map, PlusCircle, BarChart, Settings, Filter } from 'lucide-react';
import { categories } from '../data/categories';

interface SidebarProps {
  isOpen: boolean;
  onClose: () => void;
  currentView: string;
  onViewChange: (view: string) => void;
  selectedCategory: string;
  onCategoryChange: (category: string) => void;
  statusFilter: string;
  onStatusChange: (status: string) => void;
}

export const Sidebar: React.FC<SidebarProps> = ({
  isOpen,
  onClose,
  currentView,
  onViewChange,
  selectedCategory,
  onCategoryChange,
  statusFilter,
  onStatusChange
}) => {
  const menuItems = [
    { id: 'home', label: 'Início', icon: Home },
    { id: 'map', label: 'Mapa', icon: Map },
    { id: 'create', label: 'Nova Proposta', icon: PlusCircle },
    { id: 'reports', label: 'Relatórios', icon: BarChart },
    { id: 'settings', label: 'Configurações', icon: Settings }
  ];

  const statusOptions = [
    { value: 'all', label: 'Todos os Status' },
    { value: 'pending', label: 'Pendente' },
    { value: 'approved', label: 'Aprovado' },
    { value: 'in_progress', label: 'Em Andamento' },
    { value: 'completed', label: 'Concluído' },
    { value: 'rejected', label: 'Rejeitado' }
  ];

  return (
    <>
      {/* Overlay */}
      {isOpen && (
        <div
          className="fixed inset-0 bg-black bg-opacity-50 z-40 lg:hidden"
          onClick={onClose}
        />
      )}

      {/* Sidebar */}
      <aside
        className={`fixed left-0 top-0 h-full w-80 bg-white border-r border-gray-200 z-50 transform transition-transform duration-300 ease-in-out ${
          isOpen ? 'translate-x-0' : '-translate-x-full'
        } lg:translate-x-0 overflow-y-auto shadow-xl`}
      >
        <div className="p-4 border-b border-gray-200 lg:hidden">
          <div className="flex items-center justify-between">
            <h2 className="text-lg font-semibold text-gray-900">Menu</h2>
            <button
              onClick={onClose}
              className="p-2 text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded-xl transition-all"
            >
              <X className="w-5 h-5" />
            </button>
          </div>
        </div>

        <div className="p-4">
          {/* Menu Principal */}
          <nav className="space-y-2 mb-8">
            {menuItems.map((item) => {
              const Icon = item.icon;
              return (
                <button
                  key={item.id}
                  onClick={() => {
                    onViewChange(item.id);
                    onClose();
                  }}
                  className={`w-full flex items-center space-x-3 px-3 py-3 rounded-xl text-sm font-medium transition-all transform hover:scale-[1.02] ${
                    currentView === item.id
                      ? 'bg-gradient-to-r from-blue-100 to-green-100 text-blue-700 shadow-sm'
                      : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
                  }`}
                >
                  <Icon className="w-5 h-5" />
                  <span>{item.label}</span>
                </button>
              );
            })}
          </nav>

          {/* Filtros */}
          <div className="border-t border-gray-200 pt-6">
            <div className="flex items-center space-x-2 mb-4">
              <div className="w-6 h-6 bg-gradient-to-br from-blue-500 to-green-500 rounded-lg flex items-center justify-center">
                <Filter className="w-3 h-3 text-white" />
              </div>
              <h3 className="text-sm font-medium text-gray-900">Filtros</h3>
            </div>

            {/* Categorias */}
            <div className="mb-6">
              <h4 className="text-xs font-medium text-gray-500 uppercase tracking-wider mb-3">
                Categorias
              </h4>
              <div className="space-y-1">
                <button
                  onClick={() => onCategoryChange('all')}
                  className={`w-full text-left px-3 py-2 rounded-lg text-sm transition-all ${
                    selectedCategory === 'all'
                      ? 'bg-gradient-to-r from-blue-50 to-green-50 text-gray-900 shadow-sm'
                      : 'text-gray-600 hover:bg-gray-50'
                  }`}
                >
                  Todas as categorias
                </button>
                {categories.map((category) => (
                  <button
                    key={category.id}
                    onClick={() => onCategoryChange(category.id)}
                    className={`w-full text-left px-3 py-2 rounded-lg text-sm flex items-center space-x-2 transition-all ${
                      selectedCategory === category.id
                        ? 'bg-gradient-to-r from-blue-50 to-green-50 text-gray-900 shadow-sm'
                        : 'text-gray-600 hover:bg-gray-50'
                    }`}
                  >
                    <div
                      className="w-3 h-3 rounded-full shadow-sm"
                      style={{ backgroundColor: category.color }}
                    />
                    <span>{category.name}</span>
                  </button>
                ))}
              </div>
            </div>

            {/* Status */}
            <div>
              <h4 className="text-xs font-medium text-gray-500 uppercase tracking-wider mb-3">
                Status
              </h4>
              <div className="space-y-1">
                {statusOptions.map((status) => (
                  <button
                    key={status.value}
                    onClick={() => onStatusChange(status.value)}
                    className={`w-full text-left px-3 py-2 rounded-lg text-sm transition-all ${
                      statusFilter === status.value
                        ? 'bg-gradient-to-r from-blue-50 to-green-50 text-gray-900 shadow-sm'
                        : 'text-gray-600 hover:bg-gray-50'
                    }`}
                  >
                    {status.label}
                  </button>
                ))}
              </div>
            </div>
          </div>
        </div>
      </aside>
    </>
  );
};