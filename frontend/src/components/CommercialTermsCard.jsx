import React from 'react';
import { Info, HelpCircle } from 'lucide-react';

export default function CommercialTermsCard({ recommendation }) {
  if (!recommendation) return null;

  const isUnknown = recommendation.evidence_state === 'INSUFFICIENT_EVIDENCE';

  const getTierTag = (tier) => {
    switch (tier) {
      case 'PREFERRED_CREDIT':
        return { label: 'Preferred Credit Terms', color: 'text-[#55C89A] border-[#55C89A]/30 bg-[#55C89A]/10' };
      case 'STANDARD_CREDIT':
        return { label: 'Standard Commercial Credit', color: 'text-[#D58BAA] border-[#D58BAA]/30 bg-[#D58BAA]/10' };
      case 'RESTRICTED_CREDIT':
        return { label: 'Restricted Credit Mandatory', color: 'text-[#E7B85C] border-[#E7B85C]/30 bg-[#E7B85C]/10' };
      case 'SECURED_ADVANCE':
        return { label: '100% Upfront Advance Mandate', color: 'text-[#E56B75] border-[#E56B75]/30 bg-[#E56B75]/10' };
      default:
        return { label: 'Conservative Milestone Terms', color: 'text-[#8D82E8] border-[#8D82E8]/30 bg-[#8D82E8]/10' };
    }
  };

  const tier = getTierTag(recommendation.commercial_tier);

  return (
    <div className="space-y-10 py-6">
      
      {/* Analyst Conclusion Header */}
      <div className="border-b border-[#202734] pb-6 space-y-4">
        <div className="flex flex-wrap items-center justify-between gap-4">
          <div className="space-y-1">
            <span className="text-[11px] font-mono uppercase tracking-widest text-[#5F6877]">
              Commercial Assessment & Terms
            </span>
            <div className="flex items-center gap-3">
              <h2 className="text-xl font-medium text-[#F4F3EF]">
                Commercial Term Guidance
              </h2>
              <span className={`text-xs font-mono px-2.5 py-0.5 rounded border ${tier.color}`}>
                {tier.label}
              </span>
            </div>
          </div>

          <div className="text-right font-mono text-xs text-[#8F98A8]">
            <span className="text-[#5F6877] block text-[10px] uppercase">Confidence</span>
            <span className="font-semibold text-[#F4F3EF]">
              {recommendation.confidence_tier} ({Math.round(recommendation.prediction_confidence * 100)}%)
            </span>
          </div>
        </div>

        {/* Executive Verdict Quote */}
        <div className="p-5 rounded-xl bg-[#0D1118] border-l-2 border-[#6757D9]">
          <p className="text-sm text-[#F4F3EF] leading-relaxed font-light italic">
            "{recommendation.summary_verdict}"
          </p>
        </div>
      </div>

      {/* Dominant Terms Strip (Spacious, Non-Boxed) */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-8 py-2 border-b border-[#202734] pb-10">
        
        <div className="space-y-2">
          <span className="text-xs font-mono uppercase tracking-wider text-[#5F6877] block">
            Suggested Advance
          </span>
          <div className="font-mono text-4xl sm:text-5xl font-light text-[#F4F3EF] tracking-tight">
            {recommendation.suggested_advance_pct}%
          </div>
          <p className="text-xs text-[#8F98A8]">
            {recommendation.suggested_advance_pct === 0 
              ? 'Unsecured supply acceptable under standard terms.' 
              : 'Upfront deposit advised before material dispatch.'}
          </p>
        </div>

        <div className="space-y-2 sm:border-l sm:border-[#202734] sm:pl-8">
          <span className="text-xs font-mono uppercase tracking-wider text-[#5F6877] block">
            Credit Period
          </span>
          <div className="font-mono text-4xl sm:text-5xl font-light text-[#F4F3EF] tracking-tight">
            {recommendation.recommended_credit_days} <span className="text-xl font-normal text-[#5F6877]">days</span>
          </div>
          <p className="text-xs text-[#8F98A8]">
            Agreed contractual payment maturity window.
          </p>
        </div>

        <div className="space-y-2 sm:border-l sm:border-[#202734] sm:pl-8">
          <span className="text-xs font-mono uppercase tracking-wider text-[#5F6877] block">
            Expected Payment
          </span>
          <div className="font-mono text-3xl sm:text-4xl font-light text-signature-gradient tracking-tight">
            {recommendation.expected_payment_window}
          </div>
          <p className="text-xs text-[#8F98A8]">
            {recommendation.expected_delay_days !== null
              ? `Estimated average delay: +${recommendation.expected_delay_days} days.`
              : 'Awaiting initial trade baseline.'}
          </p>
        </div>

      </div>

      {/* Ethical Unknown State Callout (when thin file) */}
      {isUnknown && (
        <div className="p-6 rounded-2xl bg-[#0D1118] border border-[#202734] space-y-2">
          <div className="flex items-center gap-2 text-xs font-mono text-[#8D82E8]">
            <Info className="w-4 h-4" />
            <span className="uppercase tracking-wider font-semibold">Mandatory Fairness Protocol</span>
          </div>
          <p className="text-xs text-[#8F98A8] leading-relaxed">
            We found limited public trade history for this buyer in searched registries. In accordance with ethical credit evaluation, 
            <strong> absence of evidence is not treated as adverse risk</strong>. We advise conservative milestone billing until receivables data accumulates.
          </p>
        </div>
      )}

      {/* "Why?" Rationale Section */}
      <div className="space-y-6 pt-2">
        <div className="flex items-center justify-between">
          <div className="space-y-0.5">
            <span className="text-[11px] font-mono uppercase tracking-widest text-[#5F6877]">
              Auditable Findings
            </span>
            <h3 className="font-serif text-2xl text-[#F4F3EF] font-normal">
              Why Did The System Reach This Conclusion?
            </h3>
          </div>
        </div>

        {/* Key Rationales List */}
        <div className="space-y-2 text-xs text-[#8F98A8]">
          {recommendation.why_reasons?.map((reason, idx) => (
            <div key={idx} className="flex items-start gap-3 py-1.5 border-b border-[#202734]/50">
              <span className="font-mono text-[#5F6877] mt-0.5">0{idx + 1}</span>
              <span className="text-[#F4F3EF] leading-relaxed">{reason}</span>
            </div>
          ))}
        </div>

        {/* Evidence Cards Grid */}
        {recommendation.evidence_cards && recommendation.evidence_cards.length > 0 && (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 pt-4">
            {recommendation.evidence_cards.map((card, idx) => (
              <div 
                key={idx}
                className="p-5 rounded-xl bg-[#0D1118] border border-[#202734] space-y-2 text-xs"
              >
                <div className="flex items-center justify-between text-[11px] font-mono text-[#5F6877]">
                  <span>{card.category.replace('_', ' ')}</span>
                  <span className={`px-2 py-0.5 rounded text-[10px] ${
                    card.impact === 'POSITIVE' ? 'text-[#55C89A] bg-[#55C89A]/10' :
                    card.impact === 'NEGATIVE' ? 'text-[#E56B75] bg-[#E56B75]/10' :
                    'text-[#8F98A8] bg-[#202734]'
                  }`}>
                    {card.impact}
                  </span>
                </div>

                <h4 className="font-medium text-sm text-[#F4F3EF]">
                  {card.headline}
                </h4>

                <p className="text-xs text-[#8F98A8] leading-relaxed font-light">
                  {card.evidence_snippet}
                </p>

                <div className="pt-2 border-t border-[#202734]/60 flex items-center justify-between text-[11px] text-[#5F6877] font-mono">
                  <span>Source: {card.source}</span>
                  <span>Confidence: {Math.round(card.confidence * 100)}%</span>
                </div>
              </div>
            ))}
          </div>
        )}

      </div>

      <div className="text-[11px] font-mono text-[#5F6877] pt-4">
        {recommendation.disclaimer}
      </div>

    </div>
  );
}
