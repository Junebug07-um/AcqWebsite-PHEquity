import asyncio
import uuid
from typing import List, Optional, Dict
from models import BusinessListing, ScrapeRequest, ScrapeProgress
from .bizbuysell import BizBuySellScraper
from .flippa import FlippaScraper
from .acquire import AcquireScraper
from .empire_flippers import EmpireFlippersScraper
from .businesses_for_sale import BusinessesForSaleScraper
from .business_broker import BusinessBrokerScraper
from .fe_international import FEInternationalScraper
from .loopnet import LoopNetScraper
from database import upsert_listings_bulk

SCRAPER_REGISTRY = {
    "BusinessesForSale": BusinessesForSaleScraper(),
    "BizBuySell": BizBuySellScraper(),
    "Flippa": FlippaScraper(),
    "Acquire.com": AcquireScraper(),
    "Empire Flippers": EmpireFlippersScraper(),
    "BusinessBroker.net": BusinessBrokerScraper(),
    "FE International": FEInternationalScraper(),
    "LoopNet": LoopNetScraper()
}

SCRAPE_JOBS: Dict[str, ScrapeProgress] = {}

class ScraperAggregator:
    @staticmethod
    def get_supported_sources() -> List[str]:
        return list(SCRAPER_REGISTRY.keys())

    @staticmethod
    async def run_scrape_job(task_id: str, request: ScrapeRequest):
        sources_to_scrape = request.sources if request.sources else list(SCRAPER_REGISTRY.keys())
        
        SCRAPE_JOBS[task_id] = ScrapeProgress(
            task_id=task_id,
            status="running",
            progress=5,
            message="Initializing scrapers...",
            found_count=0,
            sources_status={src: "pending" for src in sources_to_scrape}
        )

        all_scraped: List[BusinessListing] = []
        total_sources = len(sources_to_scrape)
        completed_sources = 0

        for source_name in sources_to_scrape:
            scraper = SCRAPER_REGISTRY.get(source_name)
            if not scraper:
                SCRAPE_JOBS[task_id].sources_status[source_name] = "unsupported"
                continue

            SCRAPE_JOBS[task_id].sources_status[source_name] = "scraping"
            SCRAPE_JOBS[task_id].message = f"Scraping listings from {source_name}..."

            try:
                listings = await scraper.scrape(
                    keywords=request.keywords,
                    category=request.category,
                    limit=request.max_results
                )
                all_scraped.extend(listings)
                SCRAPE_JOBS[task_id].sources_status[source_name] = f"completed ({len(listings)} found)"
            except Exception as e:
                print(f"[Aggregator] Error scraping {source_name}: {e}")
                SCRAPE_JOBS[task_id].sources_status[source_name] = f"error: {str(e)[:30]}"

            completed_sources += 1
            progress_pct = int(10 + (completed_sources / max(total_sources, 1)) * 80)
            SCRAPE_JOBS[task_id].progress = progress_pct
            SCRAPE_JOBS[task_id].found_count = len(all_scraped)
            await asyncio.sleep(0.3)

        # Upsert and normalize
        SCRAPE_JOBS[task_id].message = f"Saving {len(all_scraped)} listings to database..."
        saved_count = upsert_listings_bulk(all_scraped)
        
        SCRAPE_JOBS[task_id].progress = 100
        SCRAPE_JOBS[task_id].status = "completed"
        SCRAPE_JOBS[task_id].message = f"Successfully aggregated {saved_count} listings across {completed_sources} marketplace platforms."

    @staticmethod
    def get_job_status(task_id: str) -> Optional[ScrapeProgress]:
        return SCRAPE_JOBS.get(task_id)
