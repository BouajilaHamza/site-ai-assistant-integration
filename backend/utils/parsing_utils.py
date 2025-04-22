import requests
from bs4 import BeautifulSoup
import os
import logging

logger = logging.getLogger(__name__)

def extract_sitemap_links(base_url_or_path: str, visited=None) -> list:
    """
    Extract all URLs from a sitemap, including nested sitemaps.

    Args:
        base_url_or_path (str): The base URL of the website or the path to a local sitemap file.
        visited (set): A set of already visited sitemap URLs or file paths to avoid duplication.

    Returns:
        list: A list of all extracted URLs.
    """
    if visited is None:
        visited = set()

    urls = []
    try:
        # Check if the input is a local file path
        if os.path.isfile(base_url_or_path):
            logger.debug(f"Processing local sitemap file: {base_url_or_path}")
            with open(base_url_or_path, 'r', encoding='utf-8') as file:
                soup = BeautifulSoup(file, features="xml")
        else:
            # Check if base_url_or_path already contains "sitemap" or ".xml"
            if "sitemap" in base_url_or_path or base_url_or_path.endswith(".xml"):
                sitemap_urls = [base_url_or_path]
            else:
                # Attempt to fetch sitemap.xml or sitemaps.xml
                sitemap_urls = [base_url_or_path.rstrip("/") + suffix for suffix in ["/sitemap.xml", "/sitemaps.xml"]]

            for sitemap_url in sitemap_urls:
                logger.debug(f"Trying sitemap: {sitemap_url}")
                response = requests.get(sitemap_url)
                if response.status_code == 200:
                    logger.debug(f"Found sitemap: {sitemap_url}")
                    response.raise_for_status()
                    soup = BeautifulSoup(response.text, features="xml")
                    break
            else:
                logger.debug(f"No sitemap found. Adding base URL: {base_url_or_path}")
                if base_url_or_path not in visited:
                    visited.add(base_url_or_path)
                    urls.append(base_url_or_path)
                return urls

        # Process the sitemap content
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

    except requests.RequestException as e:
        logger.error(f"Error fetching sitemap {base_url_or_path}: {e}")
    except Exception as e:
        logger.error(f"Error processing sitemap {base_url_or_path}: {e}")

    return urls
