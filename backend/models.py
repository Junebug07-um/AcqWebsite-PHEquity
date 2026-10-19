from typing import Optional, List, Dict
from pydantic import BaseModel, Field
from datetime import datetime
import uuid

class BusinessListing(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    description: str = ""
    asking_price: Optional[float] = None
    cash_flow: Optional[float] = None
    gross_revenue: Optional[float] = None
    ebitda: Optional[float] = None
    location: str = "United States"
    city: Optional[str] = None
    state: Optional[str] = None
    country: str = "USA"
    is_relocatable: bool = False
    category: str = "General Business"
    sub_category: Optional[str] = None
    source: str  # e.g., "BizBuySell", "Flippa", "Acquire.com", "Empire Flippers", "BusinessBroker"
    source_url: str
    image_url: Optional[str] = None
    established_year: Optional[int] = None
    employees: Optional[int] = None
    inventory_included: Optional[bool] = None
    real_estate_included: Optional[bool] = None
    reason_for_selling: Optional[str] = None
    scraped_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    price_to_cashflow_multiple: Optional[float] = None
    price_to_revenue_multiple: Optional[float] = None

    def calculate_multiples(self):
        if self.asking_price and self.cash_flow and self.cash_flow > 0:
            self.price_to_cashflow_multiple = round(self.asking_price / self.cash_flow, 2)
        if self.asking_price and self.gross_revenue and self.gross_revenue > 0:
            self.price_to_revenue_multiple = round(self.asking_price / self.gross_revenue, 2)

class FilterParams(BaseModel):
    q: Optional[str] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    min_cash_flow: Optional[float] = None
    max_cash_flow: Optional[float] = None
    min_revenue: Optional[float] = None
    max_revenue: Optional[float] = None
    category: Optional[str] = None
    location: Optional[str] = None
    source: Optional[str] = None
    is_relocatable: Optional[bool] = None
    max_multiple: Optional[float] = None
    sort_by: Optional[str] = "newest"  # "price_asc", "price_desc", "cash_flow_desc", "multiple_asc", "newest"
    page: int = 1
    page_size: int = 12

class PaginatedListings(BaseModel):
    items: List[BusinessListing]
    total: int
    page: int
    page_size: int
    total_pages: int

class ScrapeRequest(BaseModel):
    sources: List[str] = ["BizBuySell", "Flippa", "Acquire.com", "Empire Flippers"]
    keywords: Optional[str] = None
    category: Optional[str] = None
    location: Optional[str] = None
    max_results: int = 25

class ScrapeProgress(BaseModel):
    task_id: str
    status: str  # "running", "completed", "failed"
    progress: int  # 0 to 100
    message: str
    found_count: int
    sources_status: Dict[str, str]

class MarketStats(BaseModel):
    total_listings: int
    avg_asking_price: float
    median_asking_price: float
    avg_cash_flow: float
    avg_multiple: float
    category_distribution: Dict[str, int]
    source_distribution: Dict[str, int]
    top_locations: Dict[str, int]
