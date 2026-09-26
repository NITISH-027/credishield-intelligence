import React, { useState } from 'react';
import { X, ExternalLink } from 'lucide-react';

export default function TimelineView({ timelineEvents }) {
  const [activeModalEvent, setActiveModalEvent] = useState(null);

  if (!timelineEvents || timelineEvents.length === 0) {
    return (
      <div className="p-12 text-center text-[#5F6877] font-mono text-xs border border-[#202734] rounded-2xl bg-[#0D1118]">
        No chronological milestones recorded.
      </div>
    );
  }

  // Group events by year
  const eventsByYear = timelineEvents.reduce((acc, ev) => {
    acc[ev.year] = acc[ev.year] || [];
    acc[ev.year].push(ev);
    return acc;
  }, {});

  const years = Object.keys(eventsByYear).sort((a, b) => Number(a) - Number(b));

  const getSeverityAccent = (severity) => {
    switch (severity) {
      case 'CRITICAL':
        return 'text-[#E56B75] border-[#E56B75]/30 bg-[#E56B75]/10';
      case 'HIGH':
        return 'text-[#E7B85C] border-[#E7B85C]/30 bg-[#E7B85C]/10';
      case 'MEDIUM':
        return 'text-[#D58BAA] border-[#D58BAA]/30 bg-[#D58BAA]/10';
      default:
        return 'text-[#8F98A8] border-[#202734] bg-[#121824]';
    }
  };

  return (
    <div className="space-y-8">
      
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-baseline justify-between gap-2 border-b border-[#202734] pb-4">
        <div>
          <span className="text-[11px] font-mono uppercase tracking-widest text-[#5F6877] block">
            Chronological Archive
          </span>
          <h3 className="font-serif text-2xl text-[#F4F3EF] font-normal">
            Corporate & Dispute Timeline
          </h3>
        </div>
        <span className="text-xs font-mono text-[#5F6877]">
          {timelineEvents.length} Verified Milestones
        </span>
      </div>

      {/* Editorial Thin Rail Timeline */}
      <div className="relative pl-6 sm:pl-8 space-y-12 before:absolute before:left-2 sm:before:left-3 before:top-2 before:bottom-2 before:w-[1px] before:bg-[#202734]">
        
        {years.map(year => (
          <div key={year} className="relative space-y-4">
            
            {/* Year Stamp */}
            <div className="flex items-center gap-3 -ml-8 sm:-ml-9">
              <span className="w-2.5 h-2.5 rounded-full bg-[#07090D] border-2 border-[#6757D9]"></span>
              <span className="font-serif text-xl text-[#F4F3EF] font-light">
                {year}
              </span>
            </div>

            {/* Event Items for Year */}
            <div className="space-y-4 pl-2 sm:pl-4">
              {eventsByYear[year].map(ev => (
                <div
                  key={ev.id}
                  onClick={() => setActiveModalEvent(ev)}
                  className="group cursor-pointer p-5 rounded-xl bg-[#0D1118] hover:bg-[#121824] border border-[#202734] hover:border-[#2C3547] transition-all space-y-2"
                >
                  <div className="flex flex-col sm:flex-row sm:items-baseline justify-between gap-2">
                    <h4 className="font-medium text-sm text-[#F4F3EF] group-hover:text-white transition-colors">
                      {ev.title}
                    </h4>
                    <div className="flex items-center gap-2 text-xs font-mono">
                      <span className="text-[#5F6877]">{ev.date}</span>
                      <span className={`px-2 py-0.5 rounded text-[10px] uppercase border ${getSeverityAccent(ev.severity)}`}>
                        {ev.category}
                      </span>
                    </div>
                  </div>

                  <p className="text-xs text-[#8F98A8] font-light leading-relaxed">
                    {ev.description}
                  </p>

                  <div className="pt-2 border-t border-[#202734]/60 flex items-center justify-between text-[11px] font-mono text-[#5F6877]">
                    <span>Source: {ev.source}</span>
                    <span className="text-[#6757D9] group-hover:underline">Inspect Documentation →</span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        ))}

      </div>

      {/* Modal Inspector */}
      {activeModalEvent && (
        <div className="fixed inset-0 z-50 bg-[#07090D]/80 backdrop-blur-sm flex items-center justify-center p-4 animate-fadeIn">
          <div className="bg-[#0D1118] border border-[#202734] rounded-2xl max-w-lg w-full p-6 shadow-2xl space-y-5">
            
            <div className="flex items-start justify-between border-b border-[#202734] pb-4">
              <div className="space-y-1">
                <span className={`text-[10px] font-mono uppercase px-2 py-0.5 rounded border inline-block ${getSeverityAccent(activeModalEvent.severity)}`}>
                  {activeModalEvent.category} • {activeModalEvent.severity}
                </span>
                <h4 className="font-serif text-xl text-[#F4F3EF] font-normal leading-snug">
                  {activeModalEvent.title}
                </h4>
              </div>
              <button
                onClick={() => setActiveModalEvent(null)}
                className="text-[#5F6877] hover:text-[#F4F3EF] p-1 transition-colors"
              >
                <X className="w-4 h-4" />
              </button>
            </div>

            <div className="space-y-4 text-xs font-mono">
              <div className="grid grid-cols-2 gap-3 p-4 rounded-xl bg-[#07090D] border border-[#202734] text-[#8F98A8]">
                <div>
                  <span className="text-[#5F6877] block text-[10px] uppercase">Date</span>
                  <span className="text-[#F4F3EF]">{activeModalEvent.date}</span>
                </div>
                <div>
                  <span className="text-[#5F6877] block text-[10px] uppercase">Entity</span>
                  <span className="text-[#F4F3EF] truncate block">{activeModalEvent.entity_name}</span>
                </div>
                <div>
                  <span className="text-[#5F6877] block text-[10px] uppercase">Source</span>
                  <span className="text-[#F4F3EF]">{activeModalEvent.source}</span>
                </div>
                <div>
                  <span className="text-[#5F6877] block text-[10px] uppercase">Status</span>
                  <span className="text-[#F4F3EF]">{activeModalEvent.status || 'Verified'}</span>
                </div>
              </div>

              <div className="space-y-1.5 font-sans">
                <span className="text-[11px] font-mono text-[#5F6877] uppercase tracking-wider block">
                  Documentary Evidence
                </span>
                <p className="p-4 rounded-xl bg-[#07090D] border border-[#202734] text-[#8F98A8] text-xs leading-relaxed font-light">
                  {activeModalEvent.description}
                </p>
              </div>

              {activeModalEvent.amount && (
                <div className="flex items-center justify-between p-3 rounded-lg bg-[#07090D] border border-[#202734]">
                  <span className="text-[#8F98A8]">Claim Amount:</span>
                  <span className="font-bold text-[#F4F3EF]">INR {activeModalEvent.amount.toLocaleString()}</span>
                </div>
              )}
            </div>

            <div className="flex items-center justify-between pt-4 border-t border-[#202734]">
              {activeModalEvent.source_url ? (
                <a
                  href={activeModalEvent.source_url}
                  target="_blank"
                  rel="noreferrer"
                  className="text-xs text-[#6757D9] hover:underline flex items-center gap-1 font-mono"
                >
                  Public Source Record <ExternalLink className="w-3 h-3" />
                </a>
              ) : <span></span>}

              <button
                onClick={() => setActiveModalEvent(null)}
                className="px-4 py-1.5 bg-[#121824] hover:bg-[#202734] text-[#F4F3EF] text-xs rounded border border-[#202734] transition-colors"
              >
                Close
              </button>
            </div>

          </div>
        </div>
      )}

    </div>
  );
}
