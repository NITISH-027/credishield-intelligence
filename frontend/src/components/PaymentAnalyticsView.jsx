import React from 'react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell } from 'recharts';
import { Clock } from 'lucide-react';

export default function PaymentAnalyticsView({ paymentAnalytics }) {
  if (!paymentAnalytics) return null;

  const isThinFile = paymentAnalytics.invoice_count === 0;

  // Chart data with refined, muted palette
  const chartData = [
    { name: 'On Time (<= 0d)', count: paymentAnalytics.delay_distribution?.on_time || 0, fill: '#55C89A' },
    { name: '1–15 Days', count: paymentAnalytics.delay_distribution?.['1_15_days'] || 0, fill: '#D58BAA' },
    { name: '16–30 Days', count: paymentAnalytics.delay_distribution?.['16_30_days'] || 0, fill: '#E7B85C' },
    { name: '31–60 Days', count: paymentAnalytics.delay_distribution?.['31_60_days'] || 0, fill: '#E56B75' },
    { name: '> 60 Days', count: paymentAnalytics.delay_distribution?.over_60_days || 0, fill: '#C04B55' },
  ];

  const getStatusColor = (status) => {
    if (status === 'PAID') return 'text-[#55C89A] border-[#55C89A]/30 bg-[#55C89A]/10';
    if (status === 'OVERDUE') return 'text-[#E56B75] border-[#E56B75]/30 bg-[#E56B75]/10';
    return 'text-[#E7B85C] border-[#E7B85C]/30 bg-[#E7B85C]/10';
  };

  return (
    <div className="space-y-10">
      
      {/* Overview & Distribution Strip */}
      <div className="space-y-4">
        <div className="flex flex-col sm:flex-row sm:items-baseline justify-between gap-2 border-b border-[#202734] pb-3">
          <div>
            <span className="text-[11px] font-mono uppercase tracking-widest text-[#5F6877] block">
              Receivables Ledger
            </span>
            <h3 className="font-serif text-2xl text-[#F4F3EF] font-normal">
              Payment Turnaround & Delay Distribution
            </h3>
          </div>
          <div className="flex items-center gap-3 text-xs font-mono text-[#8F98A8]">
            <span>Segment: <strong className="text-[#F4F3EF]">{paymentAnalytics.segment.replace('_', ' ')}</strong></span>
            <span>•</span>
            <span>Trend: <strong className="text-[#F4F3EF]">{paymentAnalytics.recent_delay_trend}</strong></span>
          </div>
        </div>

        {isThinFile ? (
          <div className="p-12 text-center border border-[#202734] rounded-2xl bg-[#0D1118] space-y-3">
            <Clock className="w-6 h-6 text-[#5F6877] mx-auto" />
            <h4 className="text-sm font-medium text-[#F4F3EF]">Zero Invoices Observed in Public Records</h4>
            <p className="text-xs text-[#8F98A8] max-w-md mx-auto leading-relaxed">
              This buyer does not have historical receivables indexed in public databases. Missing data is preserved as unverified rather than assumed negative.
            </p>
          </div>
        ) : (
          <div className="p-6 rounded-2xl bg-[#0D1118] border border-[#202734] space-y-4">
            <div className="flex items-center justify-between text-xs font-mono text-[#8F98A8]">
              <span>Delay Distribution Bucket</span>
              <span>Observed Invoices: {paymentAnalytics.invoice_count}</span>
            </div>
            
            <div className="h-44 w-full">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={chartData} margin={{ top: 10, right: 10, left: -25, bottom: 0 }}>
                  <XAxis dataKey="name" stroke="#5F6877" fontSize={11} tickLine={false} fontFamily="IBM Plex Mono" />
                  <YAxis stroke="#5F6877" fontSize={11} tickLine={false} allowDecimals={false} fontFamily="IBM Plex Mono" />
                  <Tooltip 
                    contentStyle={{ backgroundColor: '#0D1118', borderColor: '#202734', borderRadius: '8px', fontSize: '11px', fontFamily: 'IBM Plex Mono' }}
                    itemStyle={{ color: '#F4F3EF' }}
                  />
                  <Bar dataKey="count" radius={[3, 3, 0, 0]}>
                    {chartData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.fill} />
                    ))}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>
        )}
      </div>

      {/* Recent Ledger Invoices Table (Subtle dividers, non-boxed, spacious) */}
      {paymentAnalytics.recent_invoices && paymentAnalytics.recent_invoices.length > 0 && (
        <div className="space-y-4">
          <div className="flex items-baseline justify-between border-b border-[#202734] pb-3">
            <h4 className="font-serif text-xl text-[#F4F3EF] font-normal">
              Recent Trade Invoices
            </h4>
            <span className="text-xs font-mono text-[#5F6877]">Showing last 10 records</span>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs font-mono">
              <thead>
                <tr className="border-b border-[#202734] text-[#5F6877]">
                  <th className="py-3 px-2 font-normal">Invoice ID</th>
                  <th className="py-3 px-2 font-normal font-sans">Supplier Name</th>
                  <th className="py-3 px-2 font-normal">Amount (INR)</th>
                  <th className="py-3 px-2 font-normal">Issue Date</th>
                  <th className="py-3 px-2 font-normal">Due Date</th>
                  <th className="py-3 px-2 font-normal">Delay</th>
                  <th className="py-3 px-2 font-normal">Status</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-[#202734]/60">
                {paymentAnalytics.recent_invoices.map(inv => (
                  <tr key={inv.id} className="hover:bg-[#0D1118] transition-colors">
                    <td className="py-3.5 px-2 text-[#F4F3EF]">{inv.invoice_id}</td>
                    <td className="py-3.5 px-2 font-sans text-[#8F98A8]">{inv.supplier_name}</td>
                    <td className="py-3.5 px-2 text-[#F4F3EF]">INR {inv.invoice_amount?.toLocaleString()}</td>
                    <td className="py-3.5 px-2 text-[#5F6877]">{inv.issue_date}</td>
                    <td className="py-3.5 px-2 text-[#5F6877]">{inv.due_date}</td>
                    <td className="py-3.5 px-2">
                      <span className={
                        inv.delay_days === null ? 'text-[#5F6877]' :
                        inv.delay_days <= 0 ? 'text-[#55C89A]' :
                        inv.delay_days <= 15 ? 'text-[#D58BAA]' :
                        inv.delay_days <= 30 ? 'text-[#E7B85C]' : 'text-[#E56B75]'
                      }>
                        {inv.delay_days === null ? 'Pending' : (inv.delay_days > 0 ? `+${inv.delay_days}d` : `${inv.delay_days}d`)}
                      </span>
                    </td>
                    <td className="py-3.5 px-2">
                      <span className={`px-2 py-0.5 rounded border text-[10px] uppercase ${getStatusColor(inv.status)}`}>
                        {inv.status}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

    </div>
  );
}
