import sqlite3
import json
import os
from typing import List, Optional, Dict, Any, Tuple
from models import BusinessListing, FilterParams, MarketStats

DB_PATH = os.path.join(os.path.dirname(__file__), "businesses.db")

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS listings (
        id TEXT PRIMARY KEY,
        title TEXT NOT NULL,
        description TEXT,
        asking_price REAL,
        cash_flow REAL,
        gross_revenue REAL,
        ebitda REAL,
        location TEXT,
        city TEXT,
        state TEXT,
        country TEXT,
        is_relocatable INTEGER,
        category TEXT,
        sub_category TEXT,
        source TEXT NOT NULL,
        source_url TEXT UNIQUE NOT NULL,
        image_url TEXT,
        established_year INTEGER,
        employees INTEGER,
        inventory_included INTEGER,
        real_estate_included INTEGER,
        reason_for_selling TEXT,
        scraped_at TEXT,
        price_to_cashflow_multiple REAL,
        price_to_revenue_multiple REAL,
        raw_data TEXT
    );
    """)

    cursor.execute("CREATE INDEX IF NOT EXISTS idx_asking_price ON listings(asking_price);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_cash_flow ON listings(cash_flow);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_category ON listings(category);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_source ON listings(source);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_location ON listings(location);")

    # Watchlist table for user favorites
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS watchlist (
        listing_id TEXT PRIMARY KEY,
        added_at TEXT,
        notes TEXT,
        FOREIGN KEY(listing_id) REFERENCES listings(id) ON DELETE CASCADE
    );
    """)

    # Scheduler sync logs table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sync_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task_id TEXT,
        timestamp TEXT,
        sources TEXT,
        status TEXT,
        message TEXT
    );
    """)

    # App settings key-value store
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS settings (
        key TEXT PRIMARY KEY,
        value TEXT
    );
    """)

    conn.commit()
    conn.close()

def upsert_listing(listing: BusinessListing) -> bool:
    listing.calculate_multiples()
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute("""
        INSERT INTO listings (
            id, title, description, asking_price, cash_flow, gross_revenue, ebitda,
            location, city, state, country, is_relocatable, category, sub_category,
            source, source_url, image_url, established_year, employees,
            inventory_included, real_estate_included, reason_for_selling, scraped_at,
            price_to_cashflow_multiple, price_to_revenue_multiple, raw_data
        ) VALUES (
            ?, ?, ?, ?, ?, ?, ?,
            ?, ?, ?, ?, ?, ?, ?,
            ?, ?, ?, ?, ?,
            ?, ?, ?, ?,
            ?, ?, ?
        )
        ON CONFLICT(source_url) DO UPDATE SET
            title=excluded.title,
            description=excluded.description,
            asking_price=excluded.asking_price,
            cash_flow=excluded.cash_flow,
            gross_revenue=excluded.gross_revenue,
            location=excluded.location,
            category=excluded.category,
            image_url=excluded.image_url,
            price_to_cashflow_multiple=excluded.price_to_cashflow_multiple,
            price_to_revenue_multiple=excluded.price_to_revenue_multiple,
            scraped_at=excluded.scraped_at;
        """, (
            listing.id, listing.title, listing.description, listing.asking_price, listing.cash_flow, listing.gross_revenue, listing.ebitda,
            listing.location, listing.city, listing.state, listing.country, 1 if listing.is_relocatable else 0,
            listing.category, listing.sub_category, listing.source, listing.source_url, listing.image_url,
            listing.established_year, listing.employees,
            1 if listing.inventory_included else (0 if listing.inventory_included is False else None),
            1 if listing.real_estate_included else (0 if listing.real_estate_included is False else None),
            listing.reason_for_selling, listing.scraped_at,
            listing.price_to_cashflow_multiple, listing.price_to_revenue_multiple,
            json.dumps(listing.model_dump())
        ))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error upserting listing {listing.title}: {e}")
        return False
    finally:
        conn.close()

def upsert_listings_bulk(listings: List[BusinessListing]) -> int:
    inserted_count = 0
    for item in listings:
        if upsert_listing(item):
            inserted_count += 1
    return inserted_count

def row_to_listing(row: sqlite3.Row) -> BusinessListing:
    return BusinessListing(
        id=row["id"],
        title=row["title"],
        description=row["description"] or "",
        asking_price=row["asking_price"],
        cash_flow=row["cash_flow"],
        gross_revenue=row["gross_revenue"],
        ebitda=row["ebitda"],
        location=row["location"] or "Unknown",
        city=row["city"],
        state=row["state"],
        country=row["country"] or "USA",
        is_relocatable=bool(row["is_relocatable"]),
        category=row["category"] or "General Business",
        sub_category=row["sub_category"],
        source=row["source"],
        source_url=row["source_url"],
        image_url=row["image_url"],
        established_year=row["established_year"],
        employees=row["employees"],
        inventory_included=bool(row["inventory_included"]) if row["inventory_included"] is not None else None,
        real_estate_included=bool(row["real_estate_included"]) if row["real_estate_included"] is not None else None,
        reason_for_selling=row["reason_for_selling"],
        scraped_at=row["scraped_at"] or "",
        price_to_cashflow_multiple=row["price_to_cashflow_multiple"],
        price_to_revenue_multiple=row["price_to_revenue_multiple"]
    )

