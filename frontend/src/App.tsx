import React, { useState, useEffect, useCallback } from 'react';
import { Navbar } from './components/Navbar';
import { MarketInsights } from './components/MarketInsights';
import { FilterSidebar } from './components/FilterSidebar';
import { ListingCard } from './components/ListingCard';
import { ListingModal } from './components/ListingModal';
import { ScrapeModal } from './components/ScrapeModal';
import { DealCalculatorModal } from './components/DealCalculatorModal';
import { WatchlistDrawer } from './components/WatchlistDrawer';
import {
  fetchListings,
  fetchMarketStats,
  fetchFilterMetadata,
  fetchWatchlist,
  toggleWatchlistApi,
  deleteListingApi,
  purgeStaleListingsApi,
} from './services/api';
import {
  BusinessListing,
  FilterState,
  MarketStats as MarketStatsType,
  FilterMetadata,
} from './types';
import {
  SlidersHorizontal,
  ArrowUpDown,
  SearchX,
  Loader2,
  ChevronLeft,
  ChevronRight,
  Sparkles,
  RefreshCw,
  Trash2,
} from 'lucide-react';

const initialFilters: FilterState = {
  q: '',
  min_price: null,
  max_price: null,
  min_cash_flow: null,
  max_cash_flow: null,
  min_revenue: null,
  max_revenue: null,
  category: 'All',
  location: 'All',
  source: 'All',
  is_relocatable: null,
  max_multiple: null,
  only_priced: false,
  max_age_days: null,
  sort_by: 'newest',
  page: 1,
  page_size: 12,
};

