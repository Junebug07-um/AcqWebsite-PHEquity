import { BusinessListing, FilterState, PaginatedResponse, MarketStats, FilterMetadata, ScrapeProgress } from '../types';

const API_BASE = '/api';

export async function fetchListings(filters: Partial<FilterState>): Promise<PaginatedResponse> {
  const params = new URLSearchParams();

  if (filters.q) params.append('q', filters.q);
  if (filters.min_price !== null && filters.min_price !== undefined) params.append('min_price', filters.min_price.toString());
  if (filters.max_price !== null && filters.max_price !== undefined) params.append('max_price', filters.max_price.toString());
  if (filters.min_cash_flow !== null && filters.min_cash_flow !== undefined) params.append('min_cash_flow', filters.min_cash_flow.toString());
  if (filters.max_cash_flow !== null && filters.max_cash_flow !== undefined) params.append('max_cash_flow', filters.max_cash_flow.toString());
  if (filters.min_revenue !== null && filters.min_revenue !== undefined) params.append('min_revenue', filters.min_revenue.toString());
  if (filters.max_revenue !== null && filters.max_revenue !== undefined) params.append('max_revenue', filters.max_revenue.toString());
  if (filters.category && filters.category !== 'All') params.append('category', filters.category);
  if (filters.location && filters.location !== 'All') params.append('location', filters.location);
  if (filters.source && filters.source !== 'All') params.append('source', filters.source);
  if (filters.is_relocatable !== null && filters.is_relocatable !== undefined) params.append('is_relocatable', filters.is_relocatable.toString());
  if (filters.max_multiple !== null && filters.max_multiple !== undefined) params.append('max_multiple', filters.max_multiple.toString());
  if (filters.only_priced) params.append('only_priced', 'true');
  if (filters.max_age_days !== null && filters.max_age_days !== undefined) params.append('max_age_days', filters.max_age_days.toString());
  if (filters.sort_by) params.append('sort_by', filters.sort_by);
  if (filters.page) params.append('page', filters.page.toString());
  if (filters.page_size) params.append('page_size', filters.page_size.toString());

  const res = await fetch(`${API_BASE}/listings?${params.toString()}`);
  if (!res.ok) throw new Error(`Failed to fetch listings: ${res.statusText}`);
  return res.json();
}


export async function fetchListingDetail(id: string): Promise<BusinessListing> {
  const res = await fetch(`${API_BASE}/listings/${id}`);
  if (!res.ok) throw new Error(`Listing not found: ${res.statusText}`);
  return res.json();
}

export async function fetchMarketStats(): Promise<MarketStats> {
  const res = await fetch(`${API_BASE}/stats`);
  if (!res.ok) throw new Error(`Failed to fetch stats: ${res.statusText}`);
  return res.json();
}

export async function fetchFilterMetadata(): Promise<FilterMetadata> {
  const res = await fetch(`${API_BASE}/filters/metadata`);
  if (!res.ok) throw new Error(`Failed to fetch filter metadata: ${res.statusText}`);
  return res.json();
}

export async function triggerScraperJob(sources: string[], keywords?: string, category?: string): Promise<{ task_id: string; message: string }> {
  const res = await fetch(`${API_BASE}/scrape`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ sources, keywords, category, max_results: 20 })
  });
  if (!res.ok) throw new Error(`Failed to trigger scraper: ${res.statusText}`);
  return res.json();
}

export async function pollScraperStatus(taskId: string): Promise<ScrapeProgress> {
  const res = await fetch(`${API_BASE}/scrape/${taskId}`);
  if (!res.ok) throw new Error(`Failed to poll scraper status: ${res.statusText}`);
  return res.json();
}

export async function fetchWatchlist(): Promise<string[]> {
  const res = await fetch(`${API_BASE}/watchlist`);
  if (!res.ok) return [];
  return res.json();
}

export async function toggleWatchlistApi(listingId: string): Promise<{ listing_id: string; is_saved: boolean }> {
  const res = await fetch(`${API_BASE}/watchlist/${listingId}`, {
    method: 'POST'
  });
  if (!res.ok) throw new Error(`Failed to toggle watchlist: ${res.statusText}`);
  return res.json();
}

export async function fetchSchedulerStatus(): Promise<import('../types').SchedulerStatus> {
  const res = await fetch(`${API_BASE}/scheduler/status`);
  if (!res.ok) throw new Error(`Failed to fetch scheduler status: ${res.statusText}`);
  return res.json();
}

export async function triggerDailySync(): Promise<{ status: string; task_id: string; sources: string[] }> {
  const res = await fetch(`${API_BASE}/scheduler/trigger`, {
    method: 'POST'
  });
  if (!res.ok) throw new Error(`Failed to trigger sync: ${res.statusText}`);
  return res.json();
}

export async function deleteListingApi(listingId: string): Promise<{ success: boolean; deleted_id: string }> {
  const res = await fetch(`${API_BASE}/listings/${listingId}`, {
    method: 'DELETE'
  });
  if (!res.ok) throw new Error(`Failed to delete listing: ${res.statusText}`);
  return res.json();
}

export async function purgeStaleListingsApi(days: number = 14, keepWatchlist: boolean = true): Promise<{ success: boolean; purged_count: number }> {
  const res = await fetch(`${API_BASE}/listings/purge?days=${days}&keep_watchlist=${keepWatchlist}`, {
    method: 'POST'
  });
  if (!res.ok) throw new Error(`Failed to purge stale listings: ${res.statusText}`);
  return res.json();
}

export async function clearListingsApi(keepWatchlist: boolean = true): Promise<{ success: boolean; cleared_count: number }> {
  const res = await fetch(`${API_BASE}/listings/clear?keep_watchlist=${keepWatchlist}`, {
    method: 'POST'
  });
  if (!res.ok) throw new Error(`Failed to clear database: ${res.statusText}`);
  return res.json();
}


