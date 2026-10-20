import React from 'react';
import { BusinessListing } from '../types';
import { MapPin, DollarSign, TrendingUp, Bookmark, ExternalLink, ShieldCheck, Clock, Users, Building, Laptop, Trash2, CalendarCheck } from 'lucide-react';

interface ListingCardProps {
  listing: BusinessListing;
  isSaved: boolean;
  onToggleSave: (id: string, e: React.MouseEvent) => void;
  onDelete?: (id: string, e: React.MouseEvent) => void;
  onSelect: (listing: BusinessListing) => void;
}

export const ListingCard: React.FC<ListingCardProps> = ({
  listing,
  isSaved,
  onToggleSave,
  onDelete,
  onSelect,
}) => {
  const formatMoney = (amount: number | null) => {
    if (amount === null || amount === undefined) return 'Undisclosed';
    if (amount >= 1_000_000) return `$${(amount / 1_000_000).toFixed(2)}M`;
    return `$${amount.toLocaleString()}`;
  };

  const getFreshnessBadge = (isoDate?: string | null) => {
    if (!isoDate) return null;
    try {
      const diffDays = Math.floor((Date.now() - new Date(isoDate).getTime()) / (1000 * 60 * 60 * 24));
      if (diffDays <= 0) return 'Today';
      if (diffDays === 1) return '1d ago';
      return `${diffDays}d ago`;
    } catch {
      return null;
    }
  };

  const freshness = getFreshnessBadge(listing.scraped_at);

  const getSourceBadge = (source: string) => {
    switch (source.toLowerCase()) {
      case 'bizbuysell':
        return 'bg-blue-950/80 text-blue-400 border-blue-800/60';
      case 'businessesforsale':
        return 'bg-rose-950/80 text-rose-400 border-rose-800/60';
      case 'flippa':
        return 'bg-violet-950/80 text-violet-400 border-violet-800/60';
      case 'acquire.com':
        return 'bg-emerald-950/80 text-emerald-400 border-emerald-800/60';
      case 'empire flippers':
        return 'bg-amber-950/80 text-amber-400 border-amber-800/60';
      case 'businessbroker.net':
        return 'bg-cyan-950/80 text-cyan-400 border-cyan-800/60';
      case 'fe international':
        return 'bg-indigo-950/80 text-indigo-400 border-indigo-800/60';
      case 'loopnet':
        return 'bg-orange-950/80 text-orange-400 border-orange-800/60';
      default:
        return 'bg-slate-800 text-slate-300 border-slate-700';
    }
  };

  return (
    <div
      onClick={() => onSelect(listing)}
      className="glass-card rounded-2xl overflow-hidden cursor-pointer flex flex-col group relative"
    >
      {/* Header Image & Source Badge */}
      <div className="relative h-44 w-full bg-slate-900 overflow-hidden">
        {listing.image_url ? (
          <img
            src={listing.image_url}
            alt={listing.title}
            className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500 opacity-80 group-hover:opacity-100"
            loading="lazy"
          />
        ) : (
          <div className="w-full h-full flex items-center justify-center bg-gradient-to-br from-slate-900 to-slate-800">
            <Building className="w-12 h-12 text-slate-700" />
          </div>
        )}
        <div className="absolute inset-0 bg-gradient-to-t from-slate-950 via-slate-950/40 to-transparent" />

        {/* Source Badge & Category */}
        <div className="absolute top-3 left-3 flex items-center gap-1.5 flex-wrap">
          <span
            className={`text-[11px] font-bold px-2.5 py-0.5 rounded-full border backdrop-blur-md shadow-sm ${getSourceBadge(
              listing.source
            )}`}
          >
            {listing.source}
          </span>
          <span className="text-[11px] font-medium px-2.5 py-0.5 rounded-full bg-slate-900/90 text-slate-300 border border-slate-700/60 backdrop-blur-md">
            {listing.category}
          </span>
          {freshness && (
            <span className="text-[10px] font-medium px-2 py-0.5 rounded-full bg-slate-950/80 text-slate-400 border border-slate-800 backdrop-blur-md flex items-center gap-1">
              <CalendarCheck className="w-3 h-3 text-emerald-400" />
              {freshness}
            </span>
          )}
        </div>

        {/* Action buttons: Direct Link, Bookmark & Delete */}
        <div className="absolute top-3 right-3 flex items-center gap-1.5">
          <a
            href={listing.source_url}
            target="_blank"
            rel="noopener noreferrer"
            onClick={(e) => e.stopPropagation()}
            title={`Open on ${listing.source}`}
            className="p-2 rounded-full bg-slate-950/80 hover:bg-emerald-600 text-slate-300 hover:text-white border border-slate-700/80 backdrop-blur-md transition-all active:scale-90"
          >
            <ExternalLink className="w-3.5 h-3.5" />
          </a>
          <button
            onClick={(e) => onToggleSave(listing.id, e)}
            title={isSaved ? 'Remove from saved' : 'Save listing'}
            className="p-2 rounded-full bg-slate-950/80 hover:bg-slate-900 text-slate-300 hover:text-white border border-slate-700/80 backdrop-blur-md transition-all active:scale-90"
          >
            <Bookmark
              className={`w-3.5 h-3.5 ${isSaved ? 'text-amber-400 fill-amber-400' : 'text-slate-300'}`}
            />
          </button>
          {onDelete && (
            <button
              onClick={(e) => onDelete(listing.id, e)}
              title="Remove this listing from database"
              className="p-2 rounded-full bg-slate-950/80 hover:bg-rose-900/80 text-slate-400 hover:text-rose-300 border border-slate-700/80 backdrop-blur-md transition-all active:scale-90"
            >
              <Trash2 className="w-3.5 h-3.5" />
            </button>
          )}
        </div>


        {/* Location & Relocatable Tag */}
        <div className="absolute bottom-3 left-3 right-3 flex items-center justify-between text-xs text-slate-300">
          <div className="flex items-center gap-1.5 font-medium truncate max-w-[70%]">
            {listing.is_relocatable ? (
              <Laptop className="w-3.5 h-3.5 text-emerald-400 shrink-0" />
            ) : (
              <MapPin className="w-3.5 h-3.5 text-slate-400 shrink-0" />
            )}
            <span className="truncate">{listing.location}</span>
          </div>
          {listing.established_year && (
            <div className="flex items-center gap-1 text-[11px] text-slate-400">
              <Clock className="w-3 h-3" />
              <span>Est. {listing.established_year}</span>
            </div>
          )}
        </div>
      </div>

      {/* Body */}
      <div className="p-4 sm:p-5 flex-1 flex flex-col justify-between">
        <div>
          <h3 className="font-bold text-slate-100 text-base line-clamp-2 group-hover:text-emerald-400 transition-colors">
            {listing.title}
          </h3>
          <p className="mt-2 text-xs text-slate-400 line-clamp-2 leading-relaxed">
            {listing.description}
          </p>
        </div>

        {/* Key Financial Badges Grid */}
        <div className="mt-4 pt-3 border-t border-slate-800/80 grid grid-cols-2 gap-2 text-xs">
          {/* Asking Price */}
          <div className="bg-slate-900/90 rounded-xl p-2.5 border border-slate-800/80">
            <span className="text-[10px] uppercase font-bold tracking-wider text-slate-400 block">
              Asking Price
            </span>
            <span className="text-base font-extrabold text-white tracking-tight">
              {formatMoney(listing.asking_price)}
            </span>
          </div>

          {/* Cash Flow */}
          <div className="bg-emerald-950/30 rounded-xl p-2.5 border border-emerald-800/30">
            <span className="text-[10px] uppercase font-bold tracking-wider text-emerald-400 block">
              Cash Flow (SDE)
            </span>
            <span className="text-base font-extrabold text-emerald-300 tracking-tight">
              {formatMoney(listing.cash_flow)}
            </span>
          </div>
        </div>

        {/* Footer Metrics */}
        <div className="mt-3 flex items-center justify-between text-[11px] text-slate-400 font-medium">
          <div>
            {listing.price_to_cashflow_multiple ? (
              <span className="px-2 py-0.5 rounded-md bg-purple-950/60 text-purple-300 border border-purple-800/40">
                {listing.price_to_cashflow_multiple}x Cash Flow
              </span>
            ) : listing.gross_revenue ? (
              <span>Rev: {formatMoney(listing.gross_revenue)}</span>
            ) : (
              <span className="text-slate-500">Verified Marketplace</span>
            )}
          </div>

          <a
            href={listing.source_url}
            target="_blank"
            rel="noopener noreferrer"
            onClick={(e) => e.stopPropagation()}
            className="text-xs text-emerald-400 hover:text-emerald-300 font-semibold flex items-center gap-1 group/link"
          >
            <span>Visit Site</span>
            <ExternalLink className="w-3 h-3 group-hover/link:translate-x-0.5 group-hover/link:-translate-y-0.5 transition-transform" />
          </a>
        </div>
      </div>
    </div>
  );
};
