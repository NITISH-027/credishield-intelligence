import React, { useState } from 'react';
import { ZoomIn, ZoomOut, RotateCcw, AlertTriangle, Building2, UserCheck, History } from 'lucide-react';

export default function EntityGraphView({ graphData, onSelectEntity }) {
  const [zoom, setZoom] = useState(1);
  const [selectedNode, setSelectedNode] = useState(null);

  if (!graphData || !graphData.nodes || graphData.nodes.length === 0) {
    return (
      <div className="p-12 text-center text-[#5F6877] font-mono text-xs border border-[#202734] rounded-2xl bg-[#0D1118]">
        No corporate entity connections identified.
      </div>
    );
  }

  // Node coordinates layout
  const nodePositions = {};
  const primaryNode = graphData.nodes.find(n => n.type === 'PRIMARY_BUYER') || graphData.nodes[0];
  nodePositions[primaryNode.id] = { x: 380, y: 240 };

  let parentCount = 0;
  let subCount = 0;
  let sisterCount = 0;
  let prevCount = 0;

  graphData.nodes.forEach(node => {
    if (node.id === primaryNode.id) return;

    if (node.type === 'PARENT_HOLDING' || node.type === 'PARENT') {
      nodePositions[node.id] = { x: 260 + (parentCount++ * 240), y: 90 };
    } else if (node.type === 'SUBSIDIARY') {
      nodePositions[node.id] = { x: 260 + (subCount++ * 240), y: 390 };
    } else if (node.type.includes('SISTER') || node.type.includes('DIRECTOR')) {
      nodePositions[node.id] = { x: 650, y: 160 + (sisterCount++ * 150) };
    } else if (node.type === 'HISTORICAL_NAME') {
      nodePositions[node.id] = { x: 120, y: 240 + (prevCount++ * 120) };
    } else {
      nodePositions[node.id] = { x: 380 + ((sisterCount % 2 === 0 ? 1 : -1) * 200), y: 150 + (sisterCount++ * 100) };
    }
  });

  const getNodeStyle = (node) => {
    if (node.risk_level === 'CRITICAL') {
      return { fill: '#161014', stroke: '#E56B75', text: '#F4F3EF', badge: 'text-[#E56B75] border-[#E56B75]/30 bg-[#E56B75]/10' };
    }
    if (node.risk_level === 'HIGH') {
      return { fill: '#171510', stroke: '#E7B85C', text: '#F4F3EF', badge: 'text-[#E7B85C] border-[#E7B85C]/30 bg-[#E7B85C]/10' };
    }
    if (node.type === 'PRIMARY_BUYER') {
      return { fill: '#140E14', stroke: '#D58BAA', text: '#F4F3EF', badge: 'text-[#D58BAA] border-[#D58BAA]/30 bg-[#D58BAA]/10' };
    }
    if (node.type === 'PARENT' || node.type === 'PARENT_HOLDING') {
      return { fill: '#100E1C', stroke: '#6757D9', text: '#F4F3EF', badge: 'text-[#6757D9] border-[#6757D9]/30 bg-[#6757D9]/10' };
    }
    return { fill: '#0D1118', stroke: '#2C3547', text: '#8F98A8', badge: 'text-[#8F98A8] border-[#202734] bg-[#07090D]' };
  };

  return (
    <div className="space-y-6">
      
      {/* Header & Controls */}
      <div className="flex flex-col sm:flex-row sm:items-baseline justify-between gap-4 border-b border-[#202734] pb-4">
        <div>
          <span className="text-[11px] font-mono uppercase tracking-widest text-[#5F6877] block">
            Directorship & Equity Linkage
          </span>
          <h3 className="font-serif text-2xl text-[#F4F3EF] font-normal">
            Corporate Ownership Network
          </h3>
        </div>

        {/* Controls */}
        <div className="flex items-center gap-3 text-xs font-mono text-[#8F98A8]">
          <span className="text-[#5F6877]">{graphData.total_related_entities} Connected Entities</span>
          <div className="flex items-center gap-1 border border-[#202734] rounded-lg p-0.5 bg-[#0D1118]">
            <button 
              onClick={() => setZoom(z => Math.max(0.6, z - 0.15))}
              className="p-1.5 hover:text-[#F4F3EF] transition-colors"
              title="Zoom Out"
            >
              <ZoomOut className="w-3.5 h-3.5" />
            </button>
            <span className="px-1 text-[11px] text-[#5F6877]">{Math.round(zoom * 100)}%</span>
            <button 
              onClick={() => setZoom(z => Math.min(1.6, z + 0.15))}
              className="p-1.5 hover:text-[#F4F3EF] transition-colors"
              title="Zoom In"
            >
              <ZoomIn className="w-3.5 h-3.5" />
            </button>
            <button 
              onClick={() => { setZoom(1); setSelectedNode(null); }}
              className="p-1.5 hover:text-[#F4F3EF] transition-colors border-l border-[#202734]"
              title="Reset"
            >
              <RotateCcw className="w-3 h-3" />
            </button>
          </div>
        </div>
      </div>

      {/* Spillover Warning Banner if present */}
      {graphData.risk_spillover_detected && (
        <div className="p-4 rounded-xl bg-[#161014] border border-[#E56B75]/30 flex items-start gap-3 text-xs text-[#E56B75]">
          <AlertTriangle className="w-4 h-4 shrink-0 mt-0.5" />
          <p className="leading-relaxed">
            <strong className="font-semibold text-white">Group Risk Spillover Alert:</strong> A sister entity under common promoter directorship has defaulted or is admitted to CIRP insolvency proceedings.
          </p>
        </div>
      )}

      {/* Canvas & Inspector Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 rounded-2xl bg-[#0D1118] border border-[#202734] overflow-hidden">
        
        {/* Canvas Area */}
        <div className="lg:col-span-2 relative p-6 flex items-center justify-center min-h-[480px] border-b lg:border-b-0 lg:border-r border-[#202734] overflow-hidden">
          <div 
            className="transition-transform duration-200 ease-out origin-center"
            style={{ transform: `scale(${zoom})` }}
          >
            <svg width="760" height="480" className="overflow-visible select-none">
              <defs>
                <linearGradient id="gradient-line" x1="0%" y1="0%" x2="100%" y2="100%">
                  <stop offset="0%" stopColor="#6757D9" stopOpacity="0.8" />
                  <stop offset="100%" stopColor="#D58BAA" stopOpacity="0.8" />
                </linearGradient>
                <linearGradient id="gradient-line-danger" x1="0%" y1="0%" x2="100%" y2="100%">
                  <stop offset="0%" stopColor="#E56B75" stopOpacity="0.9" />
                  <stop offset="100%" stopColor="#E7B85C" stopOpacity="0.9" />
                </linearGradient>
              </defs>

              {/* Render Relationship Edges */}
              {graphData.edges.map(edge => {
                const sPos = nodePositions[edge.source] || { x: 380, y: 240 };
                const tPos = nodePositions[edge.target] || { x: 380, y: 240 };
                const isDanger = edge.relationship_type.includes('SISTER') && graphData.risk_spillover_detected;

                return (
                  <g key={edge.id}>
                    <line
                      x1={sPos.x}
                      y1={sPos.y}
                      x2={tPos.x}
                      y2={tPos.y}
                      stroke={isDanger ? 'url(#gradient-line-danger)' : 'url(#gradient-line)'}
                      strokeWidth={isDanger ? 2 : 1.25}
                      strokeDasharray={edge.relationship_type === 'HISTORICAL_RENAME' ? '4,4' : 'none'}
                      opacity={0.65}
                    />
                    <text
                      x={(sPos.x + tPos.x) / 2}
                      y={(sPos.y + tPos.y) / 2 - 6}
                      fill="#8F98A8"
                      fontSize="9"
                      fontFamily="IBM Plex Mono"
                      textAnchor="middle"
                    >
                      {edge.label}
                    </text>
                  </g>
                );
              })}

              {/* Render Entity Nodes */}
              {graphData.nodes.map(node => {
                const pos = nodePositions[node.id] || { x: 380, y: 240 };
                const style = getNodeStyle(node);
                const isSelected = selectedNode?.id === node.id;
                const isPrimary = node.type === 'PRIMARY_BUYER';

                return (
                  <g
                    key={node.id}
                    transform={`translate(${pos.x}, ${pos.y})`}
                    onClick={() => setSelectedNode(node)}
                    className="cursor-pointer group"
                  >
                    {isSelected && (
                      <circle
                        r={isPrimary ? 34 : 26}
                        fill="none"
                        stroke="#6757D9"
                        strokeWidth="1.5"
                        strokeDasharray="3,3"
                      />
                    )}

                    <circle
                      r={isPrimary ? 28 : 20}
                      fill={style.fill}
                      stroke={style.stroke}
                      strokeWidth={isSelected ? 2 : 1.25}
                      className="group-hover:opacity-90 transition-opacity"
                    />

                    {/* Node Icon */}
                    <g transform={`translate(${isPrimary ? -7 : -6}, ${isPrimary ? -7 : -6})`}>
                      {node.type === 'PRIMARY_BUYER' && <Building2 className="w-3.5 h-3.5 text-[#D58BAA]" />}
                      {node.type === 'PARENT' && <Building2 className="w-3.5 h-3.5 text-[#6757D9]" />}
                      {node.type.includes('SISTER') && <UserCheck className="w-3.5 h-3.5 text-[#E7B85C]" />}
                      {node.type === 'HISTORICAL_NAME' && <History className="w-3.5 h-3.5 text-[#8F98A8]" />}
                      {node.type === 'SUBSIDIARY' && <Building2 className="w-3.5 h-3.5 text-[#8F98A8]" />}
                    </g>

                    {/* Node Label Below */}
                    <text
                      y={isPrimary ? 44 : 34}
                      textAnchor="middle"
                      fill={style.text}
                      fontSize={isPrimary ? '11' : '10'}
                      fontWeight={isPrimary ? '600' : '400'}
                      fontFamily="Manrope"
                      className="pointer-events-none"
                    >
                      {node.label.length > 24 ? `${node.label.substring(0, 22)}...` : node.label}
                    </text>
                  </g>
                );
              })}
            </svg>
          </div>
        </div>

        {/* Node Inspector Panel */}
        <div className="p-8 flex flex-col justify-between space-y-6">
          <div className="space-y-4">
            <span className="text-[10px] font-mono uppercase tracking-widest text-[#5F6877] block">
              Node Details
            </span>

            {selectedNode ? (
              <div className="space-y-4 animate-fadeIn">
                <div>
                  <span className={`text-[10px] font-mono px-2 py-0.5 rounded border uppercase block w-fit mb-2 ${getNodeStyle(selectedNode).badge}`}>
                    {selectedNode.type.replace('_', ' ')}
                  </span>
                  <h4 className="text-base font-medium text-[#F4F3EF]">
                    {selectedNode.label}
                  </h4>
                  {selectedNode.cin && (
                    <p className="text-xs font-mono text-[#5F6877] mt-0.5">CIN: {selectedNode.cin}</p>
                  )}
                </div>

                <div className="space-y-2 text-xs font-mono pt-2 border-t border-[#202734]">
                  <div>
                    <span className="text-[#5F6877] block">Status:</span>
                    <span className="text-[#F4F3EF]">{selectedNode.company_status}</span>
                  </div>

                  {selectedNode.details?.shared_directors && (
                    <div>
                      <span className="text-[#5F6877] block">Shared Directors / DIN:</span>
                      <span className="text-[#F4F3EF]">
                        {Array.isArray(selectedNode.details.shared_directors)
                          ? selectedNode.details.shared_directors.join(', ')
                          : selectedNode.details.shared_directors}
                      </span>
                    </div>
                  )}

                  {selectedNode.details?.ownership_percentage && (
                    <div>
                      <span className="text-[#5F6877] block">Equity Interest:</span>
                      <span className="text-[#F4F3EF]">{selectedNode.details.ownership_percentage}</span>
                    </div>
                  )}

                  {selectedNode.details?.evidence && (
                    <div className="pt-1 font-sans font-light">
                      <span className="text-[#5F6877] font-mono block">Linkage Evidence:</span>
                      <p className="text-xs text-[#8F98A8] mt-1 leading-relaxed italic">
                        {selectedNode.details.evidence}
                      </p>
                    </div>
                  )}
                </div>
              </div>
            ) : (
              <div className="py-16 text-center text-xs text-[#5F6877] space-y-2">
                <Building2 className="w-6 h-6 mx-auto text-[#2C3547]" />
                <p>Click any network node to inspect directorship links and corporate cross-guarantee exposure.</p>
              </div>
            )}
          </div>

          <div className="pt-4 border-t border-[#202734] text-[11px] text-[#5F6877] font-mono">
            Directorship linkages mapped via Ministry of Corporate Affairs ROC Director Identification Numbers (DIN).
          </div>
        </div>

      </div>

    </div>
  );
}
