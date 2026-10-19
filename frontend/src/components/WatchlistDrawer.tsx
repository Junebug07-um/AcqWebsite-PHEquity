import React from 'react';
import { BusinessListing } from '../types';
import { X, Bookmark, ExternalLink, Trash2, DollarSign, MapPin } from 'lucide-react';

interface WatchlistDrawerProps {
  isOpen: boolean;
  onClose: () => void;
  savedListings: BusinessListing[];
  onRemoveSave: (id: string, e: React.MouseEvent) => void;
  onSelectListing: (listing: BusinessListing) => void;
}

export const WatchlistDrawer: React.FC<WatchlistDrawerProps> = ({
  isOpen,
  onClose,
  savedListings,
  onRemoveSave,
  onSelectListing,
}) => {
  if (!isOpen) return null;

  const formatMoney = (amount: number | null) => {
    if (amount === null || amount === undefined) return 'Undisclosed';
    if (amount >= 1_000_000) return `$${(amount / 1_000_000).toFixed(2)}M`;
    return `$${amount.toLocaleString()}`;
  };

  return (
    <div className="fixed inset-0 z-50 overflow-hidden">
      <div
        className="absolute inset-0 bg-black/70 backdrop-blur-sm transition-opacity"
        onClick={onClose}
      />

      <div className="fixed inset-y-0 right-0 max-w-full flex pl-10">
        <div className="w-screen max-w-md bg-slate-900 border-l border-slate-800 shadow-2xl flex flex-col">
          {/* Header */}
          <div className="p-5 border-b border-slate-800 flex items-center justify-between bg-slate-950/60">
            <div className="flex items-center gap-2">
              <Bookmark className="w-5 h-5 text-amber-400 fill-amber-400" />
              <h2 className="text-base font-bold text-white">Saved Listings</h2>
              <span className="px-2 py-0.5 rounded-full text-xs font-bold bg-slate-800 text-slate-300">
                {savedListings.length}
              </span>
            </div>
            <button
              onClick={onClose}
              className="p-1.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-400 hover:text-white"
            >
              <X className="w-5 h-5" />
            </button>
          </div>

          {/* List */}
          <div className="p-4 overflow-y-auto flex-1 space-y-3">
            {savedListings.length === 0 ? (
              <div className="text-center py-16 space-y-3">
                <Bookmark className="w-10 h-10 text-slate-700 mx-auto" />
                <p className="text-sm font-semibold text-slate-400">No saved businesses yet</p>
                <p className="text-xs text-slate-500 max-w-xs mx-auto">
                  Click the bookmark icon on any business card to save it for comparison and tracking.
                </p>
              </div>
            ) : (
              savedListings.map((item) => (
                <div
                  key={item.id}
                  onClick={() => {
                    onSelectListing(item);
                    onClose();
                  }}
                  className="p-4 rounded-2xl bg-slate-950/70 border border-slate-800 hover:border-emerald-500/40 cursor-pointer transition-all space-y-2 group"
                >
                  <div className="flex items-center justify-between gap-2">
                    <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-slate-800 text-emerald-400">
                      {item.source}
                    </span>
                    <button
                      onClick={(e) => onRemoveSave(item.id, e)}
                      title="Remove"
                      className="text-slate-500 hover:text-rose-400 transition-colors p-1"
                    >
                      <Trash2 className="w-4 h-4" />
                    </button>
                  </div>

                  <h4 className="text-xs font-bold text-white line-clamp-2 group-hover:text-emerald-300 transition-colors">
                    {item.title}
                  </h4>

                  <div className="flex items-center justify-between text-xs pt-1 border-t border-slate-800/80">
                    <span className="font-extrabold text-white">
                      {formatMoney(item.asking_price)}
                    </span>
                    <span className="text-emerald-400 font-semibold">
                      CF: {formatMoney(item.cash_flow)}
                    </span>
                  </div>
                </div>
              ))
            )}
          </div>
        </div>
      </div>
    </div>
  );
};
