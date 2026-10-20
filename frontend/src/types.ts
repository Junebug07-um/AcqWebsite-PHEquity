export interface BusinessListing {
  id: string;
  title: string;
  description: string;
  asking_price: number | null;
  cash_flow: number | null;
  gross_revenue: number | null;
  ebitda: number | null;
  location: string;
  city: string | null;
  state: string | null;
  country: string;
  is_relocatable: boolean;
  category: string;
  sub_category: string | null;
  source: string;
  source_url: string;
  image_url: string | null;
  established_year: number | null;
  employees: number | null;
  inventory_included: boolean | null;
  real_estate_included: boolean | null;
  reason_for_selling: string | null;
  scraped_at: string;
  price_to_cashflow_multiple: number | null;
  price_to_revenue_multiple: number | null;
}

export interface PaginatedResponse {
  items: BusinessListing[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
}

export interface FilterState {
  q: string;
  min_price: number | null;
  max_price: number | null;
  min_cash_flow: number | null;
  max_cash_flow: number | null;
  min_revenue: number | null;
  max_revenue: number | null;
  category: string;
  location: string;
  source: string;
  is_relocatable: boolean | null;
  max_multiple: number | null;
  only_priced: boolean;
  max_age_days: number | null;
  sort_by: string;
  page: number;
  page_size: number;
}


export interface MarketStats {
  total_listings: number;
  avg_asking_price: number;
  median_asking_price: number;
  avg_cash_flow: number;
  avg_multiple: number;
  category_distribution: Record<string, number>;
  source_distribution: Record<string, number>;
  top_locations: Record<string, number>;
}

export interface FilterMetadata {
  categories: string[];
  sources: string[];
  locations: string[];
  supported_scrapers: string[];
}

export interface ScrapeProgress {
  task_id: string;
  status: 'running' | 'completed' | 'failed';
  progress: number;
  message: string;
  found_count: number;
  sources_status: Record<string, string>;
}

export interface SchedulerStatus {
  is_running: boolean;
  interval_hours: number;
  last_run_at: string | null;
  next_run_at: string | null;
  status_message: string;
}

