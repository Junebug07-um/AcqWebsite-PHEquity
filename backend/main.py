import asyncio
import uuid
from typing import Optional, List, Dict
from fastapi import FastAPI, Query, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from models import (
    BusinessListing, FilterParams, PaginatedListings,
    ScrapeRequest, ScrapeProgress, MarketStats
)
from database import (
    init_db, query_listings, get_listing_by_id,
    get_market_statistics, toggle_watchlist, get_watchlist_ids,
    get_latest_sync_event
)
from seed_data import seed_database
from scrapers.aggregator import ScraperAggregator
from scheduler import scheduler_instance

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize DB and populate seed data if empty
    init_db()
    seed_database()
    # Start automated daily scraper scheduler
    scheduler_instance.start()
    yield
    # Stop scheduler on shutdown
    scheduler_instance.stop()

app = FastAPI(
    title="Business-for-Sale Aggregator & Scraper API",
    description="Multi-platform business search, financial filters, live scraper engine, and daily auto-sync",
    version="1.1.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/health")
def health_check():
    return {
        "status": "online",
        "service": "Business-for-Sale Aggregator API",
        "docs": "/docs",
        "daily_auto_sync": scheduler_instance.get_status()
    }


@app.get("/api/listings", response_model=PaginatedListings)
def get_listings(
    q: Optional[str] = Query(None, description="Search keyword in title or description"),
    min_price: Optional[float] = Query(None, description="Minimum asking price"),
    max_price: Optional[float] = Query(None, description="Maximum asking price"),
    min_cash_flow: Optional[float] = Query(None, description="Minimum annual cash flow"),
    max_cash_flow: Optional[float] = Query(None, description="Maximum annual cash flow"),
    min_revenue: Optional[float] = Query(None, description="Minimum annual gross revenue"),
    max_revenue: Optional[float] = Query(None, description="Maximum annual gross revenue"),
    category: Optional[str] = Query(None, description="Industry / Category filter"),
    location: Optional[str] = Query(None, description="Location or State filter"),
    source: Optional[str] = Query(None, description="Platform source filter"),
    is_relocatable: Optional[bool] = Query(None, description="Filter for online/relocatable businesses"),
    max_multiple: Optional[float] = Query(None, description="Max Asking Price / Cash Flow multiple"),
    sort_by: Optional[str] = Query("newest", description="Sort order: newest, price_asc, price_desc, cash_flow_desc, multiple_asc, revenue_desc"),
    page: int = Query(1, ge=1),
    page_size: int = Query(12, ge=1, le=100)
):
    params = FilterParams(
        q=q,
        min_price=min_price,
        max_price=max_price,
        min_cash_flow=min_cash_flow,
        max_cash_flow=max_cash_flow,
        min_revenue=min_revenue,
        max_revenue=max_revenue,
        category=category,
        location=location,
        source=source,
        is_relocatable=is_relocatable,
        max_multiple=max_multiple,
        sort_by=sort_by,
        page=page,
        page_size=page_size
    )

    items, total = query_listings(params)
    total_pages = (total + page_size - 1) // page_size if total > 0 else 1

    return PaginatedListings(
        items=items,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages
    )

@app.get("/api/listings/{listing_id}", response_model=BusinessListing)
def get_listing_detail(listing_id: str):
    listing = get_listing_by_id(listing_id)
    if not listing:
        raise HTTPException(status_code=404, detail="Business listing not found")
    return listing

@app.get("/api/stats", response_model=MarketStats)
def get_stats():
    return get_market_statistics()

@app.get("/api/filters/metadata")
def get_filter_metadata():
    conn = get_market_statistics()
    categories = list(conn.category_distribution.keys())
    sources = list(conn.source_distribution.keys())
    locations = list(conn.top_locations.keys())
    
    return {
        "categories": ["All"] + sorted(categories),
        "sources": ["All"] + sorted(sources),
        "locations": ["All", "Online / Relocatable"] + [loc for loc in sorted(locations) if loc != "Online / Relocatable"],
        "supported_scrapers": ScraperAggregator.get_supported_sources()
    }

@app.post("/api/scrape")
async def trigger_scrape(request: ScrapeRequest, background_tasks: BackgroundTasks):
    task_id = str(uuid.uuid4())
    background_tasks.add_task(ScraperAggregator.run_scrape_job, task_id, request)
    return {
        "task_id": task_id,
        "message": f"Scrape job initiated across {len(request.sources)} sources",
        "sources": request.sources
    }

@app.get("/api/scrape/{task_id}", response_model=ScrapeProgress)
def get_scrape_status(task_id: str):
    job = ScraperAggregator.get_job_status(task_id)
    if not job:
        raise HTTPException(status_code=404, detail="Scrape task not found")
    return job

@app.get("/api/watchlist", response_model=List[str])
def get_watchlist():
    return get_watchlist_ids()

@app.post("/api/watchlist/{listing_id}")
def toggle_listing_watchlist(listing_id: str):
    saved = toggle_watchlist(listing_id)
    return {"listing_id": listing_id, "is_saved": saved}

@app.get("/api/scheduler/status")
def get_scheduler_status():
    return scheduler_instance.get_status()

@app.post("/api/scheduler/trigger")
async def trigger_scheduler_now(background_tasks: BackgroundTasks):
    req = ScrapeRequest(
        sources=ScraperAggregator.get_supported_sources(),
        max_results=20
    )
    task_id = f"manual-daily-sync-{int(asyncio.get_event_loop().time())}"
    background_tasks.add_task(ScraperAggregator.run_scrape_job, task_id, req)
    return {"status": "triggered", "task_id": task_id, "sources": req.sources}

# Mount frontend single page application if built
import os
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

frontend_dist = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "frontend", "dist"))
if os.path.exists(frontend_dist):
    assets_dir = os.path.join(frontend_dist, "assets")
    if os.path.exists(assets_dir):
        app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")

    @app.get("/{full_path:path}")
    async def serve_spa(full_path: str):
        if full_path.startswith("api") or full_path.startswith("docs") or full_path.startswith("openapi.json"):
            raise HTTPException(status_code=404, detail="Not Found")
        target_file = os.path.join(frontend_dist, full_path)
        if full_path and os.path.exists(target_file) and os.path.isfile(target_file):
            return FileResponse(target_file)
        return FileResponse(os.path.join(frontend_dist, "index.html"))

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)

