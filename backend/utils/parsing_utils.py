import requests
from bs4 import BeautifulSoup

def extract_sitemap_links(base_url: str, visited=None) -> list:
    """
    Extract all URLs from a sitemap, including nested sitemaps.

    Args:
        base_url (str): The base URL of the website.
        visited (set): A set of already visited sitemap URLs to avoid duplication.

    Returns:
        list: A list of all extracted URLs.
    """
    if visited is None:
        visited = set()

    urls = []
    try:
        # Check if base_url already contains "sitemap" or ".xml"
        if "sitemap" in base_url or base_url.endswith(".xml"):
            sitemap_urls = [base_url]
        else:
            # Attempt to fetch sitemap.xml or sitemaps.xml
            sitemap_urls = [base_url.rstrip("/") + suffix for suffix in ["/sitemap.xml", "/sitemaps.xml"]]

        for sitemap_url in sitemap_urls:
            print(f"Trying sitemap: {sitemap_url}")
            response = requests.get(sitemap_url)
            if response.status_code == 200:
                print(f"Found sitemap: {sitemap_url}")
                response.raise_for_status()
                soup = BeautifulSoup(response.text, features="xml")
                for loc in soup.find_all('loc'):
                    link = loc.text.strip()
                    if link in visited:
                        continue
                    visited.add(link)
                    if "sitemap" in link or link.endswith(".xml"):
                        # Recursively process nested sitemaps
                        urls.extend(extract_sitemap_links(link, visited))
                    else:
                        urls.append(link)
                return urls  # Return if a valid sitemap is found

        # If no sitemap is found, treat base_url as a regular URL
        print(f"No sitemap found. Adding base URL: {base_url}")
        if base_url not in visited:
            visited.add(base_url)
            urls.append(base_url)

    except requests.RequestException as e:
        print(f"Error fetching sitemap {base_url}: {e}")
    except Exception as e:
        print(f"Error processing sitemap {base_url}: {e}")

    return urls
