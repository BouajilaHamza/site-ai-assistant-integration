import requests
from bs4 import BeautifulSoup



# New helper function to extract links from sitemap.xml
def extract_sitemap_links(base_url: str) -> list:
    sitemap_url = base_url.rstrip("/") + "/sitemap.xml"
    try:
        r = requests.get(sitemap_url)
        if r.status_code == 200:
            soup = BeautifulSoup(r.text,features="xml")    
            return [loc.text.replace("\r\n", "").strip() for loc in soup.find_all('loc')]
    except Exception as e:
        print(f"Error extracting sitemap: {e}")
        return []
