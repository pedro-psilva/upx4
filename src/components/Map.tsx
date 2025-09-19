import React from 'react';
import { MapPin } from 'lucide-react';
import { Proposal } from '../types';
import { categories } from '../data/categories';

interface MapProps {
  proposals: Proposal[];
  onProposalClick: (proposal: Proposal) => void;
  selectedProposal?: Proposal | null;
}

export const Map: React.FC<MapProps> = ({ 
  proposals, 
  onProposalClick, 
  selectedProposal 
}) => {
  // Center of the map (São Paulo downtown as example)
  const mapCenter = { lat: -23.550520, lng: -46.633308 };
  
  // Convert lat/lng to pixel positions (simplified for demo)
  const latLngToPixel = (lat: number, lng: number) => {
    const mapBounds = {
      north: -23.545,
      south: -23.556,
      west: -46.640,
      east: -46.626
    };
    
    const x = ((lng - mapBounds.west) / (mapBounds.east - mapBounds.west)) * 100;
    const y = ((mapBounds.north - lat) / (mapBounds.north - mapBounds.south)) * 100;
    
    return { x: Math.max(0, Math.min(100, x)), y: Math.max(0, Math.min(100, y)) };
  };

  return (
    <div className="relative w-full h-96 bg-gray-100 rounded-lg overflow-hidden map-container">
      {/* Map background */}
      <div className="absolute inset-0 bg-gradient-to-br from-green-100 via-blue-50 to-green-100">
        {/* Simulated streets */}
        <div className="absolute inset-0">
          <div className="absolute top-1/4 left-0 right-0 h-1 bg-gray-300"></div>
          <div className="absolute top-2/4 left-0 right-0 h-1 bg-gray-300"></div>
          <div className="absolute top-3/4 left-0 right-0 h-1 bg-gray-300"></div>
          <div className="absolute top-0 bottom-0 left-1/4 w-1 bg-gray-300"></div>
          <div className="absolute top-0 bottom-0 left-2/4 w-1 bg-gray-300"></div>
          <div className="absolute top-0 bottom-0 left-3/4 w-1 bg-gray-300"></div>
        </div>
      </div>

      {/* Proposals markers */}
      {proposals.map((proposal) => {
        const position = latLngToPixel(proposal.latitude, proposal.longitude);
        const category = categories.find(cat => cat.id === proposal.category);
        const isSelected = selectedProposal?.id === proposal.id;

        return (
          <div
            key={proposal.id}
            className={`absolute transform -translate-x-1/2 -translate-y-1/2 cursor-pointer transition-all duration-200 ${
              isSelected ? 'z-20 scale-110' : 'z-10 hover:scale-105'
            }`}
            style={{
              left: `${position.x}%`,
              top: `${position.y}%`
            }}
            onClick={() => onProposalClick(proposal)}
          >
            {/* Marker */}
            <div
              className={`w-6 h-6 rounded-full border-2 border-white shadow-lg flex items-center justify-center ${
                isSelected ? 'ring-2 ring-blue-400 ring-opacity-75' : ''
              }`}
              style={{ backgroundColor: category?.color || '#6B7280' }}
            >
              <MapPin className="w-3 h-3 text-white" />
            </div>
            
            {/* Tooltip */}
            {isSelected && (
              <div className="absolute bottom-8 left-1/2 transform -translate-x-1/2 bg-white rounded-lg shadow-lg border border-gray-200 p-3 min-w-48 max-w-64 z-30">
                <div className="absolute -bottom-1 left-1/2 transform -translate-x-1/2 w-2 h-2 bg-white border-r border-b border-gray-200 rotate-45"></div>
                <h4 className="font-medium text-sm text-gray-900 mb-1 line-clamp-2">
                  {proposal.title}
                </h4>
                <p className="text-xs text-gray-500 mb-2">{proposal.address}</p>
                <div className="flex items-center justify-between">
                  <span
                    className="text-xs px-2 py-1 rounded-full"
                    style={{
                      backgroundColor: `${category?.color}20`,
                      color: category?.color
                    }}
                  >
                    {category?.name}
                  </span>
                  <span className="text-xs text-gray-500">
                    {proposal.votes_count} votos
                  </span>
                </div>
              </div>
            )}
          </div>
        );
      })}

      {/* Map controls */}
      <div className="absolute top-4 right-4 bg-white rounded-lg shadow-md border border-gray-200">
        <div className="p-2 space-y-1">
          <button className="w-8 h-8 flex items-center justify-center text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded">
            +
          </button>
          <div className="w-full h-px bg-gray-200"></div>
          <button className="w-8 h-8 flex items-center justify-center text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded">
            −
          </button>
        </div>
      </div>

      {/* Legend */}
      <div className="absolute bottom-4 left-4 bg-white rounded-lg shadow-md border border-gray-200 p-3">
        <h4 className="text-sm font-medium text-gray-900 mb-2">Categorias</h4>
        <div className="space-y-1">
          {categories.slice(0, 4).map((category) => (
            <div key={category.id} className="flex items-center space-x-2">
              <div
                className="w-3 h-3 rounded-full"
                style={{ backgroundColor: category.color }}
              ></div>
              <span className="text-xs text-gray-600">{category.name}</span>
            </div>
          ))}
          {categories.length > 4 && (
            <div className="text-xs text-gray-500">+{categories.length - 4} mais</div>
          )}
        </div>
      </div>
    </div>
  );
};