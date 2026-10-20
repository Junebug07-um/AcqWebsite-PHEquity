import re
import httpx
from bs4 import BeautifulSoup
from typing import List, Optional
from datetime import datetime
from models import BusinessListing
from .base import BaseScraper

class BusinessesForSaleScraper(BaseScraper):
    def __init__(self):
        super().__init__(source_name="BusinessesForSale", base_url="https://us.businessesforsale.com")

    async def scrape(self, keywords: Optional[str] = None, category: Optional[str] = None, limit: int = 35) -> List[BusinessListing]:
        results: List[BusinessListing] = []
        
        # Build page list to crawl (page 1, 2, 3)
        page_urls = []
        if keywords:
            kw = keywords.replace(' ', '+')
            page_urls.append(f"{self.base_url}/us/search/businesses-for-sale?keywords={kw}")
            page_urls.append(f"{self.base_url}/us/search/businesses-for-sale-2?keywords={kw}")
        else:
            page_urls.append(f"{self.base_url}/us/search/businesses-for-sale")
            page_urls.append(f"{self.base_url}/us/search/businesses-for-sale-2")
            page_urls.append(f"{self.base_url}/us/search/businesses-for-sale-3")
            
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
        }

        try:
            async with httpx.AsyncClient(timeout=12.0, follow_redirects=True) as client:
                for target_url in page_urls:
                    if len(results) >= limit:
                        break
                    try:
                        resp = await client.get(target_url, headers=headers)
                        if resp.status_code != 200:
                            continue
                            
                        soup = BeautifulSoup(resp.text, "html.parser")
                        cards = soup.select("div.result")
                        
                        for card in cards:
                            if len(results) >= limit:
                                break
                                
                            title_el = card.select_one("h2 a, h3 a, .title a")
                            if not title_el:
                                continue
                                
                            title = title_el.get_text(strip=True)
                            rel_url = title_el.get("href", "")
                            
                            # Filter out franchise opportunities / promotional ads
                            if "/franchises/" in rel_url or "franchise opportunity" in title.lower():
                                continue
                                
                            full_url = rel_url if rel_url.startswith("http") else f"{self.base_url}{rel_url}"
                            
                            # Extract table details
                            rows_text = {}
                            for tr in card.select("tr"):
                                th = tr.select_one("th")
                                td = tr.select_one("td")
                                if th and td:
                                    key = th.get_text(strip=True).replace(":", "")
                                    val = td.get_text(strip=True)
                                    rows_text[key] = val
                                    
                            loc_text = rows_text.get("Location", "United States")
                            loc_formatted, city, state = self.parse_location(loc_text)
                            
                            # Asking Price
                            raw_price = rows_text.get("Asking Price", "")
                            price = self.parse_currency(raw_price) if "$" in raw_price else None
                            
                            # Cash flow
                            raw_cf = rows_text.get("Cash Flow", "")
                            cf = self.parse_currency(raw_cf) if "$" in raw_cf else None
                            
                            # Revenue
                            raw_rev = rows_text.get("Revenue", "")
                            rev = self.parse_currency(raw_rev) if "$" in raw_rev else None
                            
                            # Skip listings that have neither price nor cash flow (unhelpful placeholders)
                            if not price and not cf:
                                continue
                            
                            desc_el = card.select_one(".desc, p")
                            desc = desc_el.get_text(strip=True) if desc_el else ""
                            desc = re.sub(r"More details.*$", "", desc).strip()
                            
                            # Infer category
                            inferred_cat = "General Business"
                            title_lower = (title + " " + desc).lower()
                            if any(k in title_lower for k in ["saas", "software", "tech", "platform", "app", "website", "online"]):
                                inferred_cat = "SaaS & Software"
                            elif any(k in title_lower for k in ["amazon", "ecommerce", "e-commerce", "shopify", "store", "vendor", "retail"]):
                                inferred_cat = "E-commerce"
                            elif any(k in title_lower for k in ["restaurant", "bar", "cafe", "coffee", "food", "bakery", "deli"]):
                                inferred_cat = "Restaurants & Food"
                            elif any(k in title_lower for k in ["contract", "roofing", "hvac", "plumbing", "waste", "cleaning", "landscap"]):
                                inferred_cat = "Services & Contracting"
                            elif any(k in title_lower for k in ["medical", "health", "spa", "dental", "clinic", "chiro"]):
                                inferred_cat = "Healthcare & Medical"
                            elif any(k in title_lower for k in ["auto", "car", "wash", "tire", "dealership"]):
                                inferred_cat = "Automotive"
                            elif any(k in title_lower for k in ["manufactur", "metal", "cnc", "industrial"]):
                                inferred_cat = "Manufacturing & Industrial"
                                
                            # Image fallback
                            img_el = card.select_one("img")
                            img_url = img_el.get("src") if img_el and img_el.get("src") and not "blank" in img_el.get("src", "") else None
                            if not img_url:
                                img_url = "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=800&q=80"
                                
                            listing = BusinessListing(
                                title=title,
                                description=desc,
                                asking_price=price,
                                cash_flow=cf,
                                gross_revenue=rev,
                                location=loc_formatted,
                                city=city,
                                state=state,
                                category=category if category and category != "All" else inferred_cat,
                                source=self.source_name,
                                source_url=full_url,
                                image_url=img_url,
                                is_relocatable="online" in loc_formatted.lower() or "amazon" in title_lower or "saas" in title_lower or "shopify" in title_lower,
                                scraped_at=datetime.utcnow().isoformat()
                            )
                            results.append(listing)
                    except Exception as err:
                        print(f"[BusinessesForSaleScraper] Page fetch notice: {err}")
                        continue
        except Exception as e:
            print(f"[BusinessesForSaleScraper] Error: {e}")
            
        return results[:limit]
