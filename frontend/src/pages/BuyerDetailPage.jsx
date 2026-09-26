import React, { useState, useEffect } from 'react';
import { ArrowLeft, Clock, AlertTriangle, Layers, Calendar, Scale, ShieldCheck } from 'lucide-react';
import { 
  getBuyerDetail, getBuyerGraph, getBuyerTimeline, 
  getBuyerDisputes, getBuyerFilings, getBuyerInsolvency 
} from '../services/api';
import CommercialTermsCard from '../components/CommercialTermsCard';
import PaymentAnalyticsView from '../components/PaymentAnalyticsView';
import EntityGraphView from '../components/EntityGraphView';
import TimelineView from '../components/TimelineView';
import PublicEvidenceView from '../components/PublicEvidenceView';

export default function BuyerDetailPage({ buyerId, onBack, onSelectBuyer }) {
  const [buyer, setBuyer] = useState(null);
  const [graphData, setGraphData] = useState(null);
  const [timelineEvents, setTimelineEvents] = useState([]);
  const [disputes, setDisputes] = useState([]);
  const [filings, setFilings] = useState([]);
  const [insolvencies, setInsolvencies] = useState([]);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('commercial');

  useEffect(() => {
    async function loadData() {
      if (!buyerId) return;
      setLoading(true);
      try {
        const [bData, gData, tData, dData, fData, iData] = await Promise.all([
          getBuyerDetail(buyerId),
          getBuyerGraph(buyerId),
          getBuyerTimeline(buyerId),
          getBuyerDisputes(buyerId),
          getBuyerFilings(buyerId),
          getBuyerInsolvency(buyerId)
        ]);

        setBuyer(bData);
        setGraphData(gData);
        setTimelineEvents(tData);
        setDisputes(dData);
        setFilings(fData);
        setInsolvencies(iData);
      } catch (err) {
        console.error("Failed to load dossier:", err);
      } finally {
        setLoading(false);
      }
    }
    loadData();
  }, [buyerId]);

  if (loading) {
    return (
      <div className="max-w-5xl mx-auto px-6 py-28 text-center space-y-4">
        <div className="w-8 h-8 border border-[#6757D9] border-t-transparent rounded-full animate-spin mx-auto"></div>
        <p className="text-xs font-mono text-[#8F98A8]">Compiling intelligence dossier...</p>
      </div>
    );
  }

  if (!buyer) {
    return (
      <div className="max-w-5xl mx-auto px-6 py-24 text-center space-y-4">
        <p className="text-sm text-[#8F98A8]">Buyer profile not found.</p>
        <button onClick={onBack} className="px-4 py-2 bg-[#121824] text-xs text-[#F4F3EF] rounded">
          Return to Overview
        </button>
      </div>
    );
  }

  const pa = buyer.payment_analytics || {};

  return (
    <div className="max-w-6xl mx-auto px-6 py-12 space-y-12 animate-fadeIn dossier-glow">
      
      {/* Top Header Navigation */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-[#202734] pb-4 text-xs font-mono">
        <button
          onClick={onBack}
          className="inline-flex items-center gap-1.5 text-[#8F98A8] hover:text-[#F4F3EF] transition-colors"
        >
          <ArrowLeft className="w-3.5 h-3.5" />
          <span>Back to Search</span>
        </button>

        <div className="flex items-center gap-3 text-[#5F6877]">
          {buyer.is_demo && (
            <span className="px-2 py-0.5 rounded bg-[#121824] border border-[#202734] text-[#8F98A8]">
              {buyer.demo_tag}
            </span>
          )}
          <span>{buyer.last_verified}</span>
        </div>
      </div>

      {/* Dominant Editorial Profile Header */}
      <div className="space-y-6">
        
        {/* Category & Status */}
        <div className="flex flex-wrap items-center gap-3 text-xs font-mono text-[#8F98A8]">
          <span className={`px-2 py-0.5 rounded border text-[11px] ${
            buyer.company_status === 'Active' 
              ? 'text-[#55C89A] border-[#55C89A]/30 bg-[#55C89A]/10' 
              : 'text-[#E56B75] border-[#E56B75]/30 bg-[#E56B75]/10'
          }`}>
            {buyer.company_status}
          </span>
          <span>{buyer.industry}</span>
          <span>•</span>
          <span>{buyer.company_class || 'Corporate Body'}</span>
          <span>•</span>
          <span>{buyer.state}</span>
        </div>

        {/* Dominant Buyer Name */}
        <div>
          <h1 className="font-serif text-4xl sm:text-6xl text-[#F4F3EF] font-normal tracking-tight leading-[1.08]">
            {buyer.legal_name}
          </h1>
          {buyer.trade_name && (
            <p className="text-sm text-[#8F98A8] mt-1.5 font-light">
              Known commercially as <strong className="text-[#F4F3EF] font-medium">"{buyer.trade_name}"</strong>
            </p>
          )}
        </div>

        {/* Previous Legal Names (if any) */}
        {buyer.previous_names && buyer.previous_names.length > 0 && (
          <div className="text-xs text-[#E7B85C] flex items-center gap-2 font-mono">
            <span>Former Legal Registration:</span>
            <span className="underline">{buyer.previous_names.join(', ')}</span>
          </div>
        )}

        {/* Context Note */}
        {buyer.demo_scenario && (
          <p className="text-xs text-[#8F98A8] leading-relaxed max-w-4xl font-light">
            <strong className="text-[#F4F3EF] font-medium">Background:</strong> {buyer.demo_scenario}
          </p>
        )}

        {/* Technical Metadata Row */}
        <div className="flex flex-wrap items-center gap-x-8 gap-y-2 text-xs font-mono text-[#8F98A8] pt-2 border-t border-[#202734]/50">
          <div><span className="text-[#5F6877]">CIN:</span> <span className="text-[#F4F3EF]">{buyer.cin || 'Not Registered'}</span></div>
          <div><span className="text-[#5F6877]">GSTIN:</span> <span className="text-[#F4F3EF]">{buyer.gstin || 'Not Registered'}</span></div>
          <div><span className="text-[#5F6877]">PAN:</span> <span className="text-[#F4F3EF]">{buyer.pan || 'N/A'}</span></div>
          <div><span className="text-[#5F6877]">Incorporation:</span> <span className="text-[#F4F3EF]">{buyer.incorporation_date || 'N/A'}</span></div>
          <div><span className="text-[#5F6877]">Registered Office:</span> <span className="text-[#F4F3EF]">{buyer.city}, {buyer.state}</span></div>
        </div>

        {/* Directors Strip */}
        {buyer.directors && buyer.directors.length > 0 && (
          <div className="flex flex-wrap items-center gap-2 text-xs font-mono text-[#8F98A8] pt-1">
            <span className="text-[#5F6877]">Directors:</span>
            {buyer.directors.map((d, i) => (
              <span key={i} className="text-[#F4F3EF]">
                {d.name} {d.din ? `(${d.din})` : ''}{i < buyer.directors.length - 1 ? ' •' : ''}
              </span>
            ))}
          </div>
        )}

      </div>

      {/* Major Dominant Metrics Strip (As requested in prompt) */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-8 py-8 border-y border-[#202734]">
        
        <div className="space-y-1">
          <span className="text-xs font-mono uppercase tracking-wider text-[#5F6877] block">
            Expected Payment
          </span>
          <div className="font-mono text-3xl sm:text-4xl font-light text-signature-gradient tracking-tight">
            {buyer.commercial_recommendation?.expected_payment_window || 'Uncertain'}
          </div>
          <span className="text-xs text-[#8F98A8] block pt-1">
            Turnaround: <strong className="text-[#F4F3EF] font-mono">{pa.average_payment_days || 0}d</strong> average
          </span>
        </div>

        <div className="space-y-1 sm:border-l sm:border-[#202734] sm:pl-8">
          <span className="text-xs font-mono uppercase tracking-wider text-[#5F6877] block">
            Historical Delay
          </span>
          <div className={`font-mono text-3xl sm:text-4xl font-light tracking-tight ${
            (pa.average_delay_days || 0) > 20 ? 'text-[#E56B75]' : 
            (pa.average_delay_days || 0) > 5 ? 'text-[#E7B85C]' : 'text-[#55C89A]'
          }`}>
            {(pa.average_delay_days || 0) > 0 ? `+${pa.average_delay_days}` : pa.average_delay_days || 0}
            <span className="text-lg font-normal text-[#5F6877]"> days</span>
          </div>
          <span className="text-xs text-[#8F98A8] block pt-1">
            Max observed delay: <strong className="text-[#F4F3EF] font-mono">{pa.maximum_delay_days || 0}d</strong>
          </span>
        </div>

        <div className="space-y-1 sm:border-l sm:border-[#202734] sm:pl-8">
          <span className="text-xs font-mono uppercase tracking-wider text-[#5F6877] block">
            Late-Payment Rate
          </span>
          <div className={`font-mono text-3xl sm:text-4xl font-light tracking-tight ${
            (pa.late_payment_percentage || 0) > 50 ? 'text-[#E56B75]' : 
            (pa.late_payment_percentage || 0) > 20 ? 'text-[#E7B85C]' : 'text-[#55C89A]'
          }`}>
            {pa.late_payment_percentage || 0}%
          </div>
          <span className="text-xs text-[#8F98A8] block pt-1">
            On-time settlement: <strong className="text-[#F4F3EF] font-mono">{pa.on_time_percentage || 0}%</strong>
          </span>
        </div>

      </div>

      {/* Commercial Terms Section */}
      <CommercialTermsCard recommendation={buyer.commercial_recommendation} />

      {/* Investigative Tabs */}
      <div className="space-y-8 pt-6">
        
        {/* Minimal Navigation Tabs */}
        <div className="flex flex-wrap items-center gap-6 border-b border-[#202734] text-xs font-medium pb-3">
          <button
            onClick={() => setActiveTab('commercial')}
            className={`transition-colors py-1 relative ${
              activeTab === 'commercial' 
                ? 'text-[#F4F3EF] font-semibold' 
                : 'text-[#8F98A8] hover:text-[#F4F3EF]'
            }`}
          >
            Payment Behaviour ({pa.invoice_count || 0})
            {activeTab === 'commercial' && (
              <span className="absolute -bottom-3 left-0 right-0 h-[1.5px] bg-signature-gradient"></span>
            )}
          </button>

          <button
            onClick={() => setActiveTab('graph')}
            className={`transition-colors py-1 relative ${
              activeTab === 'graph' 
                ? 'text-[#F4F3EF] font-semibold' 
                : 'text-[#8F98A8] hover:text-[#F4F3EF]'
            }`}
          >
            Corporate Ownership ({buyer.related_entities_count})
            {activeTab === 'graph' && (
              <span className="absolute -bottom-3 left-0 right-0 h-[1.5px] bg-signature-gradient"></span>
            )}
          </button>

          <button
            onClick={() => setActiveTab('evidence')}
            className={`transition-colors py-1 relative ${
              activeTab === 'evidence' 
                ? 'text-[#F4F3EF] font-semibold' 
                : 'text-[#8F98A8] hover:text-[#F4F3EF]'
            }`}
          >
            Public Evidence ({buyer.disputes_count} Disputes • {buyer.filing_signals_count} Filings)
            {activeTab === 'evidence' && (
              <span className="absolute -bottom-3 left-0 right-0 h-[1.5px] bg-signature-gradient"></span>
            )}
          </button>

          <button
            onClick={() => setActiveTab('timeline')}
            className={`transition-colors py-1 relative ${
              activeTab === 'timeline' 
                ? 'text-[#F4F3EF] font-semibold' 
                : 'text-[#8F98A8] hover:text-[#F4F3EF]'
            }`}
          >
            Evidence Timeline ({timelineEvents.length})
            {activeTab === 'timeline' && (
              <span className="absolute -bottom-3 left-0 right-0 h-[1.5px] bg-signature-gradient"></span>
            )}
          </button>
        </div>

        {/* Tab Views */}
        <div>
          {activeTab === 'commercial' && (
            <PaymentAnalyticsView paymentAnalytics={buyer.payment_analytics} />
          )}

          {activeTab === 'graph' && (
            <EntityGraphView graphData={graphData} onSelectEntity={onSelectBuyer} />
          )}

          {activeTab === 'evidence' && (
            <PublicEvidenceView 
              disputes={disputes} 
              filings={filings} 
              insolvencyRecords={insolvencies} 
              buyerName={buyer.legal_name} 
            />
          )}

          {activeTab === 'timeline' && (
            <TimelineView timelineEvents={timelineEvents} />
          )}
        </div>

      </div>

    </div>
  );
}
