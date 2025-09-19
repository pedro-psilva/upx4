import React from 'react';
import { MapPin, Menu, User, Bell, LogOut } from 'lucide-react';

interface HeaderProps {
  onToggleSidebar: () => void;
  currentUser?: { name: string; avatar?: string } | null;
  onLogin: () => void;
  onLogout: () => void;
}

export const Header: React.FC<HeaderProps> = ({ 
  onToggleSidebar, 
  currentUser, 
  onLogin, 
  onLogout 
}) => {
  return (
    <header className="bg-white/95 backdrop-blur-sm shadow-sm border-b border-gray-200 sticky top-0 z-40">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo e Menu */}
          <div className="flex items-center space-x-4">
            <button
              onClick={onToggleSidebar}
              className="lg:hidden p-2 rounded-xl text-gray-600 hover:text-gray-900 hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-all"
            >
              <Menu className="w-6 h-6" />
            </button>
            <div className="flex items-center space-x-2">
              <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-green-500 rounded-xl flex items-center justify-center shadow-lg">
                <MapPin className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="text-xl font-bold bg-gradient-to-r from-blue-600 to-green-600 bg-clip-text text-transparent">
                  Meu Bairro Melhor
                </h1>
                <p className="text-xs text-gray-500 hidden sm:block">Urbanismo Colaborativo</p>
              </div>
            </div>
          </div>

          {/* Ações do usuário */}
          <div className="flex items-center space-x-4">
            {currentUser && (
              <button className="p-2 text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded-xl relative transition-all">
                <Bell className="w-6 h-6" />
                <span className="absolute -top-1 -right-1 w-3 h-3 bg-red-500 rounded-full animate-pulse"></span>
              </button>
            )}
            
            {currentUser ? (
              <div className="flex items-center space-x-3">
                <div className="flex items-center space-x-2 cursor-pointer hover:bg-gray-50 rounded-xl p-2 transition-all">
                  <div className="w-8 h-8 bg-gradient-to-br from-blue-500 to-green-500 rounded-full flex items-center justify-center shadow-md">
                    <span className="text-white text-sm font-medium">
                      {currentUser.name.charAt(0).toUpperCase()}
                    </span>
                  </div>
                  <span className="hidden sm:block text-sm font-medium text-gray-700">
                    {currentUser.name}
                  </span>
                </div>
                <button
                  onClick={onLogout}
                  className="p-2 text-gray-600 hover:text-red-600 hover:bg-red-50 rounded-xl transition-all"
                  title="Sair"
                >
                  <LogOut className="w-5 h-5" />
                </button>
              </div>
            ) : (
              <button
                onClick={onLogin}
                className="flex items-center space-x-2 px-4 py-2 bg-gradient-to-r from-blue-600 to-green-600 text-white rounded-xl hover:from-blue-700 hover:to-green-700 transition-all transform hover:scale-105 shadow-md"
              >
                <User className="w-4 h-4" />
                <span className="hidden sm:block text-sm font-medium">Entrar</span>
              </button>
            )}
          </div>
        </div>
      </div>
    </header>
  );
};