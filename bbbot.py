import webbrowser
import json
import requests
import codecs
import threading
from datetime import datetime

prod_link = "https://www.bestbuy.ca/en-ca/product/"
# 3070 and 80
sku_3k = [15078017, 15038016, 15081879, 15000079, 15000078,
          14953249, 14950588, 14961449, 14953248, 14954116,
          15000077]

sku_ps5 = [14962185, 14962184]

sku_xsx = [14964951]
def strnify(a):
    return [str(s) for s in a]

skus = strnify(sku_3k) + strnify(sku_ps5) + strnify(sku_xsx)


headers = {
    'authority': 'www.bestbuy.ca',
    'pragma': 'no-cache',
    'cache-control': 'no-cache',
    'sec-ch-ua': '"Chromium";v="86", "\\"Not\\\\A;Brand";v="99", "Google Chrome";v="86"',
    'sec-ch-ua-mobile': '?0',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'none',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-dest': 'document',
    'accept-language': 'en-US,en;q=0.9',
    'cookie': ''}

params = (
    ('accept', 'application/vnd.bestbuy.simpleproduct.v1+json'),
    ('accept-language', 'en-CA'),
    ('locations',
     '203|977|617|62|931|927|57|938|965|237|932|943|956|200|202|926|795|916|937|544|910|954|207|233|930|622|245|223|925|985|990|949|959|942'),
    ('postalCode', 'M1M'),
    ('skus', '15078017|15038016|15081879|15000079|15000078|14953249|14950588|14961449|14953248|14954116|15000077|14962185|14962184|14964951'),
)


def bbbot():
    print(datetime.now())
    threading.Timer(15.0, bbbot).start()
    r = requests.get('https://www.bestbuy.ca/ecomm-api/availability/products', headers=headers, params=params)
    j = json.loads(r.text[1:])
    j = j["availabilities"]
    print(skus)

    for item in j:
        sku = item["sku"]
        status = item['shipping']['status']
        if status == "InStock":
            if sku in skus:
                try:
                    print(sku)
                    print(item['shipping']['quantityRemaining'])
                except:
                    print("No Stock")
                url = prod_link + str(sku)
                webbrowser.open(url)
                sku_3k.remove(sku)


bbbot()
