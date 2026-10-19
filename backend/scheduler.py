import asyncio
import datetime
from typing import Optional, Dict, Any
from scrapers.aggregator import ScraperAggregator
from models import ScrapeRequest
from database import record_sync_event, get_latest_sync_event, get_sync_setting, set_sync_setting

class DailyScraperScheduler:
    def __init__(self, interval_hours: float = 24.0):
        self.interval_hours = interval_hours
        self.is_running = False
        self._task: Optional[asyncio.Task] = None
        self.last_run_at: Optional[str] = None
        self.next_run_at: Optional[str] = None
        self.status_message: str = "Daily scheduler initialized."

    def start(self):
        if not self.is_running:
            self.is_running = True
            self._task = asyncio.create_task(self._scheduler_loop())
            print(f"[Scheduler] Daily auto-scraper started (Interval: {self.interval_hours}h).")

    def stop(self):
        self.is_running = False
        if self._task and not self._task.done():
            self._task.cancel()
            print("[Scheduler] Daily auto-scraper stopped.")

    async def _scheduler_loop(self):
        # Check last run from database
        latest = get_latest_sync_event()
        if latest:
            self.last_run_at = latest["timestamp"]
        
        # Calculate next run
        now = datetime.datetime.utcnow()
        if self.last_run_at:
            try:
                last_dt = datetime.datetime.fromisoformat(self.last_run_at)
                next_dt = last_dt + datetime.timedelta(hours=self.interval_hours)
                if next_dt < now:
                    next_dt = now + datetime.timedelta(minutes=1)
                self.next_run_at = next_dt.isoformat()
            except Exception:
                self.next_run_at = (now + datetime.timedelta(hours=self.interval_hours)).isoformat()
        else:
            # If never run, run soon after startup
            self.next_run_at = (now + datetime.timedelta(seconds=15)).isoformat()

        while self.is_running:
            try:
                now = datetime.datetime.utcnow()
                next_dt = datetime.datetime.fromisoformat(self.next_run_at)
                wait_seconds = max(1.0, (next_dt - now).total_seconds())

                self.status_message = f"Next daily update scheduled in {int(wait_seconds // 60)} minutes."
                print(f"[Scheduler] Waiting {wait_seconds:.0f}s until next scheduled daily run ({self.next_run_at}).")
                
                await asyncio.sleep(min(wait_seconds, 60.0))

                # Check if it is time to run
                if datetime.datetime.utcnow() >= next_dt:
                    print("[Scheduler] Triggering scheduled daily scrape across all 8 marketplaces...")
                    self.status_message = "Running daily marketplace sync..."
                    
                    req = ScrapeRequest(
                        sources=ScraperAggregator.get_supported_sources(),
                        max_results=20
                    )
                    task_id = f"daily-cron-{int(datetime.datetime.utcnow().timestamp())}"
                    
                    await ScraperAggregator.run_scrape_job(task_id, req)
                    
                    self.last_run_at = datetime.datetime.utcnow().isoformat()
                    self.next_run_at = (datetime.datetime.utcnow() + datetime.timedelta(hours=self.interval_hours)).isoformat()
                    self.status_message = "Daily update completed successfully."
                    
                    record_sync_event(
                        task_id=task_id,
                        sources=req.sources,
                        status="completed",
                        message=f"Daily auto-sync completed at {self.last_run_at}"
                    )
                    print(f"[Scheduler] Daily scrape complete! Next run scheduled at {self.next_run_at}.")

            except asyncio.CancelledError:
                break
            except Exception as e:
                print(f"[Scheduler] Error during daily cycle: {e}")
                self.status_message = f"Error: {e}"
                await asyncio.sleep(60.0)

    def get_status(self) -> Dict[str, Any]:
        return {
            "is_running": self.is_running,
            "interval_hours": self.interval_hours,
            "last_run_at": self.last_run_at,
            "next_run_at": self.next_run_at,
            "status_message": self.status_message,
        }

scheduler_instance = DailyScraperScheduler(interval_hours=24.0)