export const App: React.FC = () => {
  const [filters, setFilters] = useState<FilterState>(initialFilters);
  const [listings, setListings] = useState<BusinessListing[]>([]);
  const [totalListings, setTotalListings] = useState<number>(0);
  const [totalPages, setTotalPages] = useState<number>(1);
  const [loading, setLoading] = useState<boolean>(true);
  const [stats, setStats] = useState<MarketStatsType | null>(null);
  const [metadata, setMetadata] = useState<FilterMetadata | null>(null);
  const [watchlistIds, setWatchlistIds] = useState<string[]>([]);
  const [schedulerStatus, setSchedulerStatus] = useState<import('./types').SchedulerStatus | null>(null);

  // Modal / Drawer States
  const [selectedListing, setSelectedListing] = useState<BusinessListing | null>(null);
  const [isScrapeModalOpen, setIsScrapeModalOpen] = useState<boolean>(false);
  const [isCalculatorOpen, setIsCalculatorOpen] = useState<boolean>(false);
  const [calculatorInitialListing, setCalculatorInitialListing] = useState<BusinessListing | null>(null);
  const [isWatchlistOpen, setIsWatchlistOpen] = useState<boolean>(false);
  const [isMobileFiltersOpen, setIsMobileFiltersOpen] = useState<boolean>(false);

  // Load Metadata, Stats & Watchlist on Mount
  const loadInitialData = async () => {
    try {
      const [statsData, metaData, savedIds, schedulerData] = await Promise.all([
        fetchMarketStats(),
        fetchFilterMetadata(),
        fetchWatchlist(),
        (await import('./services/api')).fetchSchedulerStatus().catch(() => null),
      ]);
      setStats(statsData);
      setMetadata(metaData);
      setWatchlistIds(savedIds);
      if (schedulerData) setSchedulerStatus(schedulerData);
    } catch (e) {
      console.error('Failed to load initial metadata:', e);
    }
  };


  useEffect(() => {
    loadInitialData();
  }, []);

  // Fetch Listings whenever filters change
  const loadListings = useCallback(async () => {
    setLoading(true);
    try {
      const data = await fetchListings(filters);
      setListings(data.items);
      setTotalListings(data.total);
      setTotalPages(data.total_pages);
    } catch (e) {
      console.error('Failed to fetch listings:', e);
    } finally {
      setLoading(false);
    }
  }, [filters]);

  useEffect(() => {
    const timer = setTimeout(() => {
      loadListings();
    }, 200); // 200ms debounce
    return () => clearTimeout(timer);
  }, [loadListings]);

  const handleFilterChange = (updates: Partial<FilterState>) => {
    setFilters((prev) => ({ ...prev, ...updates }));
  };

  const handleResetFilters = () => {
    setFilters(initialFilters);
  };

  const handleToggleWatchlist = async (id: string, e: React.MouseEvent) => {
    e.stopPropagation();
    try {
      const res = await toggleWatchlistApi(id);
      if (res.is_saved) {
        setWatchlistIds((prev) => [...prev, id]);
      } else {
        setWatchlistIds((prev) => prev.filter((item) => item !== id));
      }
    } catch (err) {
      console.error('Failed to toggle save:', err);
    }
  };

  const handleOpenCalculatorForDeal = (listing: BusinessListing) => {
    setSelectedListing(null);
    setCalculatorInitialListing(listing);
    setIsCalculatorOpen(true);
  };

  const handleDeleteListing = async (id: string, e: React.MouseEvent) => {
    e.stopPropagation();
    if (!window.confirm('Delete this listing from the database?')) return;
    try {
      await deleteListingApi(id);
      setListings((prev) => prev.filter((item) => item.id !== id));
      setTotalListings((prev) => Math.max(0, prev - 1));
      loadInitialData();
    } catch (err) {
      console.error('Failed to delete listing:', err);
      alert('Could not delete listing');
    }
  };

  const handlePurgeStale = async () => {
    if (!window.confirm('Clean stale database records? This will delete listings older than 14 days while keeping your saved watchlist.')) return;
    try {
      const res = await purgeStaleListingsApi(14, true);
      alert(`Cleaned up ${res.purged_count} stale listings.`);
      await loadInitialData();
      loadListings();
    } catch (err) {
      console.error('Failed to purge stale listings:', err);
      alert('Could not purge stale listings');
    }
  };

  const handleScrapeComplete = async () => {
    await loadInitialData();
    loadListings();
  };

  const savedListingsObjects = listings.filter((item) => watchlistIds.includes(item.id));

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col selection:bg-emerald-500 selection:text-white">
      {/* Top Navbar */}
      <Navbar
        searchQuery={filters.q}
        onSearchChange={(q) => handleFilterChange({ q, page: 1 })}
        onOpenScraper={() => setIsScrapeModalOpen(true)}
        onOpenCalculator={() => {
          setCalculatorInitialListing(null);
          setIsCalculatorOpen(true);
        }}
        onOpenWatchlist={() => setIsWatchlistOpen(true)}
        watchlistCount={watchlistIds.length}
        totalListings={totalListings}
        schedulerStatus={schedulerStatus}
      />


      {/* Main App Body */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-6 flex gap-8">
        {/* Left Filter Sidebar */}
        <FilterSidebar
          filters={filters}
          metadata={metadata}
          onChange={handleFilterChange}
          onReset={handleResetFilters}
          isOpenMobile={isMobileFiltersOpen}
          onCloseMobile={() => setIsMobileFiltersOpen(false)}
        />

        {/* Right Listing Feed & Controls */}
        <div className="flex-1 min-w-0 space-y-6">
          {/* Market Intelligence KPIs */}
          <MarketInsights
            stats={stats}
            activeSource={filters.source}
            onSelectSource={(src) => handleFilterChange({ source: src, page: 1 })}
          />

          {/* Results Toolbar: Mobile Filter Button, Result Count & Sort Selector */}
          <div className="flex flex-wrap items-center justify-between gap-3 p-3.5 rounded-2xl bg-slate-900/60 border border-slate-800/80">
            <div className="flex items-center gap-3">
              <button
                onClick={() => setIsMobileFiltersOpen(true)}
                className="lg:hidden flex items-center gap-2 px-3 py-1.5 rounded-xl bg-slate-800 text-xs font-semibold text-slate-200"
              >
                <SlidersHorizontal className="w-3.5 h-3.5 text-emerald-400" />
                Filters
              </button>

              <span className="text-xs font-semibold text-slate-300">
                Found <strong className="text-white">{totalListings}</strong> matching business
                deals
              </span>

              <button
                onClick={handlePurgeStale}
                title="Purge listings older than 14 days (watchlist preserved)"
                className="flex items-center gap-1.5 px-2.5 py-1 rounded-xl bg-slate-800/80 hover:bg-slate-700/80 border border-slate-700/60 text-[11px] font-semibold text-slate-300 hover:text-rose-300 transition-all ml-2"
              >
                <Trash2 className="w-3 h-3 text-rose-400" />
                <span className="hidden sm:inline">Clean Stale Deals</span>
              </button>
            </div>

            {/* Sort Order Selector */}
            <div className="flex items-center gap-2 text-xs">
              <span className="text-slate-400 font-medium hidden sm:inline flex items-center gap-1">
                <ArrowUpDown className="w-3.5 h-3.5" /> Sort:
              </span>
              <select
                value={filters.sort_by}
                onChange={(e) => handleFilterChange({ sort_by: e.target.value, page: 1 })}
                className="bg-slate-950 border border-slate-700/80 rounded-xl px-3 py-1.5 text-xs text-slate-200 font-semibold focus:outline-none focus:border-emerald-500"
              >
                <option value="newest">Newest Scraped</option>
                <option value="price_asc">Price: Low to High</option>
                <option value="price_desc">Price: High to Low</option>
                <option value="cash_flow_desc">Cash Flow: High to Low</option>
                <option value="multiple_asc">Lowest Valuation Multiple</option>
                <option value="revenue_desc">Revenue: High to Low</option>
              </select>
            </div>
          </div>

          {/* Listing Cards Grid */}
          {loading ? (
            <div className="py-24 text-center space-y-3">
              <Loader2 className="w-8 h-8 text-emerald-400 animate-spin mx-auto" />
              <p className="text-sm font-semibold text-slate-400">
                Searching & filtering listings...
              </p>
            </div>
          ) : listings.length === 0 ? (
            <div className="py-20 text-center rounded-3xl bg-slate-900/40 border border-slate-800 p-8 space-y-4">
              <SearchX className="w-12 h-12 text-slate-600 mx-auto" />
              <div>
                <h3 className="text-base font-bold text-slate-200">No businesses found</h3>
                <p className="text-xs text-slate-400 mt-1 max-w-sm mx-auto">
                  No deals matched your current filter criteria. Try broadening your price range or
                  run a fresh live scrape.
                </p>
              </div>
              <div className="flex items-center justify-center gap-3 pt-2">
                <button
                  onClick={handleResetFilters}
                  className="px-4 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-xs font-semibold text-slate-200"
                >
                  Clear Filters
                </button>
                <button
                  onClick={() => setIsScrapeModalOpen(true)}
                  className="flex items-center gap-1.5 px-4 py-2 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-xs font-bold text-white shadow-md shadow-emerald-950"
                >
                  <Sparkles className="w-3.5 h-3.5" />
                  Scrape New Listings
                </button>
              </div>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-5">
              {listings.map((item) => (
                <ListingCard
                  key={item.id}
                  listing={item}
                  isSaved={watchlistIds.includes(item.id)}
                  onToggleSave={handleToggleWatchlist}
                  onDelete={handleDeleteListing}
                  onSelect={setSelectedListing}
                />
              ))}
            </div>
          )}

          {/* Pagination Controls */}
          {totalPages > 1 && (
            <div className="flex items-center justify-center gap-3 pt-6 pb-12">
              <button
                onClick={() => handleFilterChange({ page: Math.max(1, filters.page - 1) })}
                disabled={filters.page <= 1}
                className="p-2 rounded-xl bg-slate-900 border border-slate-800 hover:bg-slate-800 disabled:opacity-40 disabled:cursor-not-allowed text-slate-300"
              >
                <ChevronLeft className="w-4 h-4" />
              </button>

              <span className="text-xs font-bold text-slate-300 px-3 py-1.5 rounded-xl bg-slate-900 border border-slate-800">
                Page {filters.page} of {totalPages}
              </span>

              <button
                onClick={() =>
                  handleFilterChange({ page: Math.min(totalPages, filters.page + 1) })
                }
                disabled={filters.page >= totalPages}
                className="p-2 rounded-xl bg-slate-900 border border-slate-800 hover:bg-slate-800 disabled:opacity-40 disabled:cursor-not-allowed text-slate-300"
              >
                <ChevronRight className="w-4 h-4" />
              </button>
            </div>
          )}
        </div>
      </main>

      {/* Modals & Slide-overs */}
      <ListingModal
        listing={selectedListing}
        onClose={() => setSelectedListing(null)}
        isSaved={selectedListing ? watchlistIds.includes(selectedListing.id) : false}
        onToggleSave={handleToggleWatchlist}
        onOpenCalculatorForDeal={handleOpenCalculatorForDeal}
      />

      <ScrapeModal
        isOpen={isScrapeModalOpen}
        onClose={() => setIsScrapeModalOpen(false)}
        onScrapeComplete={handleScrapeComplete}
        availableSources={metadata?.supported_scrapers || []}
      />

      <DealCalculatorModal
        isOpen={isCalculatorOpen}
        onClose={() => setIsCalculatorOpen(false)}
        initialListing={calculatorInitialListing}
      />

      <WatchlistDrawer
        isOpen={isWatchlistOpen}
        onClose={() => setIsWatchlistOpen(false)}
        savedListings={savedListingsObjects}
        onRemoveSave={handleToggleWatchlist}
        onSelectListing={setSelectedListing}
      />
    </div>
  );
};

export default App;