def query_listings(params: FilterParams) -> Tuple[List[BusinessListing], int]:
    conn = get_db()
    cursor = conn.cursor()

    conditions = []
    values = []

    if params.q:
        q_wildcard = f"%{params.q.strip()}%"
        conditions.append("(title LIKE ? OR description LIKE ? OR location LIKE ? OR category LIKE ?)")
        values.extend([q_wildcard, q_wildcard, q_wildcard, q_wildcard])

    if params.min_price is not None:
        conditions.append("asking_price >= ?")
        values.append(params.min_price)

    if params.max_price is not None:
        conditions.append("asking_price <= ?")
        values.append(params.max_price)

    if params.min_cash_flow is not None:
        conditions.append("cash_flow >= ?")
        values.append(params.min_cash_flow)

    if params.max_cash_flow is not None:
        conditions.append("cash_flow <= ?")
        values.append(params.max_cash_flow)

    if params.min_revenue is not None:
        conditions.append("gross_revenue >= ?")
        values.append(params.min_revenue)

    if params.max_revenue is not None:
        conditions.append("gross_revenue <= ?")
        values.append(params.max_revenue)

    if params.category and params.category != "All":
        conditions.append("category = ?")
        values.append(params.category)

    if params.source and params.source != "All":
        conditions.append("source = ?")
        values.append(params.source)

    if params.location and params.location != "All":
        loc_wildcard = f"%{params.location.strip()}%"
        conditions.append("(location LIKE ? OR state LIKE ? OR city LIKE ?)")
        values.extend([loc_wildcard, loc_wildcard, loc_wildcard])

    if params.is_relocatable is not None:
        conditions.append("is_relocatable = ?")
        values.append(1 if params.is_relocatable else 0)

    if params.max_multiple is not None:
        conditions.append("price_to_cashflow_multiple <= ? AND price_to_cashflow_multiple > 0")
        values.append(params.max_multiple)

    if getattr(params, "only_priced", False):
        conditions.append("asking_price IS NOT NULL AND asking_price > 0")

    if getattr(params, "max_age_days", None):
        import datetime
        cutoff = (datetime.datetime.utcnow() - datetime.timedelta(days=params.max_age_days)).isoformat()
        conditions.append("scraped_at >= ?")
        values.append(cutoff)

    where_clause = ""
    if conditions:
        where_clause = "WHERE " + " AND ".join(conditions)


    # Count total matching
    count_sql = f"SELECT COUNT(*) FROM listings {where_clause}"
    cursor.execute(count_sql, values)
    total_count = cursor.fetchone()[0]

    # Order by
    sort_map = {
        "price_asc": "asking_price ASC NULLS LAST",
        "price_desc": "asking_price DESC NULLS LAST",
        "cash_flow_desc": "cash_flow DESC NULLS LAST",
        "multiple_asc": "price_to_cashflow_multiple ASC NULLS LAST",
        "revenue_desc": "gross_revenue DESC NULLS LAST",
        "newest": "scraped_at DESC, rowid DESC"
    }
    order_clause = sort_map.get(params.sort_by, "scraped_at DESC")

    offset = (params.page - 1) * params.page_size
    select_sql = f"""
        SELECT * FROM listings
        {where_clause}
        ORDER BY {order_clause}
        LIMIT ? OFFSET ?
    """
    cursor.execute(select_sql, values + [params.page_size, offset])
    rows = cursor.fetchall()

    listings = [row_to_listing(r) for r in rows]
    conn.close()
    return listings, total_count

def get_listing_by_id(listing_id: str) -> Optional[BusinessListing]:
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM listings WHERE id = ?", (listing_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return row_to_listing(row)
    return None

