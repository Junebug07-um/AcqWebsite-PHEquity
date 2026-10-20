from typing import List
from models import BusinessListing
from database import init_db, upsert_listings_bulk

SEED_LISTINGS: List[dict] = [
    # 1. Main Street & Brick-and-Mortar
    {
        "title": "Prime Express Exterior Car Wash & Detailing Center",
        "description": "High-traffic location on major arterial corridor with 120ft tunnel, top-of-the-line MacNeil equipment, 18 self-serve vacuum stations, and over 1,400 active monthly unlimited wash club members.",
        "asking_price": 2750000.0,
        "cash_flow": 680000.0,
        "gross_revenue": 1450000.0,
        "ebitda": 710000.0,
        "location": "Tampa, FL",
        "city": "Tampa",
        "state": "FL",
        "country": "USA",
        "is_relocatable": False,
        "category": "Automotive",
        "sub_category": "Car Wash",
        "source": "BizBuySell",
        "source_url": "https://www.bizbuysell.com/florida/hillsborough-county-businesses-for-sale/",
        "image_url": "https://images.unsplash.com/photo-1520340356584-f9917d1eea6f?auto=format&fit=crop&w=800&q=80",
        "established_year": 2016,
        "employees": 8,
        "inventory_included": True,
        "real_estate_included": True,
        "reason_for_selling": "Owner diversifying into multifamily real estate"
    },
    {
        "title": "Fully Absentee-Owned Card/Coin Laundromat with Modern Electrolux Machines",
        "description": "Modern laundromat with 42 washers and 48 stacked dryers (all under 4 years old). Hybrid card & mobile app payment system, automated locking doors, surveillance cameras, and full remote management.",
        "asking_price": 795000.0,
        "cash_flow": 265000.0,
        "gross_revenue": 480000.0,
        "location": "Charlotte, NC",
        "city": "Charlotte",
        "state": "NC",
        "country": "USA",
        "is_relocatable": False,
        "category": "Services & Contracting",
        "sub_category": "Laundromat",
        "source": "BizBuySell",
        "source_url": "https://www.bizbuysell.com/north-carolina/mecklenburg-county-businesses-for-sale/",
        "image_url": "https://images.unsplash.com/photo-1545173168-9f1947eebb7f?auto=format&fit=crop&w=800&q=80",
        "established_year": 2020,
        "employees": 2,
        "inventory_included": True,
        "real_estate_included": False,
        "reason_for_selling": "Owner relocating out of state"
    },
    {
        "title": "Artisanal Specialty Bakery & Coffee Roastery",
        "description": "Beloved local brand featured in regional culinary magazines. Sells wholesale sourdough and pastries to 35 local grocery stores and specialty cafes, plus high-margin retail store.",
        "asking_price": 525000.0,
        "cash_flow": 190000.0,
        "gross_revenue": 890000.0,
        "location": "Austin, TX",
        "city": "Austin",
        "state": "TX",
        "country": "USA",
        "is_relocatable": False,
        "category": "Restaurants & Food",
        "sub_category": "Bakery & Cafe",
        "source": "BizBuySell",
        "source_url": "https://www.bizbuysell.com/texas/travis-county-businesses-for-sale/",
        "image_url": "https://images.unsplash.com/photo-1509440159596-0249088772ff?auto=format&fit=crop&w=800&q=80",
        "established_year": 2017,
        "employees": 11,
        "inventory_included": True,
        "real_estate_included": False,
        "reason_for_selling": "Founder moving to manage family estate"
    },
    {
        "title": "Turnkey 24/7 Fitness Club & Strength Training Center",
        "description": "Franchise territory with 1,250 active recurring monthly gym members. Fully equipped with Hammer Strength, Rogue, and Life Fitness equipment. Keycard access system.",
        "asking_price": 650000.0,
        "cash_flow": 220000.0,
        "gross_revenue": 620000.0,
        "location": "Nashville, TN",
        "city": "Nashville",
        "state": "TN",
        "country": "USA",
        "is_relocatable": False,
        "category": "Healthcare & Medical",
        "sub_category": "Fitness Center",
        "source": "BizBuySell",
        "source_url": "https://www.bizbuysell.com/tennessee/davidson-county-businesses-for-sale/",
        "image_url": "https://images.unsplash.com/photo-1534438327276-14e5300c3a48?auto=format&fit=crop&w=800&q=80",
        "established_year": 2018,
        "employees": 4,
        "inventory_included": True,
        "real_estate_included": False,
        "reason_for_selling": "Owner pursuing corporate career"
    },

    # 2. SaaS & Tech Startups
    {
        "title": "B2B AI Document Extraction & Invoice Reconciliation SaaS",
        "description": "Proprietary OCR and LLM-powered engine that automatically parses multi-page PDF invoices, bills of lading, and freight documentation for 3PL logistics and accounting firms. $41,000 MRR, zero customer concentration risk.",
        "asking_price": 1950000.0,
        "cash_flow": 410000.0,
        "gross_revenue": 492000.0,
        "location": "Online / Relocatable",
        "city": "Remote",
        "state": "Online",
        "country": "USA",
        "is_relocatable": True,
        "category": "SaaS & Software",
        "sub_category": "AI / Enterprise Tools",
        "source": "Acquire.com",
        "source_url": "https://acquire.com/",
        "image_url": "https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&w=800&q=80",
        "established_year": 2022,
        "employees": 3,
        "inventory_included": False,
        "real_estate_included": False,
        "reason_for_selling": "Founders seeking full liquidity after 3 years bootstrapping"
    },
    {
        "title": "Cloud Monitoring & Kubernetes Cost Optimization Platform",
        "description": "Helps engineering teams reduce AWS & GCP compute bills by 30-50% via intelligent autoscaling and spot instance orchestration. 85 enterprise clients with average contract value of $9,200/yr.",
        "asking_price": 3100000.0,
        "cash_flow": 720000.0,
        "gross_revenue": 820000.0,
        "location": "Online / Relocatable",
        "city": "Remote",
        "state": "Online",
        "country": "USA",
        "is_relocatable": True,
        "category": "SaaS & Software",
        "sub_category": "DevOps & Cloud",
        "source": "Acquire.com",
        "source_url": "https://acquire.com/",
        "image_url": "https://images.unsplash.com/photo-1558494949-ef010cbdcc31?auto=format&fit=crop&w=800&q=80",
        "established_year": 2021,
        "employees": 4,
        "inventory_included": False,
        "real_estate_included": False,
        "reason_for_selling": "Strategic exit for engineering founders"
    },
    {
        "title": "No-Code Form Builder & Lead Enrichment Tool",
        "description": "Embeddable form builder that enriches incoming leads with LinkedIn and Clearbit data in real-time. Over 6,200 free tier users and 480 paying pro subscribers.",
        "asking_price": 580000.0,
        "cash_flow": 165000.0,
        "gross_revenue": 195000.0,
        "location": "Online / Relocatable",
        "city": "Remote",
        "state": "Online",
        "country": "USA",
        "is_relocatable": True,
        "category": "SaaS & Software",
        "sub_category": "MarTech SaaS",
        "source": "Acquire.com",
        "source_url": "https://acquire.com/",
        "image_url": "https://images.unsplash.com/photo-1507238691740-187a5b1d37b8?auto=format&fit=crop&w=800&q=80",
        "established_year": 2023,
        "employees": 1,
        "inventory_included": False,
        "real_estate_included": False,
        "reason_for_selling": "Solo founder working on new project"
    },

    # 3. E-Commerce & Consumer Brands
    {
        "title": "Premium Ergonomic Home Office & Sit-Stand Desk DTC Brand",
        "description": "High-growth e-commerce brand with $3.4M in trailing 12-month revenue. Custom wooden desk tops sourced sustainably with strong margins and low return rate (2.1%). Over 35,000 email subscribers.",
        "asking_price": 2400000.0,
        "cash_flow": 710000.0,
        "gross_revenue": 3400000.0,
        "location": "Online / Relocatable",
        "city": "Remote",
        "state": "Online",
        "country": "USA",
        "is_relocatable": True,
        "category": "E-commerce",
        "sub_category": "DTC Home Goods",
        "source": "Empire Flippers",
        "source_url": "https://empireflippers.com/marketplace/",
        "image_url": "https://images.unsplash.com/photo-1518455027359-f3f8164ba6bd?auto=format&fit=crop&w=800&q=80",
        "established_year": 2018,
        "employees": 5,
        "inventory_included": True,
        "real_estate_included": False,
        "reason_for_selling": "Founders pursuing other international business interests"
    },
    {
        "title": "Specialty Japanese Matcha & Ceremonial Tea Brand (Amazon + DTC)",
        "description": "Direct farm partnerships in Uji and Shizuoka, Japan. Certified Organic by USDA. 4.9-star average rating on Amazon with $115,000 monthly sales and 42% re-order rate on Shopify store.",
        "asking_price": 1150000.0,
        "cash_flow": 375000.0,
        "gross_revenue": 1380000.0,
        "location": "Online / Relocatable",
        "city": "Remote",
        "state": "Online",
        "country": "USA",
        "is_relocatable": True,
        "category": "E-commerce",
        "sub_category": "Food & Beverage",
        "source": "Flippa",
        "source_url": "https://flippa.com/search?filter[property_type]=ecommerce",
        "image_url": "https://images.unsplash.com/photo-1576092768241-dec231879fc3?auto=format&fit=crop&w=800&q=80",
        "established_year": 2019,
        "employees": 2,
        "inventory_included": True,
        "real_estate_included": False,
        "reason_for_selling": "Owner ready to retire"
    },

    # 4. Contracting & Commercial
    {
        "title": "Commercial Roofing & Waterproofing Contractor with Government Contracts",
        "description": "Multi-generational commercial roofing contractor with bonded municipal contracts, school district partnerships, and industrial plant maintenance agreements. Over $1.8M in contracted backlog for next 9 months.",
        "asking_price": 3850000.0,
        "cash_flow": 1150000.0,
        "gross_revenue": 6200000.0,
        "location": "Phoenix, AZ",
        "city": "Phoenix",
        "state": "AZ",
        "country": "USA",
        "is_relocatable": False,
        "category": "Services & Contracting",
        "sub_category": "Commercial Roofing",
        "source": "BizBuySell",
        "source_url": "https://www.bizbuysell.com/arizona/maricopa-county-businesses-for-sale/",
        "image_url": "https://images.unsplash.com/photo-1632759145351-1d592919f522?auto=format&fit=crop&w=800&q=80",
        "established_year": 1998,
        "employees": 28,
        "inventory_included": True,
        "real_estate_included": False,
        "reason_for_selling": "Planned retirement; general manager willing to stay"
    },
    {
        "title": "Custom Architectural Metal Fabrication & Powder Coating Plant",
        "description": "Fabricating custom ornamental iron railings, laser-cut gates, and commercial building facades. Equipped with fiber laser cutter, 6-axis press brakes, and large conveyorized powder coating line.",
        "asking_price": 2600000.0,
        "cash_flow": 740000.0,
        "gross_revenue": 3900000.0,
        "location": "Indianapolis, IN",
        "city": "Indianapolis",
        "state": "IN",
        "country": "USA",
        "is_relocatable": False,
        "category": "Manufacturing & Industrial",
        "sub_category": "Metal Fabrication",
        "source": "BizBuySell",
        "source_url": "https://www.bizbuysell.com/indiana/marion-county-businesses-for-sale/",
        "image_url": "https://images.unsplash.com/photo-1504917599217-d4dc5ebe6122?auto=format&fit=crop&w=800&q=80",
        "established_year": 2007,
        "employees": 16,
        "inventory_included": True,
        "real_estate_included": False,
        "reason_for_selling": "Owner looking to retire and provide 6 months consulting"
    },

    # 5. Media & Content
    {
        "title": "Niche B2B Cybersecurity Newsletter & Podcast Network",
        "description": "Reaches 78,000 Chief Information Security Officers (CISOs) and enterprise security engineers weekly with 46% open rate. Sponsored by Okta, CrowdStrike, and Cloudflare at $4,500 per issue slot.",
        "asking_price": 890000.0,
        "cash_flow": 310000.0,
        "gross_revenue": 420000.0,
        "location": "Online / Relocatable",
        "city": "Remote",
        "state": "Online",
        "country": "USA",
        "is_relocatable": True,
        "category": "Content & Media",
        "sub_category": "Newsletter / Media",
        "source": "Flippa",
        "source_url": "https://flippa.com/search?filter[property_type]=website",
        "image_url": "https://images.unsplash.com/photo-1550751827-4bd374c3f58b?auto=format&fit=crop&w=800&q=80",
        "established_year": 2020,
        "employees": 2,
        "inventory_included": False,
        "real_estate_included": False,
        "reason_for_selling": "Founder focusing on venture capital syndicate"
    }
]

def seed_database(force: bool = False):
    init_db()
    from database import get_db
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM listings")
    count = cursor.fetchone()[0]
    conn.close()
    if count > 0 and not force:
        print(f"[Seed] Database already has {count} listings. Skipping seed data insertion.")
        return
    listings = [BusinessListing(**item) for item in SEED_LISTINGS]
    inserted = upsert_listings_bulk(listings)
    print(f"[Seed] Successfully seeded {inserted} business listings into SQLite database.")


if __name__ == "__main__":
    seed_database()
