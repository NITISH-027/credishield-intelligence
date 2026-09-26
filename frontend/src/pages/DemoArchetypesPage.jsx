import React from 'react';
import { ArrowRight, Info, AlertTriangle } from 'lucide-react';

export default function DemoArchetypesPage({ demoBuyers, onSelectBuyer }) {
  return (
    <div className="max-w-6xl mx-auto px-6 py-16 space-y-16 animate-fadeIn">
      
      {/* Header */}
      <div className="space-y-4 max-w-3xl">
        <span className="text-[11px] font-mono uppercase tracking-widest text-[#5F6877] block">
          Evaluation Benchmark
        </span>
        <h1 className="font-serif text-4xl sm:text-5xl text-[#F4F3EF] font-normal tracking-tight">
          Five Curated Commercial Archetypes
        </h1>
        <p className="text-sm text-[#8F98A8] font-light leading-relaxed">
          Designed to demonstrate the fundamental distinction between <strong className="text-[#E56B75] font-medium">known adverse evidence</strong> (chronic disputes, auditor qualifications, CIRP default) and <strong className="text-[#8D82E8] font-medium">absence of public records</strong> (thin-file small businesses).
        </p>
      </div>

      {/* Conceptual Distinction Callout */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 p-8 rounded-2xl bg-[#0D1118] border border-[#202734]">
        
        <div className="space-y-2">
          <div className="flex items-center gap-2 text-xs font-mono text-[#E56B75]">
            <AlertTriangle className="w-3.5 h-3.5" />
            <span className="uppercase tracking-wider font-semibold">Documented Delinquency (Buyers B, C, E)</span>
          </div>
          <p className="text-xs text-[#8F98A8] font-light leading-relaxed">
            The platform surfaces documented public evidence: active MSEFC arbitration orders, prolonged invoice delays (+48 days), negative net worth, and sister entities admitted to NCLT liquidation.
          </p>
        </div>

        <div className="space-y-2 md:border-l md:border-[#202734] md:pl-8">
          <div className="flex items-center gap-2 text-xs font-mono text-[#8D82E8]">
            <Info className="w-3.5 h-3.5" />
            <span className="uppercase tracking-wider font-semibold">Absence of Record ≠ Bad Credit (Buyer D)</span>
          </div>
          <p className="text-xs text-[#8F98A8] font-light leading-relaxed">
            Mandatory ethical rule: An honest newly-incorporated MSME with zero public credit history is <strong>not</strong> converted into high risk. The system outputs "We don't know" and recommends safe milestone terms.
          </p>
        </div>

      </div>

      {/* Archetypes Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {demoBuyers.map(buyer => {
          const isUnknown = buyer.evidence_state === 'INSUFFICIENT_EVIDENCE';
          const isPositive = buyer.suggested_advance_pct === 0;

          const badgeColor = isUnknown 
            ? 'text-[#8D82E8] border-[#8D82E8]/30 bg-[#8D82E8]/10' 
            : isPositive 
            ? 'text-[#55C89A] border-[#55C89A]/30 bg-[#55C89A]/10' 
            : 'text-[#E7B85C] border-[#E7B85C]/30 bg-[#E7B85C]/10';

          return (
            <div
              key={buyer.id}
              className="p-6 rounded-2xl bg-[#0D1118] border border-[#202734] hover:border-[#2C3547] flex flex-col justify-between space-y-6 transition-all"
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

                <div>
                  <h3 className="text-lg font-medium text-[#F4F3EF]">
                    {buyer.legal_name}
                  </h3>
                  <p className="text-xs text-[#5F6877] font-mono mt-0.5">
                    {buyer.industry} • {buyer.state}
                  </p>
                </div>

                <p className="text-xs text-[#8F98A8] font-light leading-relaxed">
                  {buyer.demo_scenario}
                </p>

                {/* Evidence Metrics Table */}
                <div className="space-y-2 text-xs font-mono pt-3 border-t border-[#202734]">
                  <div className="flex justify-between py-0.5">
                    <span className="text-[#5F6877]">Suggested Advance:</span>
                    <span className="text-[#F4F3EF] font-medium">{buyer.suggested_advance_pct}%</span>
                  </div>
                  <div className="flex justify-between py-0.5">
                    <span className="text-[#5F6877]">Credit Period:</span>
                    <span className="text-[#F4F3EF]">{buyer.recommended_credit_days} days</span>
                  </div>
                  <div className="flex justify-between py-0.5">
                    <span className="text-[#5F6877]">Expected Payment:</span>
                    <span className="text-[#F4F3EF]">{buyer.expected_payment_window}</span>
                  </div>
                  <div className="flex justify-between py-0.5">
                    <span className="text-[#5F6877]">MSME Disputes:</span>
                    <span className={buyer.disputes_count > 0 ? 'text-[#E56B75]' : 'text-[#55C89A]'}>
                      {buyer.disputes_count} records
                    </span>
                  </div>
                  <div className="flex justify-between py-0.5">
                    <span className="text-[#5F6877]">Group Spillover:</span>
                    <span className={buyer.has_related_defaults ? 'text-[#E56B75]' : 'text-[#5F6877]'}>
                      {buyer.has_related_defaults ? 'Detected' : 'None'}
                    </span>
                  </div>
                </div>

              </div>

              <button
                onClick={() => onSelectBuyer(buyer.id)}
                className="w-full py-2.5 bg-[#121824] hover:bg-[#202734] border border-[#202734] text-[#F4F3EF] rounded-lg text-xs font-medium transition-colors flex items-center justify-center gap-1.5"
              >
                Inspect Complete Dossier
                <ArrowRight className="w-3.5 h-3.5" />
              </button>

            </div>
          );
        })}
      </div>

    </div>
  );
}
