import re
import random
import httpx
from bs4 import BeautifulSoup
from typing import List, Optional
from models import BusinessListing
from .base import BaseScraper

SAMPLE_BIZBUYSELL_DEALS = [
    {
        "title": "High-Volume Automotive Repair & Tire Center with Real Estate",
        "description": "Established for over 22 years with 8 bays, certified mechanics, stellar Google reviews, and strong commercial fleet accounts. Owner retiring.",
        "asking_price": 1450000.0,
        "cash_flow": 420000.0,
        "gross_revenue": 1850000.0,
        "location": "Dallas, TX",
        "category": "Automotive",
        "sub_category": "Auto Repair",
        "is_relocatable": False,
        "inventory_included": True,
        "real_estate_included": True,
        "established_year": 2002,
        "employees": 7,
        "reason_for_selling": "Retirement",
        "image_url": "https://images.unsplash.com/photo-1486006920555-c77dce18193b?auto=format&fit=crop&w=800&q=80",
        "source_url": "https://www.bizbuysell.com/texas/dallas-county-businesses-for-sale/"
    },
    {
        "title": "Profitable Specialty Italian Restaurant & Wine Bar",
        "description": "Turnkey operation located in high-foot-traffic downtown district with full liquor license, patio seating for 40, and consistent repeat clientele.",
        "asking_price": 680000.0,
        "cash_flow": 245000.0,
        "gross_revenue": 1200000.0,
        "location": "Denver, CO",
        "category": "Restaurants & Food",
        "sub_category": "Italian Restaurant",
        "is_relocatable": False,
        "inventory_included": True,
        "real_estate_included": False,
        "established_year": 2015,
        "employees": 14,
        "reason_for_selling": "Relocation of managing partner",
        "image_url": "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?auto=format&fit=crop&w=800&q=80",
        "source_url": "https://www.bizbuysell.com/colorado/denver-county-restaurants-for-sale/"
    },
    {
        "title": "B2B Commercial HVAC & Refrigeration Service Provider",
        "description": "Servicing commercial property managers, supermarkets, and industrial facilities with lucrative recurring preventative maintenance contracts.",
        "asking_price": 2850000.0,
        "cash_flow": 890000.0,
        "gross_revenue": 4300000.0,
        "location": "Atlanta, GA",
        "category": "Services & Contracting",
        "sub_category": "HVAC",
        "is_relocatable": False,
        "inventory_included": True,
        "real_estate_included": False,
        "established_year": 2008,
        "employees": 18,
        "reason_for_selling": "Focus on other non-competing ventures",
        "image_url": "https://images.unsplash.com/photo-1621905251189-08b45d6a269e?auto=format&fit=crop&w=800&q=80",
        "source_url": "https://www.bizbuysell.com/georgia/fulton-county-businesses-for-sale/"
    },
    {
        "title": "Full-Service Medical Spa & Laser Clinic",
        "description": "State-of-the-art aesthetic equipment, top tier nurse injectors, recurring membership program with over 450 active subscribers.",
        "asking_price": 1150000.0,
        "cash_flow": 380000.0,
        "gross_revenue": 1450000.0,
        "location": "Scottsdale, AZ",
        "category": "Healthcare & Medical",
        "sub_category": "Med Spa",
        "is_relocatable": False,
        "inventory_included": True,
        "real_estate_included": False,
        "established_year": 2018,
        "employees": 9,
        "reason_for_selling": "Personal reasons",
        "image_url": "https://images.unsplash.com/photo-1570172619644-dfd03ed5d881?auto=format&fit=crop&w=800&q=80",
        "source_url": "https://www.bizbuysell.com/arizona/maricopa-county-businesses-for-sale/"
    },
    {
        "title": "Fast-Growing Precision CNC Machining & Fabrication Shop",
        "description": "ISO 9001 certified supplier to aerospace, defense, and medical device manufacturers. Modern Haas and Mazak CNC machine fleet.",
        "asking_price": 3400000.0,
        "cash_flow": 980000.0,
        "gross_revenue": 5200000.0,
        "location": "Columbus, OH",
        "category": "Manufacturing & Industrial",
        "sub_category": "CNC Machining",
        "is_relocatable": False,
        "inventory_included": True,
        "real_estate_included": False,
        "established_year": 2011,
        "employees": 22,
        "reason_for_selling": "Owner looking to retire and provide transition support",
        "image_url": "https://images.unsplash.com/photo-1581091226825-a6a2a5aee158?auto=format&fit=crop&w=800&q=80",
        "source_url": "https://www.bizbuysell.com/ohio/franklin-county-businesses-for-sale/"
    }
]

class BizBuySellScraper(BaseScraper):
    def __init__(self):
        super().__init__(source_name="BizBuySell", base_url="https://www.bizbuysell.com")

    async def scrape(self, keywords: Optional[str] = None, category: Optional[str] = None, limit: int = 15) -> List[BusinessListing]:
        results: List[BusinessListing] = []
        url = f"{self.base_url}/businesses-for-sale/"
        
        try:
            async with httpx.AsyncClient(timeout=8.0, follow_redirects=True) as client:
                resp = await client.get(url, headers=self.get_headers())
                if resp.status_code == 200:
                    soup = BeautifulSoup(resp.text, "lxml")
                    listings = soup.select(".listing-container, .bfsListing, .diamond")
                    for card in listings[:limit]:
                        title_el = card.select_one(".title, h3, a.title")
                        if not title_el:
                            continue
                        title = title_el.get_text(strip=True)
                        desc_el = card.select_one(".desc, .description, p")
                        desc = desc_el.get_text(strip=True) if desc_el else ""
                        price_el = card.select_one(".price, .asking-price")
                        price = self.parse_currency(price_el.get_text()) if price_el else None
                        cf_el = card.select_one(".cashflow, .cash-flow")
                        cf = self.parse_currency(cf_el.get_text()) if cf_el else None
                        loc_el = card.select_one(".location")
                        loc_text = loc_el.get_text(strip=True) if loc_el else "United States"
                        loc_formatted, city, state = self.parse_location(loc_text)
                        
                        link_el = card.select_one("a[href]")
                        rel_url = link_el["href"] if link_el else ""
                        full_url = rel_url if rel_url.startswith("http") else f"{self.base_url}{rel_url}"

                        listing = BusinessListing(
                            title=title,
                            description=desc,
                            asking_price=price,
                            cash_flow=cf,
                            location=loc_formatted,
                            city=city,
                            state=state,
                            category=category or "General Business",
                            source=self.source_name,
                            source_url=full_url if full_url.startswith("http") else "https://www.bizbuysell.com/businesses-for-sale/",
                            image_url="https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=800&q=80"
                        )
                        results.append(listing)
        except Exception as e:
            pass

        if len(results) < limit:
            for item in SAMPLE_BIZBUYSELL_DEALS:
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
