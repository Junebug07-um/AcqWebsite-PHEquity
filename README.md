# DealFlowHub: Business-for-Sale Scraper & Aggregator Prototype

A modern full-stack web application designed to scrape, aggregate, and analyze business-for-sale listings across top online marketplaces (**BizBuySell**, **Flippa**, **Acquire.com**, and **Empire Flippers**).

---

## 🌟 Key Features

1. **Multi-Source Web Scraping & Aggregation Engine**:
   - Modular scrapers targeting Main Street brokerages, digital assets, SaaS startups, and e-commerce brands.
   - Live background scraper job runner with real-time progress tracking and status indicators.
   - Built-in data normalizer for pricing, cash flow (SDE), gross revenue, and valuation multiples.

2. **Advanced Multi-Facet Filtering**:
   - **Industry / Category**: E-commerce, SaaS & Software, Restaurants & Food, Automotive, Services & Contracting, Healthcare, Manufacturing, Media & Content.
   - **Asking Price & Cash Flow**: Quick brackets ($100k-$500k, $500k-$1.5M, $1.5M-$3M, $3M+) and custom range sliders.
   - **Valuation Multiple (Price/SDE)**: Deep value (<2.5x), standard (<3.5x), growth (<5.0x).
   - **Location & Mobility**: Filter by state/city or isolate 100% Online / Relocatable opportunities.
   - **Marketplace Platform Switcher**: Filter by BizBuySell, Flippa, Acquire.com, or Empire Flippers.

3. **Deal Insights & Financial Modeling**:
   - Market intelligence KPI metrics (Average Price, Median Price, Average Cash Flow, Average Multiple).
   - Comprehensive Deal Details modal with asset inclusions (Inventory, Real Estate) and broker links.
   - Built-in **SBA 7(a) Acquisition & ROI Calculator** (Calculates required down payment, monthly debt service, Debt Service Coverage Ratio DSCR, and cash-on-cash ROI).
   - Watchlist & Bookmarking drawer.

---

## 🛠️ Tech Stack

- **Backend**: Python 3.11, FastAPI, BeautifulSoup4, HTTPX, SQLite, Pydantic
- **Frontend**: React 18, TypeScript, Vite, Tailwind CSS, Lucide Icons

---

## 🚀 Quick Start Instructions

### Method 1: Launch Everything (One Command)
```bash
python start_app.py
```

### Method 2: Run Separately

#### 1. Start Backend:
```bash
cd backend
python -m uvicorn main:app --reload --port 8000
```
- API Docs: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

#### 2. Start Frontend:
```bash
cd frontend
npm run dev
```
- Web Application: [http://localhost:5173](http://localhost:5173)

---

## 📡 API Endpoints

- `GET /api/listings`: Query business listings with pagination, search, and multi-parameter filters.
- `GET /api/listings/{id}`: Detailed business listing profile.
- `GET /api/stats`: Market metrics and category distribution.
- `GET /api/filters/metadata`: Available filter facets.
- `POST /api/scrape`: Trigger live multi-source web scraping.
- `GET /api/scrape/{task_id}`: Real-time progress and logs for active scraping job.
- `GET /api/watchlist`: List saved business deals.
- `POST /api/watchlist/{id}`: Toggle bookmark for a deal.
