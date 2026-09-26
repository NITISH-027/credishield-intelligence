import React, { useState } from 'react';
import { Search, ArrowRight } from 'lucide-react';
import { searchBuyers } from '../services/api';

export default function SearchPage({ onSelectBuyer }) {
  const [query, setQuery] = useState('');
  const [cin, setCin] = useState('');
  const [gstin, setGstin] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  const sampleQueries = [
    { label: 'Apex Machining (Historical Name)', q: 'Apex Machining Works' },
    { label: 'Bharat Infra (Direct Name)', q: 'Bharat Infra Ventures' },
    { label: 'Champaran Cold (Distressed)', q: 'Champaran Cold Storage' },
    { label: 'Deccan Precision (Thin-File)', q: 'Deccan Precision Tools' },
    { label: 'SunPower Heavy (Rebranded Group)', q: 'SunPower Heavy Engineering' },
    { label: 'Exact CIN Match', q: '', cin: 'U28112MH2016PTC284910' },
  ];

  const handleSearch = async (e, overrideQ = null, overrideCin = null) => {
    if (e) e.preventDefault();
    const activeQ = overrideQ !== null ? overrideQ : query;
    const activeCin = overrideCin !== null ? overrideCin : cin;

    if (!activeQ.trim() && !activeCin.trim() && !gstin.trim()) return;

    setLoading(true);
    try {
      const res = await searchBuyers(activeQ, activeCin || null, gstin || null);
      setResult(res);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleApplySample = (sample) => {
    setQuery(sample.q || '');
    setCin(sample.cin || '');
    handleSearch(null, sample.q || '', sample.cin || '');
  };

  const getStatusColor = (status) => {
    if (status === 'MATCHED') return 'text-[#55C89A] border-[#55C89A]/30 bg-[#55C89A]/10';
    if (status === 'LIKELY_MATCH') return 'text-[#D58BAA] border-[#D58BAA]/30 bg-[#D58BAA]/10';
    if (status === 'POSSIBLE_MATCH') return 'text-[#E7B85C] border-[#E7B85C]/30 bg-[#E7B85C]/10';
    return 'text-[#E56B75] border-[#E56B75]/30 bg-[#E56B75]/10';
  };

  return (
    <div className="max-w-4xl mx-auto px-6 py-16 space-y-12 animate-fadeIn">
      
      {/* Header */}
      <div className="space-y-3">
        <span className="text-[11px] font-mono uppercase tracking-widest text-[#5F6877] block">
          Corporate Identity Engine
        </span>
        <h1 className="font-serif text-4xl sm:text-5xl text-[#F4F3EF] font-normal tracking-tight">
          Check a Buyer & Resolve Entity
        </h1>
        <p className="text-sm text-[#8F98A8] font-light max-w-2xl leading-relaxed">
          Search by legal name, trade alias, CIN, or GSTIN. The engine normalizes corporate forms, compares token fingerprints, checks ROC former legal names, and surfaces connected entities.
        </p>
      </div>

      {/* Main Search Panel */}
      <div className="p-8 rounded-2xl bg-[#0D1118] border border-[#202734] space-y-6">
        
        <form onSubmit={handleSearch} className="space-y-5">
          <div className="space-y-2">
            <label className="text-xs font-mono uppercase tracking-wider text-[#5F6877] block">
              Company Legal Name or Commercial Trade Alias
            </label>
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="e.g. Apex Precision Technologies Pvt Ltd, Bharat Infra..."
              className="w-full bg-[#07090D] border border-[#202734] hover:border-[#2C3547] focus:border-[#6757D9]/60 rounded-xl py-3.5 px-4 text-sm text-[#F4F3EF] placeholder-[#5F6877] focus:outline-none transition-colors"
            />
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div className="space-y-1.5">
              <label className="text-[11px] font-mono uppercase tracking-wider text-[#5F6877] block">
                CIN [21-Digit Identifier]
              </label>
              <input
                type="text"
                value={cin}
                onChange={(e) => setCin(e.target.value)}
                placeholder="e.g. U28112MH2016PTC284910"
                className="w-full bg-[#07090D] border border-[#202734] focus:border-[#6757D9]/60 rounded-lg py-2.5 px-3 text-xs text-[#F4F3EF] placeholder-[#5F6877] font-mono focus:outline-none"
              />
            </div>

            <div className="space-y-1.5">
              <label className="text-[11px] font-mono uppercase tracking-wider text-[#5F6877] block">
                GSTIN [15-Char Tax Number]
              </label>
              <input
                type="text"
                value={gstin}
                onChange={(e) => setGstin(e.target.value)}
                placeholder="e.g. 27AABCA1234F1Z5"
                className="w-full bg-[#07090D] border border-[#202734] focus:border-[#6757D9]/60 rounded-lg py-2.5 px-3 text-xs text-[#F4F3EF] placeholder-[#5F6877] font-mono focus:outline-none"
              />
            </div>
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full py-3 bg-signature-gradient text-[#07090D] font-semibold rounded-xl text-xs sm:text-sm hover:opacity-95 transition-opacity flex items-center justify-center gap-2"
          >
            <Search className="w-4 h-4" />
            {loading ? 'Running Multi-Signal Resolution...' : 'Search & Resolve Identity'}
          </button>
        </form>

        {/* Quick Sample Queries */}
        <div className="pt-4 border-t border-[#202734]">
          <span className="text-[11px] font-mono text-[#5F6877] uppercase tracking-wider block mb-2.5">
            Test Cases:
          </span>
          <div className="flex flex-wrap gap-2">
            {sampleQueries.map((s, idx) => (
              <button
                key={idx}
                type="button"
                onClick={() => handleApplySample(s)}
                className="px-2.5 py-1 rounded bg-[#07090D] hover:bg-[#121824] border border-[#202734] text-[11px] font-mono text-[#8F98A8] hover:text-[#F4F3EF] transition-colors"
              >
                {s.label}
              </button>
            ))}
          </div>
        </div>

      </div>

      {/* Resolution Output */}
      {result && (
        <div className="p-8 rounded-2xl bg-[#0D1118] border border-[#202734] space-y-6 animate-fadeIn">
          
          <div className="flex items-center justify-between border-b border-[#202734] pb-4">
            <div>
              <span className="text-[10px] font-mono uppercase text-[#5F6877] block">
                Resolution Finding
              </span>
              <h3 className="font-serif text-2xl text-[#F4F3EF] font-normal mt-0.5">
                {result.resolution_status === 'UNRESOLVED' ? 'No Confirmed Legal Match' : result.resolved_primary_name}
              </h3>
            </div>
            <span className={`text-xs font-mono px-3 py-1 rounded border ${getStatusColor(result.resolution_status)}`}>
              {result.resolution_status}
            </span>
          </div>

          <p className="text-xs text-[#8F98A8] font-light leading-relaxed p-4 rounded-xl bg-[#07090D] border border-[#202734]">
            {result.explanation}
          </p>

          {/* Evaluated Candidates */}
          {result.all_candidates && result.all_candidates.length > 0 && (
            <div className="space-y-3 pt-2">
              <span className="text-xs font-mono uppercase tracking-wider text-[#5F6877] block">
                Evaluated Corporate Candidates ({result.all_candidates.length})
              </span>

              {result.all_candidates.map((cand, idx) => (
                <div
                  key={idx}
                  className="p-5 rounded-xl bg-[#07090D] border border-[#202734] flex flex-col sm:flex-row sm:items-center justify-between gap-4"
                >
                  <div className="space-y-1">
                    <div className="flex items-center gap-3">
                      <span className="font-medium text-sm text-[#F4F3EF]">{cand.legal_name}</span>
                      <span className={`text-[10px] font-mono px-2 py-0.5 rounded border ${getStatusColor(cand.match_status)}`}>
                        {Math.round(cand.match_confidence * 100)}% Match
                      </span>
                    </div>

                    <div className="text-xs font-mono text-[#5F6877] space-x-3">
                      <span>CIN: {cand.cin || 'N/A'}</span>
                      <span>GSTIN: {cand.gstin || 'N/A'}</span>
                      <span>{cand.city}, {cand.state}</span>
                    </div>

                    <div className="text-[11px] text-[#6757D9] pt-0.5 font-mono">
                      Signals: {cand.match_signals.join(' • ')}
                    </div>
                  </div>

                  <button
                    onClick={() => onSelectBuyer(cand.id)}
                    className="px-4 py-2 bg-[#121824] hover:bg-[#202734] border border-[#202734] text-[#F4F3EF] text-xs font-medium rounded-lg transition-colors shrink-0 flex items-center gap-1.5"
                  >
                    Open Dossier
                    <ArrowRight className="w-3.5 h-3.5" />
                  </button>
                </div>
              ))}
            </div>
          )}

        </div>
      )}

    </div>
  );
}
