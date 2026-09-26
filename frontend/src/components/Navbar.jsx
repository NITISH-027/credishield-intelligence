import React from 'react';
import { Search, RefreshCw } from 'lucide-react';

export default function Navbar({ currentView, setCurrentView, demoBuyers, onSelectBuyer, onResetDemo }) {
  return (
    <header className="sticky top-0 z-50 bg-[#07090D]/85 backdrop-blur-md border-b border-[#202734]">
      <div className="max-w-6xl mx-auto px-6 h-16 flex items-center justify-between">
        
        {/* Brand */}
        <div 
          onClick={() => setCurrentView('landing')} 
          className="flex items-center gap-3 cursor-pointer group select-none"
        >
          <div className="w-6 h-6 rounded-md bg-[#121824] border border-[#202734] flex items-center justify-center group-hover:border-[#6757D9]/60 transition-colors">
            <span className="w-2 h-2 rounded-sm bg-signature-gradient"></span>
          </div>
          <div className="flex items-baseline gap-2">
            <span className="font-semibold text-sm tracking-tight text-[#F4F3EF] group-hover:text-white transition-colors">
              CrediShield
            </span>
            <span className="text-[11px] text-[#5F6877] font-mono tracking-wider">
              INTEL / PS-09-S2
            </span>
          </div>
        </div>

        {/* Minimal Navigation */}
        <nav className="hidden md:flex items-center gap-8 text-xs font-medium tracking-wide">
          <button
            onClick={() => setCurrentView('landing')}
            className={`transition-colors py-1 relative ${
              currentView === 'landing' 
                ? 'text-[#F4F3EF] font-semibold' 
                : 'text-[#8F98A8] hover:text-[#F4F3EF]'
            }`}
          >
            Overview
            {currentView === 'landing' && (
              <span className="absolute -bottom-5 left-0 right-0 h-[1.5px] bg-signature-gradient"></span>
            )}
          </button>
          
          <button
            onClick={() => setCurrentView('search')}
            className={`transition-colors py-1 relative flex items-center gap-1.5 ${
              currentView === 'search' 
                ? 'text-[#F4F3EF] font-semibold' 
                : 'text-[#8F98A8] hover:text-[#F4F3EF]'
            }`}
          >
            <Search className="w-3 h-3 text-[#5F6877]" />
            Check a Buyer
            {currentView === 'search' && (
              <span className="absolute -bottom-5 left-0 right-0 h-[1.5px] bg-signature-gradient"></span>
            )}
          </button>

          <button
            onClick={() => setCurrentView('demo-archetypes')}
            className={`transition-colors py-1 relative ${
              currentView === 'demo-archetypes' 
                ? 'text-[#F4F3EF] font-semibold' 
                : 'text-[#8F98A8] hover:text-[#F4F3EF]'
            }`}
          >
            5 Archetypes
            {currentView === 'demo-archetypes' && (
              <span className="absolute -bottom-5 left-0 right-0 h-[1.5px] bg-signature-gradient"></span>
            )}
          </button>
        </nav>

        {/* Right Tools */}
        <div className="flex items-center gap-4">
          
          {/* Quick Archetype Switcher */}
          <div className="hidden sm:block">
            <select
              aria-label="Select Demo Buyer"
              onChange={(e) => {
                if (e.target.value) {
                  onSelectBuyer(Number(e.target.value));
                }
              }}
              defaultValue=""
              className="bg-[#0D1118] border border-[#202734] hover:border-[#2C3547] text-[#8F98A8] hover:text-[#F4F3EF] text-xs font-mono rounded px-3 py-1.5 focus:outline-none focus:border-[#6757D9]/50 cursor-pointer transition-colors"
            >
              <option value="" disabled>Switch Dossier...</option>
              {demoBuyers.map(b => (
                <option key={b.id} value={b.id} className="bg-[#0D1118] text-[#F4F3EF]">
                  {b.demo_tag}: {b.trade_name || b.legal_name.split(' ')[0]}
                </option>
              ))}
            </select>
          </div>

          {/* Seed reset */}
          <button
            onClick={onResetDemo}
            title="Reset to benchmark seed"
            className="p-1.5 text-[#5F6877] hover:text-[#8F98A8] rounded transition-colors"
          >
            <RefreshCw className="w-3.5 h-3.5" />
          </button>

          {/* Understated Mode indicator */}
          <div className="flex items-center gap-2 pl-2 border-l border-[#202734] text-[11px] font-mono text-[#8F98A8]">
            <span className="w-1.5 h-1.5 rounded-full bg-[#55C89A]"></span>
            <span className="tracking-wider">BENCHMARK</span>
          </div>

        </div>

      </div>
    </header>
  );
}
