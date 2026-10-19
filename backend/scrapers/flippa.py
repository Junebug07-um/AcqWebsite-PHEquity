import re
from typing import List, Optional
from models import BusinessListing
from .base import BaseScraper

SAMPLE_FLIPPA_DEALS = [
    {
        "title": "Direct-to-Consumer Organic Pet Supplement Brand (Amazon FBA & Shopify)",
        "description": "Custom formulated all-natural dog vitamins and joint chews with over 12,000 Amazon 5-star reviews, strong repeat subscription rate (Subscribe & Save 38%), and verified manufacturer supplier relationships.",
        "asking_price": 875000.0,
        "cash_flow": 310000.0,
        "gross_revenue": 1420000.0,
        "location": "Online / Relocatable",
        "category": "E-commerce",
        "sub_category": "Amazon FBA & DTC",
        "is_relocatable": True,
        "inventory_included": True,
        "real_estate_included": False,
        "established_year": 2019,
        "employees": 2,
        "reason_for_selling": "Founders launching a new B2B logistics tech company",
        "image_url": "https://images.unsplash.com/photo-1583511655857-d19b40a7a54e?auto=format&fit=crop&w=800&q=80",
        "source_url": "https://flippa.com/search?filter[property_type]=ecommerce&filter[status]=open"
    },
    {
        "title": "Authority Review & Affiliate Media Site in Home Automation / Smart Tech",
        "description": "Generates 350,000 monthly organic pageviews purely via SEO with affiliate revenue from Amazon Associates, Impact, and direct sponsor placements. High domain authority (DR 54).",
        "asking_price": 320000.0,
        "cash_flow": 115000.0,
        "gross_revenue": 138000.0,
        "location": "Online / Relocatable",
        "category": "Content & Media",
        "sub_category": "Affiliate Website",
        "is_relocatable": True,
        "inventory_included": False,
        "real_estate_included": False,
        "established_year": 2017,
        "employees": 1,
        "reason_for_selling": "Portfolio rebalancing",
        "image_url": "https://images.unsplash.com/photo-1558002038-1055907df827?auto=format&fit=crop&w=800&q=80",
        "source_url": "https://flippa.com/search?filter[property_type]=website&filter[status]=open"
    },
    {
        "title": "iOS & Android Fitness Habit Tracker & Intermittent Fasting App",
        "description": "Over 400,000 lifetime downloads with 24,000 monthly active users and steady in-app subscription revenue. Highly rated on the App Store (4.8 stars).",
        "asking_price": 540000.0,
        "cash_flow": 195000.0,
        "gross_revenue": 260000.0,
        "location": "Online / Relocatable",
        "category": "Mobile Apps",
        "sub_category": "Health & Fitness App",
        "is_relocatable": True,
        "inventory_included": False,
        "real_estate_included": False,
        "established_year": 2020,
        "employees": 1,
        "reason_for_selling": "Solo developer transitioning to full-time AI research",
        "image_url": "https://images.unsplash.com/photo-1510519138195-068d828884bb?auto=format&fit=crop&w=800&q=80",
        "source_url": "https://flippa.com/search?filter[property_type]=app&filter[status]=open"
    },
    {
        "title": "High-Ticket Dropshipping Store in Commercial Kitchen Equipment",
        "description": "Average order value of $1,850 with exclusive US distributor agreements. Fully automated supplier order dispatching and low return rate.",
        "asking_price": 460000.0,
        "cash_flow": 165000.0,
        "gross_revenue": 1650000.0,
        "location": "Online / Relocatable",
        "category": "E-commerce",
        "sub_category": "High-Ticket Dropshipping",
        "is_relocatable": True,
        "inventory_included": False,
        "real_estate_included": False,
        "established_year": 2021,
        "employees": 2,
        "reason_for_selling": "Owner focusing on commercial real estate portfolio",
        "image_url": "https://images.unsplash.com/photo-1556910103-1c02745aae4d?auto=format&fit=crop&w=800&q=80",
        "source_url": "https://flippa.com/search?filter[property_type]=ecommerce&filter[status]=open"
    }
]

class FlippaScraper(BaseScraper):
    def __init__(self):
        super().__init__(source_name="Flippa", base_url="https://flippa.com")

    async def scrape(self, keywords: Optional[str] = None, category: Optional[str] = None, limit: int = 15) -> List[BusinessListing]:
        results: List[BusinessListing] = []

        for item in SAMPLE_FLIPPA_DEALS:
            if keywords and keywords.lower() not in item["title"].lower() and keywords.lower() not in item["description"].lower():
                continue
            if category and category != "All" and category.lower() not in item["category"].lower():
                continue

            search_url = f"{self.base_url}/search?query={keywords.replace(' ', '+')}" if keywords else item["source_url"]

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
                source_url=search_url,
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
