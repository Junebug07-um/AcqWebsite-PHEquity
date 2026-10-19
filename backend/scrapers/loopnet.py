from typing import List, Optional
from models import BusinessListing
from .base import BaseScraper

SAMPLE_LOOPNET_DEALS = [
    {
        "title": "Prime Highway Gas Station, Convenience Store & Quick-Serve Drive-Thru",
        "description": "High-margin branded gas station pumping 130,000 gallons/mo with 3,800 sq ft convenience store and leased national fast food drive-thru tenant. Real estate included on 1.4 acre signalized corner lot.",
        "asking_price": 4200000.0,
        "cash_flow": 920000.0,
        "gross_revenue": 5400000.0,
        "location": "Orlando, FL",
        "category": "Automotive",
        "sub_category": "Gas Station & C-Store",
        "source_url": "https://www.loopnet.com/search/commercial-real-estate/for-sale/",
        "image_url": "https://images.unsplash.com/photo-1545454675-3531b543be5d?auto=format&fit=crop&w=800&q=80",
        "established_year": 2005,
        "employees": 12,
        "real_estate_included": True,
        "inventory_included": True,
        "reason_for_selling": "Retirement",
        "is_relocatable": False
    },
    {
        "title": "Self-Storage Facility with 350 Climate-Controlled Units & Expansion Land",
        "description": "94% occupied modern storage facility with automated kiosk, gate access, security cameras, and approved permits to build additional 120 units on adjacent 0.8 acre parcel.",
        "asking_price": 5400000.0,
        "cash_flow": 1180000.0,
        "gross_revenue": 1420000.0,
        "location": "San Antonio, TX",
        "category": "Services & Contracting",
        "sub_category": "Self Storage",
        "source_url": "https://www.loopnet.com/search/commercial-real-estate/for-sale/",
        "image_url": "https://images.unsplash.com/photo-1586528116311-ad8dd3c8310d?auto=format&fit=crop&w=800&q=80",
        "established_year": 2017,
        "employees": 2,
        "real_estate_included": True,
        "inventory_included": False,
        "reason_for_selling": "Fund lifecycle completion",
        "is_relocatable": False
    }
]

class LoopNetScraper(BaseScraper):
    def __init__(self):
        super().__init__(source_name="LoopNet", base_url="https://www.loopnet.com")

    async def scrape(self, keywords: Optional[str] = None, category: Optional[str] = None, limit: int = 15) -> List[BusinessListing]:
        results: List[BusinessListing] = []

        for item in SAMPLE_LOOPNET_DEALS:
            if keywords and keywords.lower() not in item["title"].lower() and keywords.lower() not in item["description"].lower():
                continue
            if category and category != "All" and category.lower() not in item["category"].lower():
                continue

            loc_formatted, city, state = self.parse_location(item["location"])
            listing = BusinessListing(
                title=item["title"],
                description=item["description"],
                asking_price=item["asking_price"],
                cash_flow=item["cash_flow"],
                gross_revenue=item["gross_revenue"],
                location=loc_formatted,
                city=city,
                state=state,
                category=item["category"],
                sub_category=item.get("sub_category"),
                source=self.source_name,
                source_url=item["source_url"],
                image_url=item["image_url"],
                established_year=item.get("established_year"),
                employees=item.get("employees"),
                inventory_included=item.get("inventory_included"),
                real_estate_included=item.get("real_estate_included"),
                reason_for_selling=item.get("reason_for_selling"),
                is_relocatable=item.get("is_relocatable", False)
            )
            results.append(listing)

        return results[:limit]
