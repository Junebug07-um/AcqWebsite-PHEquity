import httpx
import sqlite3

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
}

def verify_and_clean_db():
    import os
    db_path = os.path.join(os.path.dirname(__file__), "businesses.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    
    # 1. Delete all legacy dummy IDs that contain fake /101, /102, etc.
    cursor.execute("""
        DELETE FROM listings 
        WHERE source_url LIKE '%/101' 
           OR source_url LIKE '%/102' 
           OR source_url LIKE '%/103' 
           OR source_url LIKE '%/104' 
           OR source_url LIKE '%/105'
           OR source_url LIKE '%/1182390%'
           OR source_url LIKE '%/b2b-ai-customer-support-platform'
           OR source_url LIKE '%/seo-keyword-clustering-saas'
           OR source_url LIKE '%/shopify-cross-sell-app'
           OR source_url LIKE '%/video-processing-api'
           OR source_url LIKE '%-6549%'
    """)
    conn.commit()
    print("Deleted legacy placeholder rows.")

    cursor.execute("SELECT id, title, source, source_url FROM listings")
    rows = cursor.fetchall()
    print(f"Remaining active listings in DB: {len(rows)}")

    with httpx.Client(timeout=10.0, follow_redirects=True) as client:
        for r in rows:
            url = r[3]
            try:
                resp = client.get(url, headers=headers)
                print(f"[{resp.status_code}] {r[2]}: {url}")
            except Exception as e:
                print(f"[ERR] {r[2]}: {url} -> {e}")

    conn.close()

if __name__ == '__main__':
    verify_and_clean_db()
