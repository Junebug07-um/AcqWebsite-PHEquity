import os
import sqlite3
from database import init_db
from seed_data import seed_database
import asyncio
from scrapers.aggregator import ScraperAggregator
from models import ScrapeRequest

def reset():
    db_path = os.path.join(os.path.dirname(__file__), "businesses.db")
    if os.path.exists(db_path):
        os.remove(db_path)
        print("Removed old database file.")

    init_db()
    seed_database()

    # Run initial scrape across all 8 sources
    async def initial_sync():
        req = ScrapeRequest(
            sources=['BusinessesForSale', 'BizBuySell', 'Flippa', 'Acquire.com', 'Empire Flippers', 'BusinessBroker.net', 'FE International', 'LoopNet'],
            max_results=10
        )
        task_id = "initial-setup-sync"
        await ScraperAggregator.run_scrape_job(task_id, req)
        print("Completed initial setup sync.")

    asyncio.run(initial_sync())

    # Verify all listings have valid URL
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM listings")
    cnt = cursor.fetchone()[0]
    print(f"Database successfully re-initialized with {cnt} listings.")
    
    cursor.execute("SELECT DISTINCT source, COUNT(*) FROM listings GROUP BY source")
    for row in cursor.fetchall():
        print(f"  • {row[0]}: {row[1]} listings")

    conn.close()

if __name__ == "__main__":
    reset()
