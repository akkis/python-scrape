from pprint import pprint
import requests
import extruct
from w3lib.html import get_base_url

# pp = pprint.PrettyPrinter(indent=2)


def scrape(url):
    """Parse structured data from a target page."""
    html = get_html(url)
    metadata = get_metadata(html, url)
    pprint(metadata, indent=2, width=150)
    return metadata


def get_html(url):
    """ Get raw HTML from URL """
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Max-Age': '3600',
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
    }

    req = requests.get(url, headers=headers)

    return req.text

def get_metadata(html: bytes, url: str):
    """Fetch JSON-LD structured data."""
    metadata = extruct.extract(
        html,
        base_url=get_base_url(url),
        syntaxes=['json-ld'],
        uniform=True
    )['json-ld']

    if bool(metadata) and isinstance(metadata, list):
        metadata=metadata[1]

    return metadata


# url="https://scrapeme.live/shop/"
# url="https://hackersandslackers.com/scrape-metadata-json-ld/"
url="https://www.germanos.gr/product/gaming/consoles/xbox-series-consoles/xbox-series-s-512gb/?productId=20398487"
scrape(url)
