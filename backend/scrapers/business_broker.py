import re
from typing import List, Optional
from models import BusinessListing
from .base import BaseScraper

SAMPLE_BUSINESSBROKER_DEALS = [
    {
        "title": "Commercial Landscape Maintenance & Irrigation Fleet with Recurring Contracts",
        "description": "Commercial landscaping enterprise servicing HOA communities, corporate campuses, and retail centers. Includes 9 crew trucks, commercial zero-turn mowers, and $1.4M annual recurring maintenance contracts.",
        "asking_price": 1850000.0,
        "cash_flow": 520000.0,
        "gross_revenue": 2100000.0,
        "location": "Tampa, FL",
        "category": "Services & Contracting",
        "sub_category": "Landscaping",
        "source_url": "https://www.businessbroker.net/businesses-for-sale.aspx?q=landscaping+florida",
        "image_url": "https://images.unsplash.com/photo-1557429287-b2e26467fc2b?auto=format&fit=crop&w=800&q=80",
        "established_year": 2010,
        "employees": 19,
        "inventory_included": True,
        "real_estate_included": False,
        "reason_for_selling": "Owner relocating to family ranch",
        "is_relocatable": False
    },
    {
        "title": "Specialty Medical Diagnostic Imaging Center with Accredited MRI & CT",
        "description": "High-margin imaging facility in medical corridor with established physician referral network, Medicare/Medicaid accreditation, and state-of-the-art Siemens 3T MRI.",
        "asking_price": 3200000.0,
        "cash_flow": 890000.0,
        "gross_revenue": 3400000.0,
        "location": "Houston, TX",
        "category": "Healthcare & Medical",
        "sub_category": "Diagnostic Imaging",
        "source_url": "https://www.businessbroker.net/businesses-for-sale.aspx?q=medical+texas",
        "image_url": "https://images.unsplash.com/photo-1516549655169-df83a0774514?auto=format&fit=crop&w=800&q=80",
        "established_year": 2012,
        "employees": 11,
        "inventory_included": True,
        "real_estate_included": False,
        "reason_for_selling": "Partnership dissolution due to retirement",
        "is_relocatable": False
    },
    {
        "title": "Established High-Volume Wholesale Bakery & Distribution Hub",
        "description": "Supplying artisanal breads, buns, and pastries to over 80 regional supermarket chains, hotels, and restaurant groups. 24,000 sq ft production facility with automated baking lines.",
        "asking_price": 4100000.0,
        "cash_flow": 1250000.0,
        "gross_revenue": 7800000.0,
        "location": "Chicago, IL",
        "category": "Manufacturing & Industrial",
        "sub_category": "Food Production",
        "source_url": "https://www.businessbroker.net/businesses-for-sale.aspx?q=bakery+illinois",
        "image_url": "https://images.unsplash.com/photo-1509440159596-0249088772ff?auto=format&fit=crop&w=800&q=80",
        "established_year": 2004,
        "employees": 34,
        "inventory_included": True,
        "real_estate_included": False,
        "reason_for_selling": "Owner looking to retire and provide 1 year advisory transition",
        "is_relocatable": False
    }
]

class BusinessBrokerScraper(BaseScraper):
    def __init__(self):
        super().__init__(source_name="BusinessBroker.net", base_url="https://www.businessbroker.net")

    async def scrape(self, keywords: Optional[str] = None, category: Optional[str] = None, limit: int = 15) -> List[BusinessListing]:
        results: List[BusinessListing] = []

        for item in SAMPLE_BUSINESSBROKER_DEALS:
            if keywords and keywords.lower() not in item["title"].lower() and keywords.lower() not in item["description"].lower():
                continue
            if category and category != "All" and category.lower() not in item["category"].lower():
                continue

            loc_formatted, city, state = self.parse_location(item["location"])
            # Generate valid search URL matching query
            source_url = f"{self.base_url}/businesses-for-sale.aspx"
            if keywords:
                source_url = f"{self.base_url}/businesses-for-sale.aspx?q={keywords.replace(' ', '+')}"

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
                source_url=item.get("source_url", source_url),
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
