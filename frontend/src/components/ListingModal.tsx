import React, { useState } from 'react';
import { BusinessListing } from '../types';
import {
  X,
  ExternalLink,
  DollarSign,
  TrendingUp,
  Building,
  MapPin,
  Calendar,
  Users,
  CheckCircle2,
  XCircle,
  HelpCircle,
  Bookmark,
  Share2,
  Calculator,
  Globe,
} from 'lucide-react';

interface ListingModalProps {
  listing: BusinessListing | null;
  onClose: () => void;
  isSaved: boolean;
  onToggleSave: (id: string, e: React.MouseEvent) => void;
  onOpenCalculatorForDeal: (listing: BusinessListing) => void;
}

export const ListingModal: React.FC<ListingModalProps> = ({
  listing,
  onClose,
  isSaved,
  onToggleSave,
  onOpenCalculatorForDeal,
}) => {
  if (!listing) return null;

  const [copied, setCopied] = useState(false);

  const formatMoney = (val: number | null) => {
    if (val === null || val === undefined) return 'Undisclosed';
    return `$${val.toLocaleString()}`;
  };

  const handleShare = () => {
    navigator.clipboard.writeText(listing.source_url);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  // Quick SBA estimate
  const downPayment = (listing.asking_price || 0) * 0.1; // 10%
  const loanAmount = (listing.asking_price || 0) * 0.9;
  const annualDebtService = loanAmount * 0.145;
  const netCashFlowAfterDebt = (listing.cash_flow || 0) - annualDebtService;
  const cashOnCashROI = downPayment > 0 ? (netCashFlowAfterDebt / downPayment) * 100 : 0;

  // Extract domain for display
  let domain = 'marketplace';
  try {
    const parsed = new URL(listing.source_url);
    domain = parsed.hostname.replace('www.', '');
  } catch (e) {}

  return (
    <div className="fixed inset-0 z-50 overflow-y-auto bg-black/80 backdrop-blur-md flex items-center justify-center p-3 sm:p-6 animate-fadeIn">
      <div
        className="relative w-full max-w-4xl bg-slate-900 border border-slate-700/80 rounded-3xl overflow-hidden shadow-2xl my-8 max-h-[90vh] flex flex-col"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header Bar */}
        <div className="flex items-center justify-between px-6 py-4 border-b border-slate-800 bg-slate-950/60 shrink-0">
          <div className="flex items-center gap-2">
            <span className="text-xs font-bold px-3 py-1 rounded-full bg-emerald-950 text-emerald-400 border border-emerald-800/60 flex items-center gap-1.5">
              <Globe className="w-3.5 h-3.5" />
              {listing.source}
            </span>
            <span className="text-xs text-slate-400 font-medium truncate max-w-[200px]">
              {domain}
            </span>
          </div>

          <div className="flex items-center gap-2">
            <button
              onClick={handleShare}
              className="p-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 transition-all text-xs flex items-center gap-1.5"
            >
              <Share2 className="w-4 h-4" />
              <span>{copied ? 'Copied!' : 'Share'}</span>
            </button>
            <button
              onClick={(e) => onToggleSave(listing.id, e)}
              className="p-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 transition-all"
            >
              <Bookmark
                className={`w-4 h-4 ${isSaved ? 'text-amber-400 fill-amber-400' : 'text-slate-400'}`}
              />
            </button>
            <button
              onClick={onClose}
              className="p-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 transition-all"
            >
              <X className="w-5 h-5" />
            </button>
          </div>
        </div>

        {/* Scrollable Content */}
        <div className="overflow-y-auto p-6 space-y-6 flex-1">
          {/* Main Title & Tagline */}
          <div>
            <div className="flex flex-wrap items-center gap-2 mb-2 text-xs font-semibold text-emerald-400">
              <span>{listing.category}</span>
              {listing.sub_category && (
                <>
                  <span>•</span>
                  <span className="text-slate-400">{listing.sub_category}</span>
                </>
              )}
            </div>
            <h1 className="text-xl sm:text-2xl font-extrabold text-white tracking-tight leading-snug">
              {listing.title}
            </h1>
            <div className="mt-2 flex items-center gap-4 text-xs text-slate-400">
              <span className="flex items-center gap-1">
                <MapPin className="w-3.5 h-3.5 text-emerald-400" />
                {listing.location}
              </span>
              {listing.established_year && (
                <span className="flex items-center gap-1">
                  <Calendar className="w-3.5 h-3.5 text-slate-400" />
                  Established {listing.established_year}
                </span>
              )}
              {listing.employees !== null && listing.employees !== undefined && (
                <span className="flex items-center gap-1">
                  <Users className="w-3.5 h-3.5 text-slate-400" />
                  {listing.employees} Employees
                </span>
              )}
            </div>
          </div>

          {/* Key Financial Cards */}
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
            <div className="p-4 rounded-2xl bg-slate-950/80 border border-slate-800">
              <span className="text-[11px] font-bold text-slate-400 uppercase tracking-wider block">
                Asking Price
              </span>
              <span className="text-xl font-extrabold text-white block mt-1">
                {formatMoney(listing.asking_price)}
              </span>
            </div>

            <div className="p-4 rounded-2xl bg-emerald-950/40 border border-emerald-800/40">
              <span className="text-[11px] font-bold text-emerald-400 uppercase tracking-wider block">
                Cash Flow (SDE)
              </span>
              <span className="text-xl font-extrabold text-emerald-300 block mt-1">
                {formatMoney(listing.cash_flow)}
              </span>
            </div>

            <div className="p-4 rounded-2xl bg-slate-950/80 border border-slate-800">
              <span className="text-[11px] font-bold text-slate-400 uppercase tracking-wider block">
                Gross Revenue
              </span>
              <span className="text-xl font-extrabold text-slate-200 block mt-1">
                {formatMoney(listing.gross_revenue)}
              </span>
            </div>

            <div className="p-4 rounded-2xl bg-purple-950/40 border border-purple-800/40">
              <span className="text-[11px] font-bold text-purple-400 uppercase tracking-wider block">
                Valuation Multiple
              </span>
              <span className="text-xl font-extrabold text-purple-300 block mt-1">
                {listing.price_to_cashflow_multiple
                  ? `${listing.price_to_cashflow_multiple}x SDE`
                  : 'N/A'}
              </span>
            </div>
          </div>

          {/* Quick Acquisition Simulation Box */}
          {listing.asking_price && listing.cash_flow && (
            <div className="p-4 sm:p-5 rounded-2xl bg-gradient-to-r from-emerald-950/30 to-teal-950/30 border border-emerald-800/40">
              <div className="flex items-center justify-between mb-3">
                <div className="flex items-center gap-2">
                  <Calculator className="w-4 h-4 text-emerald-400" />
                  <h3 className="text-sm font-bold text-emerald-200">
                    SBA 7(a) Acquisition Scenario (10% Down)
                  </h3>
                </div>
                <button
                  onClick={() => onOpenCalculatorForDeal(listing)}
                  className="text-xs font-semibold text-emerald-400 hover:text-emerald-300 underline"
                >
                  Open Full Calculator →
                </button>
              </div>

              <div className="grid grid-cols-3 gap-3 text-xs">
                <div>
                  <span className="text-slate-400 block text-[11px]">Down Payment (10%)</span>
                  <span className="font-bold text-slate-100 text-sm">{formatMoney(downPayment)}</span>
                </div>
                <div>
                  <span className="text-slate-400 block text-[11px]">Net Cash Flow After Debt</span>
                  <span className="font-bold text-emerald-400 text-sm">
                    {formatMoney(Math.max(0, netCashFlowAfterDebt))}/yr
                  </span>
                </div>
                <div>
                  <span className="text-slate-400 block text-[11px]">Est. Cash-on-Cash ROI</span>
                  <span className="font-bold text-teal-300 text-sm">
                    {cashOnCashROI > 0 ? `${cashOnCashROI.toFixed(1)}%` : 'N/A'}
                  </span>
                </div>
              </div>
            </div>
          )}

          {/* Business Description */}
          <div>
            <h3 className="text-sm font-bold text-slate-200 uppercase tracking-wider mb-2">
              Business Overview
            </h3>
            <p className="text-sm text-slate-300 leading-relaxed whitespace-pre-line bg-slate-950/50 p-4 rounded-2xl border border-slate-800">
              {listing.description}
            </p>
          </div>

          {/* Source Link Banner */}
          <div className="p-4 rounded-2xl bg-slate-950/80 border border-slate-800 flex items-center justify-between">
            <div className="text-xs">
              <span className="text-slate-400 block">Original Marketplace Source:</span>
              <span className="text-emerald-400 font-mono truncate max-w-md block mt-0.5">
                {listing.source_url}
              </span>
            </div>
            <a
              href={listing.source_url}
              target="_blank"
              rel="noopener noreferrer"
              className="flex items-center gap-1.5 px-4 py-2 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-bold shrink-0 transition-all"
            >
              <span>Visit Link</span>
              <ExternalLink className="w-3.5 h-3.5" />
            </a>
          </div>
        </div>

        {/* Footer Action */}
        <div className="p-4 sm:p-5 border-t border-slate-800 bg-slate-950 flex items-center justify-between gap-4 shrink-0">
          <button
            onClick={onClose}
            className="px-4 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 text-sm font-semibold transition-all"
          >
            Close
          </button>

          <a
            href={listing.source_url}
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center gap-2 px-6 py-2.5 rounded-xl bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-500 hover:to-teal-500 text-white text-sm font-bold shadow-lg shadow-emerald-950 transition-all hover:scale-[1.02] active:scale-98"
          >
            <span>Open Listing on {listing.source}</span>
            <ExternalLink className="w-4 h-4" />
          </a>
        </div>
      </div>
    </div>
  );
};
