import requests 
from bs4 import BeautifulSoup
import json
import extruct
from w3lib.html import get_base_url
from requests.api import head

urls = {
    '1': "https://www.skroutz.gr/s/22413644/Microsoft-Xbox-Series-X.html",
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
ldJson = soup.findAll('li', class_="card js-product-card")
# with open("skroutz.html", "w") as p:
#     p.write(ldJson)
# ldJson = soup.findAll('span', class_="availability instock")
# for pr in ldJson:
    
# for scriptTag in ldJson[0]:
#     parsedJson = json.loads(scriptTag.contents[0])
#     print(parsedJson)

# for scriptTag in ldJson:
#     parsedJson = json.loads(scriptTag.contents[0])
#     if parsedJson['@type'] == "WebSite":
#         tmp += parsedJson['name'] + ':\n'
#         tmp += '======================================\n\n'
    
#     if 'offers' in parsedJson:
#         if 'series' in parsedJson['name'].lower():
#             products.append({
#                 'name': parsedJson['name'],
#                 'price': parsedJson['offers'][0]['priceSpecification']['price'],
#                 'url': parsedJson['offers'][0]['url']
#             })
            

# for prod in products:
#     # print(prod['name'] + '\t' + prod['price'] + '\n')
#     prod_metadata=extract_metadata(prod['url'])
#     # print(prod_metadata)
#     p = get_dictionary_by_key_value(prod_metadata, "@type", "Product")
#     availability = p['offers'][0]['availability']
#     if 'OutOfStock' in availability:
#         available = 'NO'
#     else:
#         available = "YES"
#     tmp += p['name'] + '\t' + p['offers'][0]['price'] + '\t' + available + '\n'

# print(tmp)