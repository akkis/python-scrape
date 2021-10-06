# import pandas as pd
import extruct
import requests
from w3lib.html import get_base_url
from datetime import datetime
import urllib.request
import json

# timeout = 10
# socket.setdefaulttimeout(timeout) 

WEBHOOK = 'https://maker.ifttt.com/trigger/xbox_found/with/key/lsmK-M6cf4Hxiq1WU6Yez_RrFV82NKpxnPI6wc2X2jj'
values = {}

# url = "https://www.kotsovolos.gr/SearchDisplay?searchTerm=xbox&storeId=10151&filters=filters/m/Microsoft"

# Xbox Series X
url = "https://www.germanos.gr/product/gaming/consoles/xbox-series-consoles/xbox-series-x-1tb/?productId=20398488"

# Xbox Series S
#url = "https://www.germanos.gr/product/gaming/consoles/xbox-series-consoles/xbox-series-s-512gb/?productId=20398487"

#PS5
#url = "https://www.germanos.gr/product/gaming/consoles/ps5-consoles/playstation-5/?productId=20398154"

#PS2 Digital
#url = "https://www.germanos.gr/product/gaming/consoles/ps5-consoles/playstation-5-digital-edition/?productId=20398155"

def build_data(val1, val2, val3):
    values['value1'] = val1
    values['value2'] = val2
    values['value3'] = val3
    return values

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


metadata = extract_metadata(url)
s = json.dumps(metadata)
# print(type(s))

# with open("file.json", "w") as p:
#     p.write(s)


product = get_dictionary_by_key_value(metadata, "@type", "Product")
name = product['name']
price = product['offers']['price']
availability = product['offers']['availability']

if 'OutOfStock' in availability:
    available='NO'
else:
    available="YES"

now = datetime.now()
print(now.strftime("%d/%m/%Y %H:%M:%S"), name, price, available)
# print("Price:", price)
# print("Availability:", availability)
# print("\n")

# result = re.search(r'/bock/b', availability)


if available == "YES":
    values = build_data(url, price, available)
    data = urllib.parse.urlencode(values)
    data = data.encode('ascii')

    # print('Sending webhook...')
    
    # Seding webhook
    req = urllib.request.Request(WEBHOOK, data)
    urllib.request.urlopen(req)


