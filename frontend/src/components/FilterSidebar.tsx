import React from 'react';
import { FilterState, FilterMetadata } from '../types';
import { Filter, RotateCcw, DollarSign, Building2, MapPin, Tag, ChevronDown, Check, Clock, ShieldCheck } from 'lucide-react';

interface FilterSidebarProps {
  filters: FilterState;
  metadata: FilterMetadata | null;
  onChange: (updates: Partial<FilterState>) => void;
  onReset: () => void;
  isOpenMobile: boolean;
  onCloseMobile: () => void;
}

export const FilterSidebar: React.FC<FilterSidebarProps> = ({
  filters,
  metadata,
  onChange,
  onReset,
  isOpenMobile,
  onCloseMobile,
}) => {
  const priceBrackets = [
    { label: 'Under $500k', min: null, max: 500000 },
    { label: '$500k - $1.5M', min: 500000, max: 1500000 },
    { label: '$1.5M - $3M', min: 1500000, max: 3000000 },
    { label: '$3M+', min: 3000000, max: null },
  ];

  const cashFlowBrackets = [
    { label: '$100k+', min: 100000 },
    { label: '$250k+', min: 250000 },
    { label: '$500k+', min: 500000 },
    { label: '$1M+', min: 1000000 },
  ];

  const multipleCaps = [
    { label: 'Any Multiple', value: null },
    { label: '< 2.5x SDE (Deep Value)', value: 2.5 },
    { label: '< 3.5x SDE (Standard)', value: 3.5 },
    { label: '< 5.0x SDE (Growth)', value: 5.0 },
  ];

  return (
    <>
      {/* Mobile backdrop */}
      {isOpenMobile && (
        <div
          className="fixed inset-0 bg-black/60 z-40 lg:hidden backdrop-blur-sm"
          onClick={onCloseMobile}
        />
      )}

      <aside
        className={`fixed lg:static top-0 left-0 bottom-0 z-50 w-80 bg-slate-950/95 lg:bg-transparent border-r lg:border-r-0 border-slate-800 p-5 overflow-y-auto transform transition-transform duration-300 ease-in-out ${
          isOpenMobile ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'
        }`}
      >
        <div className="flex items-center justify-between pb-4 border-b border-slate-800/80 mb-6">
          <div className="flex items-center gap-2">
            <Filter className="w-4 h-4 text-emerald-400" />
            <h2 className="text-base font-bold text-slate-100">Deal Filters</h2>
          </div>
          <button
            onClick={onReset}
            className="flex items-center gap-1 text-xs font-semibold text-slate-400 hover:text-emerald-400 transition-colors"
          >
            <RotateCcw className="w-3 h-3" />
            Reset
          </button>
        </div>

        <div className="space-y-6">
          {/* Industry / Category */}
          <div>
            <label className="text-xs font-bold text-slate-300 uppercase tracking-wider mb-2.5 flex items-center gap-1.5">
              <Building2 className="w-3.5 h-3.5 text-emerald-400" /> Industry & Niche
            </label>
            <div className="space-y-1 max-h-48 overflow-y-auto pr-1">
              {(metadata?.categories || ['All', 'E-commerce', 'SaaS & Software', 'Restaurants & Food', 'Automotive', 'Services & Contracting', 'Healthcare & Medical', 'Manufacturing & Industrial', 'Content & Media']).map(
                (cat) => (
                  <button
                    key={cat}
                    onClick={() => onChange({ category: cat, page: 1 })}
                    className={`w-full text-left px-3 py-1.5 rounded-lg text-xs font-medium transition-all flex items-center justify-between ${
                      filters.category === cat || (cat === 'All' && !filters.category)
                        ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/40 font-semibold'
                        : 'text-slate-400 hover:text-slate-200 hover:bg-slate-900'
                    }`}
                  >
                    <span>{cat}</span>
                    {(filters.category === cat || (cat === 'All' && !filters.category)) && (
                      <Check className="w-3.5 h-3.5 text-emerald-400" />
                    )}
                  </button>
                )
              )}
            </div>
          </div>

          {/* Asking Price Filter */}
          <div>
            <label className="text-xs font-bold text-slate-300 uppercase tracking-wider mb-2.5 flex items-center gap-1.5">
              <DollarSign className="w-3.5 h-3.5 text-emerald-400" /> Asking Price Range
            </label>
            <div className="grid grid-cols-2 gap-2 mb-2">
              {priceBrackets.map((b) => {
                const isSelected = filters.min_price === b.min && filters.max_price === b.max;
                return (
                  <button
                    key={b.label}
                    onClick={() =>
                      onChange({
                        min_price: isSelected ? null : b.min,
                        max_price: isSelected ? null : b.max,
                        page: 1,
                      })
                    }
                    className={`px-2.5 py-1.5 rounded-lg text-[11px] font-medium transition-all text-center border ${
                      isSelected
                        ? 'bg-emerald-500/20 text-emerald-300 border-emerald-500/50'
                        : 'bg-slate-900 text-slate-400 hover:text-slate-200 border-slate-800'
                    }`}
                  >
                    {b.label}
                  </button>
                );
              })}
            </div>
            {/* Custom Price Inputs */}
            <div className="flex items-center gap-2 mt-2">
              <div className="relative flex-1">
                <span className="absolute left-2.5 top-1/2 -translate-y-1/2 text-xs text-slate-500">$</span>
                <input
                  type="number"
                  placeholder="Min Price"
                  value={filters.min_price || ''}
                  onChange={(e) =>
                    onChange({
                      min_price: e.target.value ? Number(e.target.value) : null,
                      page: 1,
                    })
                  }
                  className="w-full pl-6 pr-2 py-1.5 bg-slate-900 border border-slate-800 rounded-lg text-xs text-slate-200 focus:outline-none focus:border-emerald-500"
                />
              </div>
              <span className="text-xs text-slate-500">-</span>
              <div className="relative flex-1">
                <span className="absolute left-2.5 top-1/2 -translate-y-1/2 text-xs text-slate-500">$</span>
                <input
                  type="number"
                  placeholder="Max Price"
                  value={filters.max_price || ''}
                  onChange={(e) =>
                    onChange({
                      max_price: e.target.value ? Number(e.target.value) : null,
                      page: 1,
                    })
                  }
                  className="w-full pl-6 pr-2 py-1.5 bg-slate-900 border border-slate-800 rounded-lg text-xs text-slate-200 focus:outline-none focus:border-emerald-500"
                />
              </div>
            </div>
          </div>

          {/* Min Cash Flow (SDE) */}
          <div>
            <label className="text-xs font-bold text-slate-300 uppercase tracking-wider mb-2.5 flex items-center gap-1.5">
              <Tag className="w-3.5 h-3.5 text-emerald-400" /> Minimum Annual Cash Flow
            </label>
            <div className="grid grid-cols-2 gap-2">
              {cashFlowBrackets.map((cf) => {
                const isSelected = filters.min_cash_flow === cf.min;
                return (
                  <button
                    key={cf.label}
                    onClick={() =>
                      onChange({
                        min_cash_flow: isSelected ? null : cf.min,
                        page: 1,
                      })
                    }
                    className={`px-2.5 py-1.5 rounded-lg text-[11px] font-medium transition-all text-center border ${
                      isSelected
                        ? 'bg-emerald-500/20 text-emerald-300 border-emerald-500/50'
                        : 'bg-slate-900 text-slate-400 hover:text-slate-200 border-slate-800'
                    }`}
                  >
                    {cf.label}
                  </button>
                );
              })}
            </div>
          </div>

          {/* Valuation Multiple Cap */}
          <div>
            <label className="text-xs font-bold text-slate-300 uppercase tracking-wider mb-2.5 block">
              Max Price / SDE Multiple
            </label>
            <div className="space-y-1">
              {multipleCaps.map((m) => {
                const isSelected = filters.max_multiple === m.value;
                return (
                  <button
                    key={m.label}
                    onClick={() => onChange({ max_multiple: m.value, page: 1 })}
                    className={`w-full text-left px-3 py-1.5 rounded-lg text-xs font-medium transition-all flex items-center justify-between ${
                      isSelected
                        ? 'bg-purple-500/20 text-purple-300 border border-purple-500/40 font-semibold'
                        : 'text-slate-400 hover:text-slate-200 hover:bg-slate-900'
                    }`}
                  >
                    <span>{m.label}</span>
                    {isSelected && <Check className="w-3.5 h-3.5 text-purple-400" />}
                  </button>
                );
              })}
            </div>
          </div>

          {/* Location & Relocatable toggle */}
          <div>
            <label className="text-xs font-bold text-slate-300 uppercase tracking-wider mb-2.5 flex items-center gap-1.5">
              <MapPin className="w-3.5 h-3.5 text-emerald-400" /> Location / Mobility
            </label>
            <label className="flex items-center gap-2.5 p-2.5 rounded-xl bg-slate-900/80 border border-slate-800 cursor-pointer hover:border-slate-700 transition-all mb-3">
              <input
                type="checkbox"
                checked={filters.is_relocatable === true}
                onChange={(e) =>
                  onChange({
                    is_relocatable: e.target.checked ? true : null,
                    page: 1,
                  })
                }
                className="rounded border-slate-700 text-emerald-500 focus:ring-emerald-500/30 bg-slate-800 w-4 h-4"
              />
              <span className="text-xs text-slate-200 font-medium">
                Online / Relocatable Only
              </span>
            </label>

            <select
              value={filters.location}
              onChange={(e) => onChange({ location: e.target.value, page: 1 })}
              className="w-full px-3 py-2 bg-slate-900 border border-slate-800 rounded-lg text-xs text-slate-200 focus:outline-none focus:border-emerald-500"
            >
              {(metadata?.locations || ['All', 'Online / Relocatable', 'TX', 'FL', 'CA', 'NC', 'TN', 'AZ', 'OH', 'CO']).map(
                (loc) => (
                  <option key={loc} value={loc}>
                    {loc === 'All' ? 'All Locations' : loc}
                  </option>
                )
              )}
            </select>
          </div>

          {/* Data Quality & Recency */}
          <div>
            <label className="text-xs font-bold text-slate-300 uppercase tracking-wider mb-2.5 flex items-center gap-1.5">
              <Clock className="w-3.5 h-3.5 text-emerald-400" /> Data Quality & Recency
            </label>
            <label className="flex items-center gap-2.5 p-2.5 rounded-xl bg-slate-900/80 border border-slate-800 cursor-pointer hover:border-slate-700 transition-all mb-3">
              <input
                type="checkbox"
                checked={filters.only_priced === true}
                onChange={(e) =>
                  onChange({
                    only_priced: e.target.checked,
                    page: 1,
                  })
                }
                className="rounded border-slate-700 text-emerald-500 focus:ring-emerald-500/30 bg-slate-800 w-4 h-4"
              />
              <div className="flex flex-col">
                <span className="text-xs text-slate-200 font-medium flex items-center gap-1">
                  <ShieldCheck className="w-3 h-3 text-emerald-400" /> Verified Price Only
                </span>
                <span className="text-[10px] text-slate-400">Hide unpriced & franchise lead forms</span>
              </div>
            </label>

            <div>
              <span className="text-[11px] font-medium text-slate-400 block mb-1.5">Max Listing Age:</span>
              <div className="grid grid-cols-2 gap-1.5">
                {[
                  { label: 'All Listings', value: null },
                  { label: 'Past 24 Hours', value: 1 },
                  { label: 'Past 7 Days', value: 7 },
                  { label: 'Past 30 Days', value: 30 },
                ].map((age) => {
                  const isSelected = filters.max_age_days === age.value;
                  return (
                    <button
                      key={age.label}
                      onClick={() => onChange({ max_age_days: age.value, page: 1 })}
                      className={`px-2 py-1.5 rounded-lg text-[11px] font-medium transition-all text-center border ${
                        isSelected
                          ? 'bg-emerald-500/20 text-emerald-300 border-emerald-500/50 font-semibold'
                          : 'bg-slate-900 text-slate-400 hover:text-slate-200 border-slate-800'
                      }`}
                    >
                      {age.label}
                    </button>
                  );
                })}
              </div>
            </div>
          </div>
        </div>
      </aside>
    </>
  );
};