def get_market_statistics() -> MarketStats:
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            COUNT(*) as total,
            AVG(asking_price) as avg_price,
            AVG(cash_flow) as avg_cf,
            AVG(CASE WHEN price_to_cashflow_multiple > 0 AND price_to_cashflow_multiple < 20 THEN price_to_cashflow_multiple END) as avg_mult
        FROM listings
    """)
    stats_row = cursor.fetchone()
    total = stats_row["total"] or 0
    avg_price = round(stats_row["avg_price"] or 0, 2)
    avg_cf = round(stats_row["avg_cf"] or 0, 2)
    avg_mult = round(stats_row["avg_mult"] or 0, 2)

    # Median asking price
    cursor.execute("""
        SELECT asking_price FROM listings
        WHERE asking_price IS NOT NULL AND asking_price > 0
        ORDER BY asking_price
        LIMIT 1 OFFSET (SELECT COUNT(*) FROM listings WHERE asking_price > 0) / 2
    """)
    median_row = cursor.fetchone()
    median_price = median_row[0] if median_row and median_row[0] else avg_price

    # Category distribution
    cursor.execute("SELECT category, COUNT(*) as cnt FROM listings GROUP BY category ORDER BY cnt DESC")
    cat_dist = {r["category"]: r["cnt"] for r in cursor.fetchall() if r["category"]}

    # Source distribution
    cursor.execute("SELECT source, COUNT(*) as cnt FROM listings GROUP BY source ORDER BY cnt DESC")
    src_dist = {r["source"]: r["cnt"] for r in cursor.fetchall() if r["source"]}

    # Top locations
    cursor.execute("SELECT location, COUNT(*) as cnt FROM listings GROUP BY location ORDER BY cnt DESC LIMIT 10")
    loc_dist = {r["location"]: r["cnt"] for r in cursor.fetchall() if r["location"]}

    conn.close()
    return MarketStats(
        total_listings=total,
        avg_asking_price=avg_price,
        median_asking_price=median_price,
        avg_cash_flow=avg_cf,
        avg_multiple=avg_mult,
        category_distribution=cat_dist,
        source_distribution=src_dist,
        top_locations=loc_dist
    )

def toggle_watchlist(listing_id: str, notes: str = "") -> bool:
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT listing_id FROM watchlist WHERE listing_id = ?", (listing_id,))
    exists = cursor.fetchone()
    if exists:
        cursor.execute("DELETE FROM watchlist WHERE listing_id = ?", (listing_id,))
        saved = False
    else:
        import datetime
        cursor.execute("INSERT INTO watchlist (listing_id, added_at, notes) VALUES (?, ?, ?)",
                       (listing_id, datetime.datetime.utcnow().isoformat(), notes))
        saved = True
    conn.commit()
    conn.close()
    return saved

def get_watchlist_ids() -> List[str]:
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT listing_id FROM watchlist")
    rows = cursor.fetchall()
    conn.close()
    return [r[0] for r in rows]

def record_sync_event(task_id: str, sources: List[str], status: str, message: str):
    conn = get_db()
    cursor = conn.cursor()
    import datetime
    now_str = datetime.datetime.utcnow().isoformat()
    cursor.execute(
        "INSERT INTO sync_logs (task_id, timestamp, sources, status, message) VALUES (?, ?, ?, ?, ?)",
        (task_id, now_str, json.dumps(sources), status, message)
    )
    conn.commit()
    conn.close()

def get_latest_sync_event() -> Optional[Dict[str, Any]]:
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM sync_logs ORDER BY id DESC LIMIT 1")
    row = cursor.fetchone()
    conn.close()
    if row:
        return dict(row)
    return None

def set_sync_setting(key: str, value: str):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)", (key, value))
    conn.commit()
    conn.close()

def get_sync_setting(key: str, default: Optional[str] = None) -> Optional[str]:
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT value FROM settings WHERE key = ?", (key,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return row[0]
    return default

def delete_listing_by_id(listing_id: str) -> bool:
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM listings WHERE id = ?", (listing_id,))
    cursor.execute("DELETE FROM watchlist WHERE listing_id = ?", (listing_id,))
    conn.commit()
    deleted = cursor.rowcount > 0
    conn.close()
    return deleted

def purge_stale_listings(days: int = 14, keep_watchlist: bool = True) -> int:
    conn = get_db()
    cursor = conn.cursor()
    import datetime
    cutoff = (datetime.datetime.utcnow() - datetime.timedelta(days=days)).isoformat()
    if keep_watchlist:
        cursor.execute("DELETE FROM listings WHERE scraped_at < ? AND id NOT IN (SELECT listing_id FROM watchlist)", (cutoff,))
    else:
        cursor.execute("DELETE FROM listings WHERE scraped_at < ?", (cutoff,))
    deleted = cursor.rowcount
    conn.commit()
    conn.close()
    return deleted

def clear_all_listings(keep_watchlist: bool = True) -> int:
    conn = get_db()
    cursor = conn.cursor()
    if keep_watchlist:
        cursor.execute("DELETE FROM listings WHERE id NOT IN (SELECT listing_id FROM watchlist)")
    else:
        cursor.execute("DELETE FROM listings")
        cursor.execute("DELETE FROM watchlist")
    deleted = cursor.rowcount
    conn.commit()
    conn.close()
    return deleted


