import requests 
from bs4 import BeautifulSoup
import json
import extruct
from w3lib.html import get_base_url
from requests.api import head

urls = {
    '1': "https://www.kotsovolos.gr/SearchDisplay?searchTerm=xbox&filters=filters/m/Microsoft&pageSize=60&storeId=10151",
    '1-1': "https://www.kotsovolos.gr/SearchDisplay?searchTerm=xbox%20series&filters=filters/m/Microsoft&pageSize=60&storeId=10151",
    '2': "https://www.plaisio.gr/search?query=xbox%20series&page=1&configure%5BhitsPerPage%5D=3&configure%5Bdistinct%5D=true&configure%5BclickAnalytics%5D=true&configure%5Banalytics%5D=true&configure%5BanalyticsTags%5D%5B0%5D=Desktop&configure%5BenableABTest%5D=true&configure%5BuserToken%5D=a28d0a56-11cf-47f6-9f20-1204864f1d41&indices%5Bquery_suggestions%5D%5Bconfigure%5D%5BhitsPerPage%5D=9&indices%5Bquery_suggestions%5D%5Bconfigure%5D%5Bdistinct%5D=true&indices%5Bquery_suggestions%5D%5Bconfigure%5D%5BclickAnalytics%5D=true&indices%5Bquery_suggestions%5D%5Bconfigure%5D%5Banalytics%5D=true&indices%5Bquery_suggestions%5D%5Bconfigure%5D%5BanalyticsTags%5D%5B0%5D=Desktop&indices%5Bquery_suggestions%5D%5Bconfigure%5D%5BenableABTest%5D=true&indices%5Bquery_suggestions%5D%5Bconfigure%5D%5BuserToken%5D=a28d0a56-11cf-47f6-9f20-1204864f1d41&indices%5Bquery_suggestions%5D%5Bpage%5D=1&indices%5Bquery_suggestions%5D%5BrefinementList%5D%5Bpage%5D=1&indices%5Bblog_posts%5D%5Bconfigure%5D%5BhitsPerPage%5D=4&indices%5Bblog_posts%5D%5Bconfigure%5D%5Bdistinct%5D=true&indices%5Bblog_posts%5D%5Bconfigure%5D%5BclickAnalytics%5D=true&indices%5Bblog_posts%5D%5Bconfigure%5D%5Banalytics%5D=true&indices%5Bblog_posts%5D%5Bconfigure%5D%5BanalyticsTags%5D%5B0%5D=Desktop&indices%5Bblog_posts%5D%5Bconfigure%5D%5BenableABTest%5D=true&indices%5Bblog_posts%5D%5Bconfigure%5D%5BuserToken%5D=a28d0a56-11cf-47f6-9f20-1204864f1d41&indices%5Bblog_posts%5D%5Bpage%5D=1&indices%5Bblog_posts%5D%5BrefinementList%5D%5Bpage%5D=1&refinementList%5Bbrand%5D%5B0%5D=Microsoft&hitsPerPage=48"
}

headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '3600',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
}
 
r = requests.get(urls['1'], headers=headers)
soup = BeautifulSoup(r.content, "html.parser") 

# print(soup.title.string)

# ldJson = soup.find('script', type='application/ld+json') 
# parsedJson = json.loads(ldJson.contents[0])
# print(ldJson.contents[0])
# print([actor['name'] for actor in parsedJson['actors']])



def extract_metadata(url):
    """Extract all metadata present in the page and return a dictionary of metadata lists. 
    
    Args:
        url (string): URL of page from which to extract metadata. 
    
    Returns: 
        metadata (dict): Dictionary of json-ld, microdata, and opengraph lists. 
        Each of the lists present within the dictionary contains multiple dictionaries.
    """

    my_UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.54 Safari/537.36"
    headers = {}
    headers['User-Agent'] = my_UA
    
    r = requests.get(url, headers=headers)
    base_url = get_base_url(r.text, r.url)

    metadata = extruct.extract(r.text, 
                               base_url=base_url,
                               uniform=True,
                               syntaxes=['json-ld',
                                         'microdata',
                                         'opengraph'])
    return metadata

def get_dictionary_by_key_value(dictionary, target_key, target_value):
    """Return a dictionary that contains a target key value pair. 
    
    Args:
        dictionary: Metadata dictionary containing lists of other dictionaries.
        target_key: Target key to search for within a dictionary inside a list. 
        target_value: Target value to search for within a dictionary inside a list. 
    
    Returns:
        target_dictionary: Target dictionary that contains target key value pair. 
    """
    
    for key in dictionary:
        if len(dictionary[key]) > 0:
            for item in dictionary[key]:
                if item[target_key] == target_value:
                    return item


tmp = ''
products = list()
ldJson = soup.findAll('script', type='application/ld+json')
for scriptTag in ldJson:
    parsedJson = json.loads(scriptTag.contents[0])
    # parsedJson = scriptTag.contents[0]
    # print(scriptTag.contents[0])
    # if 'json-ld' in parsedJson:
    # print('===============================================')
    # print(parsedJson)
    if parsedJson['@type'] == "WebSite":
        tmp += parsedJson['name'] + ':\n'
        tmp += '======================================\n\n'
    
    if 'offers' in parsedJson:
        if 'series' in parsedJson['name'].lower():
            products.append({
                'name': parsedJson['name'],
                'price': parsedJson['offers'][0]['priceSpecification']['price'],
                'url': parsedJson['offers'][0]['url']
            })
            
            # print(pr)
            # tmp += pr['name'] + '\t' + pr['price'] + '\n'
            # print('\n')
# print(parsedJson)
# print([actor['name'] for actor in parsedJson['actors']]) 

# print(tmp)

for prod in products:
    # print(prod['name'] + '\t' + prod['price'] + '\n')
    prod_metadata=extract_metadata(prod['url'])
    # print(prod_metadata)
    p = get_dictionary_by_key_value(prod_metadata, "@type", "Product")
    availability = p['offers'][0]['availability']
    if 'OutOfStock' in availability:
        available = 'NO'
    else:
        available = "YES"
    tmp += p['name'] + '\t' + p['offers'][0]['price'] + '\t' + available + '\n'

print(tmp)