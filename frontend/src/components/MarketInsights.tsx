import React from 'react';
import { MarketStats } from '../types';
import { TrendingUp, DollarSign, Activity, PieChart, Globe } from 'lucide-react';

interface MarketInsightsProps {
  stats: MarketStats | null;
  activeSource: string;
  onSelectSource: (src: string) => void;
}

export const MarketInsights: React.FC<MarketInsightsProps> = ({ stats, activeSource, onSelectSource }) => {
  if (!stats) return null;

  const formatCurrency = (val: number) => {
    if (val >= 1_000_000) return `$${(val / 1_000_000).toFixed(2)}M`;
    if (val >= 1_000) return `$${(val / 1_000).toFixed(0)}k`;
    return `$${val.toLocaleString()}`;
  };

  return (
    <div className="mb-6 space-y-4">
      {/* Metric Cards Grid */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-3 sm:gap-4">
        {/* Total Listings */}
        <div className="p-4 rounded-2xl bg-slate-900/70 border border-slate-800/80 shadow-sm relative overflow-hidden group hover:border-slate-700 transition-all">
          <div className="absolute top-0 right-0 w-24 h-24 bg-emerald-500/5 rounded-full blur-xl group-hover:bg-emerald-500/10 transition-all" />
          <div className="flex items-center justify-between text-slate-400 text-xs font-semibold uppercase tracking-wider mb-1">
            <span>Aggregated Deals</span>
            <Activity className="w-4 h-4 text-emerald-400" />
          </div>
          <div className="text-2xl font-bold text-white tracking-tight">
            {stats.total_listings}
            <span className="text-xs font-normal text-slate-400 ml-2">Live Listings</span>
          </div>
        </div>

        {/* Avg Asking Price */}
        <div className="p-4 rounded-2xl bg-slate-900/70 border border-slate-800/80 shadow-sm relative overflow-hidden group hover:border-slate-700 transition-all">
          <div className="absolute top-0 right-0 w-24 h-24 bg-teal-500/5 rounded-full blur-xl group-hover:bg-teal-500/10 transition-all" />
          <div className="flex items-center justify-between text-slate-400 text-xs font-semibold uppercase tracking-wider mb-1">
            <span>Avg Asking Price</span>
            <DollarSign className="w-4 h-4 text-teal-400" />
          </div>
          <div className="text-2xl font-bold text-white tracking-tight">
            {formatCurrency(stats.avg_asking_price)}
            <span className="text-xs font-normal text-slate-400 ml-2">
              (Med. {formatCurrency(stats.median_asking_price)})
            </span>
          </div>
        </div>

        {/* Avg Cash Flow */}
        <div className="p-4 rounded-2xl bg-slate-900/70 border border-slate-800/80 shadow-sm relative overflow-hidden group hover:border-slate-700 transition-all">
          <div className="absolute top-0 right-0 w-24 h-24 bg-cyan-500/5 rounded-full blur-xl group-hover:bg-cyan-500/10 transition-all" />
          <div className="flex items-center justify-between text-slate-400 text-xs font-semibold uppercase tracking-wider mb-1">
            <span>Avg Cash Flow (SDE)</span>
            <TrendingUp className="w-4 h-4 text-cyan-400" />
          </div>
          <div className="text-2xl font-bold text-emerald-400 tracking-tight">
            {formatCurrency(stats.avg_cash_flow)}
            <span className="text-xs font-normal text-slate-400 ml-2">/ year</span>
          </div>
        </div>

        {/* Avg Multiple */}
        <div className="p-4 rounded-2xl bg-slate-900/70 border border-slate-800/80 shadow-sm relative overflow-hidden group hover:border-slate-700 transition-all">
          <div className="absolute top-0 right-0 w-24 h-24 bg-purple-500/5 rounded-full blur-xl group-hover:bg-purple-500/10 transition-all" />
          <div className="flex items-center justify-between text-slate-400 text-xs font-semibold uppercase tracking-wider mb-1">
            <span>Avg Cash Flow Multiple</span>
            <PieChart className="w-4 h-4 text-purple-400" />
          </div>
          <div className="text-2xl font-bold text-purple-300 tracking-tight">
            {stats.avg_multiple ? `${stats.avg_multiple}x` : '3.2x'}
            <span className="text-xs font-normal text-slate-400 ml-2">SDE Multiple</span>
          </div>
        </div>
      </div>

      {/* Source Market Breakdown Pills */}
      <div className="flex items-center gap-2 overflow-x-auto pb-1 text-xs no-scrollbar">
        <span className="text-slate-400 font-medium flex items-center gap-1 shrink-0 mr-1">
          <Globe className="w-3.5 h-3.5 text-slate-500" /> Marketplaces:
        </span>
        <button
          onClick={() => onSelectSource('All')}
          className={`px-3 py-1.5 rounded-lg font-medium transition-all shrink-0 ${
            activeSource === 'All'
              ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/40'
              : 'bg-slate-900 text-slate-400 hover:text-slate-200 border border-slate-800'
          }`}
        >
          All Sources ({stats.total_listings})
        </button>
        {Object.entries(stats.source_distribution).map(([src, count]) => (
          <button
            key={src}
            onClick={() => onSelectSource(src)}
            className={`px-3 py-1.5 rounded-lg font-medium transition-all shrink-0 flex items-center gap-1.5 ${
              activeSource === src
                ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/40'
                : 'bg-slate-900 text-slate-400 hover:text-slate-200 border border-slate-800'
            }`}
          >
            <span>{src}</span>
            <span className="px-1.5 py-0.2 rounded-full text-[10px] bg-slate-800 text-slate-300">
              {count}
            </span>
          </button>
        ))}
      </div>
    </div>
  );
};
