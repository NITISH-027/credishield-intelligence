import React from 'react';
import { ExternalLink } from 'lucide-react';

export default function PublicEvidenceView({ disputes, filings, insolvencyRecords, buyerName }) {
  const unresolvedDisputes = disputes?.filter(d => d.is_unresolved) || [];
  const primaryInsolvency = insolvencyRecords?.[0] || { status: 'NO_PUBLIC_RECORD_FOUND' };

  return (
    <div className="space-y-12">
      
      {/* 3 Investigation Streams Summary */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        
        {/* Stream 1: MSME Facilitation Council */}
        <div className="p-6 rounded-2xl bg-[#0D1118] border border-[#202734] space-y-3">
          <div className="flex items-center justify-between text-xs font-mono text-[#5F6877]">
            <span className="uppercase tracking-wider">MSME Samadhaan (MSEFC)</span>
            <span className={unresolvedDisputes.length > 0 ? 'text-[#E56B75]' : 'text-[#55C89A]'}>
              {unresolvedDisputes.length} Unresolved
            </span>
          </div>

          <div className="font-mono text-3xl font-light text-[#F4F3EF]">
            {disputes?.length || 0} <span className="text-sm font-normal text-[#5F6877]">cases</span>
          </div>

          <p className="text-xs text-[#8F98A8] font-light leading-relaxed">
            {disputes && disputes.length > 0 ? (
              <span>
                Cumulative claim value: <strong className="text-[#F4F3EF] font-mono">INR {disputes.reduce((sum, d) => sum + (d.claim_amount || 0), 0).toLocaleString()}</strong>.
              </span>
            ) : (
              'Clean public record. Zero supplier delayed payment claims lodged on state MSEFC council portals.'
            )}
          </p>
        </div>

        {/* Stream 2: MCA21 ROC Filings */}
        <div className="p-6 rounded-2xl bg-[#0D1118] border border-[#202734] space-y-3">
          <div className="flex items-center justify-between text-xs font-mono text-[#5F6877]">
            <span className="uppercase tracking-wider">MCA21 / ROC Statutory</span>
            <span className="text-[#8F98A8]">
              {filings?.length || 0} Annual Filings
            </span>
          </div>

          <div className="font-mono text-2xl font-light text-[#F4F3EF] pt-0.5">
            {filings?.some(f => f.going_concern_warning || f.auditor_qualification_flag) ? (
              <span className="text-[#E7B85C]">Audit Exceptions</span>
            ) : (
              <span className="text-[#55C89A]">Clean Audit</span>
            )}
          </div>

          <p className="text-xs text-[#8F98A8] font-light leading-relaxed">
            {filings?.some(f => f.going_concern_warning) ? (
              'Material uncertainty on Going Concern highlighted in CARO auditor disclosures.'
            ) : filings?.some(f => f.auditor_qualification_flag) ? (
              'Statutory auditor qualifications noted regarding trade payables to small enterprises.'
            ) : (
              'Audited annual returns (Form AOC-4) filed on schedule with clean auditor opinions.'
            )}
          </p>
        </div>

        {/* Stream 3: Insolvency CIRP Registry */}
        <div className="p-6 rounded-2xl bg-[#0D1118] border border-[#202734] space-y-3">
          <div className="flex items-center justify-between text-xs font-mono text-[#5F6877]">
            <span className="uppercase tracking-wider">NCLT / IBBI CIRP</span>
            <span className={
              primaryInsolvency.status === 'ADMITTED' ? 'text-[#E56B75]' :
              primaryInsolvency.status === 'NO_PUBLIC_RECORD_FOUND' ? 'text-[#55C89A]' : 'text-[#E7B85C]'
            }>
              {primaryInsolvency.status === 'NO_PUBLIC_RECORD_FOUND' ? 'Clear' : primaryInsolvency.status}
            </span>
          </div>

          <div className="font-mono text-xl font-light text-[#F4F3EF] pt-1 truncate">
            {primaryInsolvency.status === 'NO_PUBLIC_RECORD_FOUND' ? 'No Public Record Found' : primaryInsolvency.status}
          </div>

          <p className="text-xs text-[#8F98A8] font-light leading-relaxed">
            {primaryInsolvency.status_details || 'Verified across National Company Law Tribunal cause lists.'}
          </p>
        </div>

      </div>

      {/* Detailed Investigation Logs */}
      
      {/* 1. MSME Disputes */}
      <div className="space-y-4">
        <div className="flex items-baseline justify-between border-b border-[#202734] pb-3">
          <div>
            <span className="text-[11px] font-mono uppercase tracking-widest text-[#5F6877] block">
              Section 18 MSMED Act
            </span>
            <h4 className="font-serif text-2xl text-[#F4F3EF] font-normal">
              MSME Payment Disputes
            </h4>
          </div>
          <a
            href="https://samadhaan.msme.gov.in/"
            target="_blank"
            rel="noreferrer"
            className="text-xs font-mono text-[#6757D9] hover:underline flex items-center gap-1"
          >
            MSME Samadhaan Portal <ExternalLink className="w-3 h-3" />
          </a>
        </div>

        {disputes && disputes.length > 0 ? (
          <div className="space-y-3">
            {disputes.map((disp, idx) => (
              <div 
                key={idx}
                className="p-5 rounded-xl bg-[#0D1118] border border-[#202734] space-y-3 text-xs"
              >
                <div className="flex flex-col sm:flex-row sm:items-baseline justify-between gap-2 font-mono">
                  <div className="flex items-center gap-3">
                    <span className="text-[#F4F3EF] font-semibold">{disp.case_number}</span>
                    <span className="text-[#5F6877]">({disp.council_location})</span>
                  </div>
                  <div className="flex items-center gap-3">
                    <span className="text-[#5F6877]">Filed: {disp.application_date}</span>
                    <span className={`px-2 py-0.5 rounded border text-[10px] uppercase ${
                      disp.is_unresolved ? 'text-[#E56B75] border-[#E56B75]/30 bg-[#E56B75]/10' : 'text-[#55C89A] border-[#55C89A]/30 bg-[#55C89A]/10'
                    }`}>
                      {disp.status}
                    </span>
                  </div>
                </div>

                <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 text-[#8F98A8]">
                  <div>Claimant: <strong className="text-[#F4F3EF] font-normal">{disp.claimant_name}</strong></div>
                  <div>Claim Amount: <strong className="font-mono text-[#F4F3EF]">INR {disp.claim_amount?.toLocaleString()}</strong></div>
                </div>

                <p className="text-xs text-[#8F98A8] font-light leading-relaxed p-3 rounded-lg bg-[#07090D] border border-[#202734]/60">
                  {disp.description}
                </p>
              </div>
            ))}
          </div>
        ) : (
          <p className="text-xs text-[#5F6877] font-mono py-2">
            No active or historical payment disputes lodged under Section 18 MSMED Act.
          </p>
        )}
      </div>

      {/* 2. MCA Filings & Auditor Disclosures */}
      <div className="space-y-4">
        <div className="flex items-baseline justify-between border-b border-[#202734] pb-3">
          <div>
            <span className="text-[11px] font-mono uppercase tracking-widest text-[#5F6877] block">
              Ministry of Corporate Affairs
            </span>
            <h4 className="font-serif text-2xl text-[#F4F3EF] font-normal">
              Statutory Filings & Auditor Signals
            </h4>
          </div>
          <a
            href="https://www.mca.gov.in/"
            target="_blank"
            rel="noreferrer"
            className="text-xs font-mono text-[#6757D9] hover:underline flex items-center gap-1"
          >
            MCA Portal <ExternalLink className="w-3 h-3" />
          </a>
        </div>

        {filings && filings.length > 0 ? (
          <div className="space-y-4">
            {filings.map((filing, idx) => (
              <div 
                key={idx}
                className="p-5 rounded-xl bg-[#0D1118] border border-[#202734] space-y-4 text-xs"
              >
                <div className="flex flex-col sm:flex-row sm:items-baseline justify-between gap-2 border-b border-[#202734] pb-2 font-mono">
                  <div className="flex items-center gap-3">
                    <span className="text-[#F4F3EF] font-medium">Form {filing.form_type} — {filing.financial_year}</span>
                    <span className="text-[#5F6877] text-[11px]">SRN: {filing.document_reference}</span>
                  </div>
                  <span className="text-[#5F6877]">Filed: {filing.filing_date}</span>
                </div>

                {/* Financial KPIs */}
                <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 text-xs font-mono">
                  <div>
                    <span className="text-[#5F6877] block text-[10px] uppercase">Revenue</span>
                    <span className="text-[#F4F3EF]">INR {filing.revenue_inr_cr || 0} Cr</span>
                  </div>
                  <div>
                    <span className="text-[#5F6877] block text-[10px] uppercase">Net Profit / Loss</span>
                    <span className={filing.net_profit_inr_cr < 0 ? 'text-[#E56B75]' : 'text-[#55C89A]'}>
                      INR {filing.net_profit_inr_cr || 0} Cr
                    </span>
                  </div>
                  <div>
                    <span className="text-[#5F6877] block text-[10px] uppercase">Net Worth</span>
                    <span className={filing.net_worth_inr_cr < 0 ? 'text-[#E56B75]' : 'text-[#F4F3EF]'}>
                      INR {filing.net_worth_inr_cr || 0} Cr
                    </span>
                  </div>
                  <div>
                    <span className="text-[#5F6877] block text-[10px] uppercase">Bank Charges</span>
                    <span className="text-[#E7B85C]">{filing.active_charges_count || 0} Registered</span>
                  </div>
                </div>

                {/* Auditor Disclosure Snippet */}
                {filing.snippet && (
                  <div className="p-3.5 rounded-lg bg-[#07090D] border border-[#202734]/60 space-y-1 font-light">
                    <span className="text-[10px] font-mono text-[#5F6877] uppercase tracking-wider block">
                      Auditor Report Citation
                    </span>
                    <p className="text-xs text-[#8F98A8] italic leading-relaxed">
                      "{filing.snippet}"
                    </p>
                  </div>
                )}
              </div>
            ))}
          </div>
        ) : (
          <p className="text-xs text-[#5F6877] font-mono py-2">
            No annual statutory accounts filed in public registries.
          </p>
        )}
      </div>

    </div>
  );
}
