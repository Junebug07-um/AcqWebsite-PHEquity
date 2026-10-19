import httpx
from bs4 import BeautifulSoup
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
}

r = httpx.get('https://us.businessesforsale.com/us/search/businesses-for-sale', headers=headers, timeout=10.0, follow_redirects=True)
soup = BeautifulSoup(r.text, 'html.parser')
cards = soup.select('div.result')

for card in cards[:6]:
    title_el = card.select_one('h2 a, h3 a')
    title = title_el.get_text(strip=True) if title_el else ''
    url = title_el['href'] if title_el and 'href' in title_el.attrs else ''
    
    loc_row = card.select_one('tr.t-loc td')
    loc = loc_row.get_text(strip=True) if loc_row else 'USA'
    
    # Financial rows
    price_row = card.select_one('tr.t-p td, .price, span.price')
    price_text = price_row.get_text(strip=True) if price_row else ''
    
    # All tr rows
    rows_text = {tr.select_one('th').get_text(strip=True): tr.select_one('td').get_text(strip=True) for tr in card.select('tr') if tr.select_one('th') and tr.select_one('td')}
    
    desc_el = card.select_one('.desc, p')
    desc = desc_el.get_text(strip=True) if desc_el else ''
    
    print("---------------------------------")
    print("TITLE:", title)
    print("URL:", url)
    print("LOC:", loc)
    print("ROWS:", rows_text)
