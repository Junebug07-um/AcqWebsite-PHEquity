import React from 'react';
import { Search, Sparkles, Bookmark, Calculator, RefreshCw, Layers, Clock, CheckCircle2 } from 'lucide-react';
import { SchedulerStatus } from '../types';

interface NavbarProps {
  searchQuery: string;
  onSearchChange: (q: string) => void;
  onOpenScraper: () => void;
  onOpenCalculator: () => void;
  onOpenWatchlist: () => void;
  watchlistCount: number;
  totalListings: number;
  schedulerStatus?: SchedulerStatus | null;
}

export const Navbar: React.FC<NavbarProps> = ({
  searchQuery,
  onSearchChange,
  onOpenScraper,
  onOpenCalculator,
  onOpenWatchlist,
  watchlistCount,
  totalListings,
  schedulerStatus,
}) => {
  const formatTime = (isoString?: string | null) => {
    if (!isoString) return 'Pending first run';
    try {
      const d = new Date(isoString);
      return d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    } catch {
      return isoString;
    }
  };

  return (
    <header className="sticky top-0 z-40 bg-slate-950/85 backdrop-blur-md border-b border-slate-800/80 px-4 lg:px-8 py-3.5 transition-all">
      <div className="max-w-7xl mx-auto flex items-center justify-between gap-4">
        {/* Logo & Brand */}
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-emerald-600 via-teal-500 to-cyan-400 p-[2px] shadow-lg shadow-emerald-950/50 flex items-center justify-center">
            <div className="w-full h-full bg-slate-950 rounded-[10px] flex items-center justify-center">
              <Layers className="w-5 h-5 text-emerald-400" />
            </div>
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="text-xl font-extrabold tracking-tight bg-gradient-to-r from-white via-slate-200 to-slate-400 bg-clip-text text-transparent">
                DealFlow<span className="text-emerald-400">Hub</span>
              </span>
              <span className="hidden sm:inline-block text-[11px] font-semibold uppercase tracking-wider px-2 py-0.5 rounded-full bg-emerald-950/80 text-emerald-400 border border-emerald-800/50">
                Aggregator
              </span>
            </div>
            {/* Daily Auto-Sync Status Badge */}
            <div className="flex items-center gap-1.5 text-[11px] text-slate-400 mt-0.5">
              <span className="relative flex h-2 w-2">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
                <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
              </span>
              <span className="text-emerald-400 font-semibold">Auto-updates Daily</span>
              {schedulerStatus?.next_run_at && (
                <span className="text-slate-500 hidden md:inline">
                  • Next sync at {formatTime(schedulerStatus.next_run_at)}
                </span>
              )}
            </div>
          </div>
        </div>

        {/* Search Bar */}
        <div className="flex-1 max-w-xl hidden md:block">
          <div className="relative">
            <Search className="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
            <input
              type="text"
              placeholder="Search by keywords (e.g. 'SaaS', 'Car Wash', 'Dallas', 'HVAC', 'Shopify')..."
              value={searchQuery}
              onChange={(e) => onSearchChange(e.target.value)}
              className="w-full pl-10 pr-4 py-2 bg-slate-900/90 border border-slate-700/80 rounded-xl text-sm text-slate-100 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-emerald-500/50 focus:border-emerald-500 transition-all shadow-inner"
            />
            {searchQuery && (
              <button
                onClick={() => onSearchChange('')}
                className="absolute right-3 top-1/2 -translate-y-1/2 text-xs text-slate-400 hover:text-slate-200"
              >
                Clear
              </button>
            )}
          </div>
        </div>

        {/* Action Controls */}
        <div className="flex items-center gap-2 sm:gap-3">
          {/* Scrape Trigger Button */}
          <button
            onClick={onOpenScraper}
            className="flex items-center gap-2 px-3.5 py-2 rounded-xl bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-500 hover:to-teal-500 text-white text-xs sm:text-sm font-semibold shadow-lg shadow-emerald-900/30 active:scale-95 transition-all border border-emerald-400/20"
          >
            <Sparkles className="w-4 h-4 animate-pulse text-emerald-200" />
            <span>Scrape Web</span>
          </button>

          {/* Acquisition Calculator */}
          <button
            onClick={onOpenCalculator}
            title="Deal Valuation & Loan Calculator"
            className="flex items-center gap-1.5 px-3 py-2 rounded-xl bg-slate-900 hover:bg-slate-800 text-slate-300 hover:text-slate-100 text-xs sm:text-sm font-medium border border-slate-700/80 transition-all"
          >
            <Calculator className="w-4 h-4 text-emerald-400" />
            <span className="hidden lg:inline">Valuation Calc</span>
          </button>

          {/* Watchlist */}
          <button
            onClick={onOpenWatchlist}
            className="relative flex items-center gap-1.5 px-3 py-2 rounded-xl bg-slate-900 hover:bg-slate-800 text-slate-300 hover:text-slate-100 text-xs sm:text-sm font-medium border border-slate-700/80 transition-all"
          >
            <Bookmark className={`w-4 h-4 ${watchlistCount > 0 ? 'text-amber-400 fill-amber-400' : 'text-slate-400'}`} />
            <span className="hidden sm:inline">Saved</span>
            {watchlistCount > 0 && (
              <span className="ml-1 px-1.5 py-0.2 rounded-full text-[11px] font-bold bg-amber-500/20 text-amber-300 border border-amber-500/40">
                {watchlistCount}
              </span>
            )}
          </button>
        </div>
      </div>

      {/* Mobile Search Bar */}
      <div className="mt-3 md:hidden">
        <div className="relative">
          <Search className="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
          <input
            type="text"
            placeholder="Search businesses..."
            value={searchQuery}
            onChange={(e) => onSearchChange(e.target.value)}
            className="w-full pl-10 pr-4 py-2 bg-slate-900 border border-slate-700/80 rounded-xl text-sm text-slate-100 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-emerald-500/50"
          />
        </div>
      </div>
    </header>
  );
};
