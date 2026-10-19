from typing import List, Optional
from models import BusinessListing
from .base import BaseScraper

SAMPLE_ACQUIRE_DEALS = [
    {
        "title": "B2B AI Customer Support Automation & Agent Platform (Micro-SaaS)",
        "description": "Integrates directly with Zendesk, Intercom, and Freshdesk to resolve 65% of support tickets automatically via fine-tuned LLMs. $24,500 MRR with 110 paying enterprise and mid-market accounts, 92% gross margins, and <2.5% monthly churn.",
        "asking_price": 1200000.0,
        "cash_flow": 260000.0,
        "gross_revenue": 294000.0,
        "location": "Online / Relocatable",
        "category": "SaaS & Software",
        "sub_category": "AI / Customer Tech",
        "is_relocatable": True,
        "inventory_included": False,
        "real_estate_included": False,
        "established_year": 2023,
        "employees": 2,
        "reason_for_selling": "Founders received term sheet for a separate seed-funded frontier AI venture",
        "image_url": "https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&w=800&q=80",
        "source_url": "https://acquire.com/"
    },
    {
        "title": "SEO Keyword Clustering & Programmatic Content Generator Tool",
        "description": "Specialized developer & agency SaaS with 420 active monthly recurring subscriptions ($49-$199/mo). Zero ad spend, grown organically through Twitter and ProductHunt.",
        "asking_price": 620000.0,
        "cash_flow": 185000.0,
        "gross_revenue": 210000.0,
        "location": "Online / Relocatable",
        "category": "SaaS & Software",
        "sub_category": "MarTech SaaS",
        "is_relocatable": True,
        "inventory_included": False,
        "real_estate_included": False,
        "established_year": 2022,
        "employees": 1,
        "reason_for_selling": "Bootstrapped builder seeking liquidity to buy a residential home",
        "image_url": "https://images.unsplash.com/photo-1460925895917-afdab827c52f?auto=format&fit=crop&w=800&q=80",
        "source_url": "https://acquire.com/"
    },
    {
        "title": "Shopify App for Cross-Selling & Tiered Cart Discounts",
        "description": "Featured in Shopify App Store staff picks. Installed on 2,800+ active Shopify stores with 4.9 average review score. Generates steady passive MRR.",
        "asking_price": 490000.0,
        "cash_flow": 140000.0,
        "gross_revenue": 168000.0,
        "location": "Online / Relocatable",
        "category": "SaaS & Software",
        "sub_category": "Shopify Ecosystem",
        "is_relocatable": True,
        "inventory_included": False,
        "real_estate_included": False,
        "established_year": 2021,
        "employees": 1,
        "reason_for_selling": "Portfolio optimization",
        "image_url": "https://images.unsplash.com/photo-1556742049-0a67e5572293?auto=format&fit=crop&w=800&q=80",
        "source_url": "https://acquire.com/"
    },
    {
        "title": "API Backend for Video Processing & Subtitle Transcription",
        "description": "Developer-first API service handling 5M+ API requests monthly with high retention and usage-based billing.",
        "asking_price": 750000.0,
        "cash_flow": 210000.0,
        "gross_revenue": 275000.0,
        "location": "Online / Relocatable",
        "category": "SaaS & Software",
        "sub_category": "Developer Tools",
        "is_relocatable": True,
        "inventory_included": False,
        "real_estate_included": False,
        "established_year": 2022,
        "employees": 2,
        "reason_for_selling": "Partner buyout",
        "image_url": "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?auto=format&fit=crop&w=800&q=80",
        "source_url": "https://acquire.com/"
    }
]

class AcquireScraper(BaseScraper):
    def __init__(self):
        super().__init__(source_name="Acquire.com", base_url="https://acquire.com")

    async def scrape(self, keywords: Optional[str] = None, category: Optional[str] = None, limit: int = 15) -> List[BusinessListing]:
        results: List[BusinessListing] = []

        for item in SAMPLE_ACQUIRE_DEALS:
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
