from typing import List, Optional
from models import BusinessListing
from .base import BaseScraper

SAMPLE_FE_DEALS = [
    {
        "title": "B2B Enterprise HR & Employee Engagement SaaS",
        "description": "Comprehensive employee onboarding, performance management, and continuous feedback SaaS used by over 320 mid-market companies. High Net Revenue Retention (114%) and low churn.",
        "asking_price": 4800000.0,
        "cash_flow": 1350000.0,
        "gross_revenue": 2100000.0,
        "location": "Online / Relocatable",
        "category": "SaaS & Software",
        "sub_category": "HR Tech",
        "source_url": "https://feinternational.com/buy-a-website/",
        "image_url": "https://images.unsplash.com/photo-1522071820081-009f0129c71c?auto=format&fit=crop&w=800&q=80",
        "established_year": 2018,
        "employees": 8,
        "is_relocatable": True,
        "reason_for_selling": "Founder seeking exit after 6 years of growth"
    },
    {
        "title": "Authority Tech Media & Developer Portal with Enterprise Sponsorships",
        "description": "High-traffic tech news and developer tutorials portal with 1.2M monthly unique visits. Monetized via high-CPM direct ad contracts with AWS, MongoDB, and Datadog.",
        "asking_price": 2650000.0,
        "cash_flow": 780000.0,
        "gross_revenue": 1150000.0,
        "location": "Online / Relocatable",
        "category": "Content & Media",
        "sub_category": "Developer Media",
        "source_url": "https://feinternational.com/buy-a-website/",
        "image_url": "https://images.unsplash.com/photo-1504384308090-c894fdcc538d?auto=format&fit=crop&w=800&q=80",
        "established_year": 2015,
        "employees": 4,
        "is_relocatable": True,
        "reason_for_selling": "Portfolio rebalancing"
    }
]

class FEInternationalScraper(BaseScraper):
    def __init__(self):
        super().__init__(source_name="FE International", base_url="https://feinternational.com")

    async def scrape(self, keywords: Optional[str] = None, category: Optional[str] = None, limit: int = 15) -> List[BusinessListing]:
        results: List[BusinessListing] = []

        for item in SAMPLE_FE_DEALS:
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
                reason_for_selling=item.get("reason_for_selling"),
                is_relocatable=True
            )
            results.append(listing)

        return results[:limit]
