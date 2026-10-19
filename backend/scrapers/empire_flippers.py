from typing import List, Optional
from models import BusinessListing
from .base import BaseScraper

SAMPLE_EMPIRE_DEALS = [
    {
        "title": "Established Display Advertising & Affiliate Site in Outdoor & Camping Gear",
        "description": "Vetted high-margin content empire with over 600 comprehensive buyer guides, field tests, and gear reviews. Monitored through Google Analytics with 85% organic search traffic.",
        "asking_price": 950000.0,
        "cash_flow": 285000.0,
        "gross_revenue": 310000.0,
        "location": "Online / Relocatable",
        "category": "Content & Media",
        "sub_category": "Outdoor Media",
        "is_relocatable": True,
        "inventory_included": False,
        "real_estate_included": False,
        "established_year": 2016,
        "employees": 2,
        "reason_for_selling": "Serial entrepreneur liquidating assets for commercial real estate development",
        "image_url": "https://images.unsplash.com/photo-1504280390367-361c6d9f38f4?auto=format&fit=crop&w=800&q=80",
        "source_url": "https://empireflippers.com/marketplace/"
    },
    {
        "title": "Amazon FBA Brand in Ergonomic Office Furniture & Accessories",
        "description": "Custom designed motorized standing desks and lumbar chairs with trademarked private label brand registered on Amazon US and Canada. Excellent supplier terms and 3PL warehousing in place.",
        "asking_price": 2100000.0,
        "cash_flow": 640000.0,
        "gross_revenue": 3200000.0,
        "location": "Online / Relocatable",
        "category": "E-commerce",
        "sub_category": "Amazon FBA",
        "is_relocatable": True,
        "inventory_included": True,
        "real_estate_included": False,
        "established_year": 2018,
        "employees": 4,
        "reason_for_selling": "Owner looking to retire and pursue philanthropic interests",
        "image_url": "https://images.unsplash.com/photo-1524758631624-e2822e304c36?auto=format&fit=crop&w=800&q=80",
        "source_url": "https://empireflippers.com/marketplace/"
    },
    {
        "title": "Subscription Box & Community for Artisan Coffee Enthusiasts",
        "description": "Over 3,800 active monthly subscribers receiving curated specialty roaster beans. 94% retention rate, active Discord community, and exclusive roasting partnerships.",
        "asking_price": 720000.0,
        "cash_flow": 215000.0,
        "gross_revenue": 980000.0,
        "location": "Online / Relocatable",
        "category": "E-commerce",
        "sub_category": "Subscription Commerce",
        "is_relocatable": True,
        "inventory_included": True,
        "real_estate_included": False,
        "established_year": 2020,
        "employees": 3,
        "reason_for_selling": "Founders pursuing other international ventures",
        "image_url": "https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?auto=format&fit=crop&w=800&q=80",
        "source_url": "https://empireflippers.com/marketplace/"
    }
]

class EmpireFlippersScraper(BaseScraper):
    def __init__(self):
        super().__init__(source_name="Empire Flippers", base_url="https://empireflippers.com")

    async def scrape(self, keywords: Optional[str] = None, category: Optional[str] = None, limit: int = 15) -> List[BusinessListing]:
        results: List[BusinessListing] = []

        for item in SAMPLE_EMPIRE_DEALS:
            if keywords and keywords.lower() not in item["title"].lower() and keywords.lower() not in item["description"].lower():
                continue
            if category and category != "All" and category.lower() not in item["category"].lower():
                continue

            listing = BusinessListing(
                title=item["title"],
                description=item["description"],
                asking_price=item["asking_price"],
                cash_flow=item["cash_flow"],
                gross_revenue=item["gross_revenue"],
                location=item["location"],
                city="Remote",
                state="Online",
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
                is_relocatable=True
            )
            results.append(listing)

        return results[:limit]
