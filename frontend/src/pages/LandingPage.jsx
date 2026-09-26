import React, { useState } from 'react';
import { Search, ArrowRight } from 'lucide-react';
import { searchBuyers } from '../services/api';

export default function LandingPage({ onSelectBuyer, onNavigateSearch, onNavigateDemo, demoBuyers }) {
  const [query, setQuery] = useState('');
  const [isSearching, setIsSearching] = useState(false);
  const [searchResult, setSearchResult] = useState(null);

  const handleQuickSearch = async (e) => {
    e.preventDefault();
    if (!query.trim()) return;

    setIsSearching(true);
    try {
      const res = await searchBuyers(query);
      setSearchResult(res);
    } catch (err) {
      console.error(err);
    } finally {
      setIsSearching(false);
    }
  };

  const getStatusColor = (status) => {
    if (status === 'MATCHED') return 'text-[#55C89A] border-[#55C89A]/30 bg-[#55C89A]/10';
    if (status === 'LIKELY_MATCH') return 'text-[#D58BAA] border-[#D58BAA]/30 bg-[#D58BAA]/10';
    if (status === 'POSSIBLE_MATCH') return 'text-[#E7B85C] border-[#E7B85C]/30 bg-[#E7B85C]/10';
    return 'text-[#E56B75] border-[#E56B75]/30 bg-[#E56B75]/10';
  };

  return (
    <div className="space-y-28 pb-32">
      
      {/* Editorial Hero Section */}
      <section className="relative pt-20 sm:pt-28 text-center max-w-4xl mx-auto px-6 space-y-8 atmospheric-glow">
        
        {/* Subtle Category Eyebrow */}
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full border border-[#202734] bg-[#0D1118] text-xs font-mono text-[#8F98A8]">
          <span className="w-1.5 h-1.5 rounded-full bg-[#D58BAA]"></span>
          <span>B2B PAYMENT RISK & ENTITY INTELLIGENCE</span>
        </div>

        {/* Editorial Headline with Instrument Serif */}
        <div className="space-y-2">
          <h1 className="font-serif text-5xl sm:text-7xl font-normal tracking-tight text-[#F4F3EF] leading-[1.08]">
            Before you give credit,
          </h1>
          <h2 className="font-serif text-5xl sm:text-7xl font-normal tracking-tight text-signature-gradient leading-[1.08] italic">
            know who you're dealing with.
          </h2>
        </div>

        {/* Sophisticated Body Subtext */}
        <p className="text-base sm:text-lg text-[#8F98A8] max-w-2xl mx-auto leading-relaxed font-light">
          Search a buyer. Resolve corporate identity. Trace historical delay behaviour. 
          Investigate public MSME and insolvency filings. Set commercial terms with certainty.
        </p>

        {/* Minimal Search Bar */}
        <div className="max-w-2xl mx-auto pt-4 space-y-4">
          <form onSubmit={handleQuickSearch} className="relative flex items-center">
            <Search className="w-4 h-4 absolute left-4 text-[#5F6877] pointer-events-none" />
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Search company legal name, CIN, or GSTIN..."
              className="w-full bg-[#0D1118] border border-[#202734] hover:border-[#2C3547] focus:border-[#6757D9]/60 rounded-xl py-3.5 pl-11 pr-32 text-sm text-[#F4F3EF] placeholder-[#5F6877] focus:outline-none transition-colors"
            />
            <button
              type="submit"
              disabled={isSearching}
              className="absolute right-2 px-4 py-2 bg-signature-gradient text-[#07090D] font-semibold rounded-lg text-xs hover:opacity-95 transition-opacity flex items-center gap-1.5"
            >
              {isSearching ? 'Resolving...' : 'Check Buyer'}
              <ArrowRight className="w-3.5 h-3.5" />
            </button>
          </form>

          {/* Quick Resolution Result Card */}
          {searchResult && (
            <div className="p-5 bg-[#0D1118] border border-[#202734] rounded-xl text-left shadow-2xl space-y-3">
              <div className="flex items-center justify-between text-xs font-mono">
                <span className="text-[#5F6877] uppercase tracking-wider">Resolution Status</span>
                <span className={`px-2 py-0.5 rounded border text-[11px] font-medium ${getStatusColor(searchResult.resolution_status)}`}>
                  {searchResult.resolution_status}
                </span>
              </div>

              {searchResult.best_candidate ? (
                <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pt-1">
                  <div>
                    <h4 className="font-semibold text-base text-[#F4F3EF]">
                      {searchResult.best_candidate.legal_name}
                    </h4>
                    <p className="text-xs font-mono text-[#8F98A8] mt-0.5">
                      CIN: {searchResult.best_candidate.cin} • {searchResult.best_candidate.state}
                    </p>
                    <p className="text-xs text-[#5F6877] mt-1">
                      Signals: {searchResult.best_candidate.match_signals.join(' • ')}
                    </p>
                  </div>
                  <button
                    onClick={() => onSelectBuyer(searchResult.best_candidate.id)}
                    className="px-4 py-2 bg-[#121824] hover:bg-[#202734] border border-[#202734] text-[#F4F3EF] text-xs font-medium rounded-lg transition-colors shrink-0"
                  >
                    Open Dossier →
                  </button>
                </div>
              ) : (
                <p className="text-xs text-[#8F98A8]">{searchResult.explanation}</p>
              )}
            </div>
          )}

          {/* Action Links */}
          <div className="flex items-center justify-center gap-4 pt-2">
            <button
              onClick={onNavigateSearch}
              className="px-6 py-2.5 bg-signature-gradient text-[#07090D] font-semibold text-xs rounded-lg hover:opacity-95 transition-opacity"
            >
              Check a Buyer
            </button>
            <button
              onClick={onNavigateDemo}
              className="px-6 py-2.5 bg-[#0D1118] hover:bg-[#121824] border border-[#202734] text-[#8F98A8] hover:text-[#F4F3EF] text-xs font-medium rounded-lg transition-colors"
            >
              Explore Demo Archetypes
            </button>
          </div>
        </div>

      </section>

      {/* Spacious Archetypes Gallery */}
      <section className="max-w-6xl mx-auto px-6 space-y-8">
        
        <div className="flex flex-col sm:flex-row sm:items-end justify-between gap-4 border-b border-[#202734] pb-5">
          <div>
            <span className="text-[11px] font-mono uppercase tracking-widest text-[#5F6877] block mb-1">
              Curated Profiles
            </span>
            <h2 className="font-serif text-3xl sm:text-4xl text-[#F4F3EF] font-normal">
              Five Commercial Archetypes
            </h2>
          </div>
          <p className="text-xs text-[#8F98A8] max-w-md">
            Compare distinct behavioral profiles: from spotless settlement track records to chronic dispute patterns, balance-sheet distress, and group entity debt contagion.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {demoBuyers.map(buyer => {
            const isUnknown = buyer.evidence_state === 'INSUFFICIENT_EVIDENCE';
            const isNegative = buyer.suggested_advance_pct >= 40 || buyer.commercial_tier === 'RESTRICTED_CREDIT';
            const isPositive = buyer.suggested_advance_pct === 0;

            const badgeColor = isUnknown 
              ? 'text-[#8D82E8] border-[#8D82E8]/30 bg-[#8D82E8]/10' 
              : isPositive 
              ? 'text-[#55C89A] border-[#55C89A]/30 bg-[#55C89A]/10' 
              : 'text-[#E7B85C] border-[#E7B85C]/30 bg-[#E7B85C]/10';

            return (
              <div
                key={buyer.id}
                onClick={() => onSelectBuyer(buyer.id)}
                className="group p-6 rounded-2xl bg-[#0D1118] hover:bg-[#121824] border border-[#202734] hover:border-[#2C3547] cursor-pointer transition-all duration-200 flex flex-col justify-between space-y-6"
              >
                <div className="space-y-3">
                  <div className="flex items-center justify-between">
                    <span className="text-xs font-mono text-[#5F6877]">
                      {buyer.demo_tag}
                    </span>
                    <span className={`text-[10px] font-mono px-2 py-0.5 rounded border uppercase ${badgeColor}`}>
                      {buyer.evidence_state.replace('_', ' ')}
                    </span>
                  </div>

                  <h3 className="text-lg font-medium text-[#F4F3EF] group-hover:text-white transition-colors leading-snug">
                    {buyer.legal_name}
                  </h3>

                  <p className="text-xs text-[#5F6877] font-mono">
                    {buyer.industry} • {buyer.state}
                  </p>

                  <p className="text-xs text-[#8F98A8] line-clamp-2 leading-relaxed pt-1">
                    {buyer.demo_scenario}
                  </p>
                </div>

                {/* Key Metrics Strip */}
                <div className="pt-4 border-t border-[#202734] grid grid-cols-3 gap-2 text-left">
                  <div>
                    <span className="text-[10px] font-mono text-[#5F6877] block uppercase">Advance</span>
                    <span className="font-mono text-sm font-medium text-[#F4F3EF]">{buyer.suggested_advance_pct}%</span>
                  </div>
                  <div>
                    <span className="text-[10px] font-mono text-[#5F6877] block uppercase">Credit</span>
                    <span className="font-mono text-sm font-medium text-[#F4F3EF]">{buyer.recommended_credit_days}d</span>
                  </div>
                  <div>
                    <span className="text-[10px] font-mono text-[#5F6877] block uppercase">Disputes</span>
                    <span className={`font-mono text-sm font-medium ${buyer.disputes_count > 0 ? 'text-[#E56B75]' : 'text-[#55C89A]'}`}>
                      {buyer.disputes_count}
                    </span>
                  </div>
                </div>

              </div>
            );
          })}
        </div>

      </section>

      {/* Editorial Methodology Section */}
      <section className="max-w-6xl mx-auto px-6 pt-6">
        <div className="p-8 sm:p-12 rounded-2xl bg-[#0D1118] border border-[#202734] grid grid-cols-1 md:grid-cols-3 gap-8 sm:gap-12">
          
          <div className="space-y-3">
            <span className="text-xs font-mono text-[#6757D9] block">01 / IDENTITY</span>
            <h3 className="font-serif text-2xl text-[#F4F3EF] font-normal">Entity Resolution</h3>
            <p className="text-xs text-[#8F98A8] leading-relaxed">
              Standardizes corporate legal forms across jurisdictions. Resolves CIN, GSTIN, and directorship ties to uncover cross-entity guarantee and default exposure.
            </p>
          </div>

          <div className="space-y-3">
            <span className="text-xs font-mono text-[#D58BAA] block">02 / EVIDENCE</span>
            <h3 className="font-serif text-2xl text-[#F4F3EF] font-normal">Statutory Signals</h3>
            <p className="text-xs text-[#8F98A8] leading-relaxed">
              Cross-references Section 18 MSME Samadhaan dispute awards, MCA21 annual balance sheet filings, and active CIRP insolvency listings under IBC 2016.
            </p>
          </div>

          <div className="space-y-3">
            <span className="text-xs font-mono text-[#8D82E8] block">03 / FAIRNESS</span>
            <h3 className="font-serif text-2xl text-[#F4F3EF] font-normal">Ethical Uncertainty</h3>
            <p className="text-xs text-[#8F98A8] leading-relaxed">
              Missing data is never interpreted as poor creditworthiness. When evidence is thin, the platform explicitly acknowledges uncertainty to protect honest small businesses.
            </p>
          </div>

        </div>
      </section>

    </div>
  );
}
