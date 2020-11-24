import requests
import webbrowser
import json
import requests
import codecs
import threading
from datetime import datetime

cookies = {
}

headers = {
    'authority': 'www.walmart.ca',
    'pragma': 'no-cache',
    'cache-control': 'no-cache',
    'sec-ch-ua': '"Chromium";v="86", "\\"Not\\\\A;Brand";v="99", "Google Chrome";v="86"',
    'accept': 'application/json',
    'content-type': 'application/json',
    'sec-ch-ua-mobile': '?0',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
    'origin': 'https://www.walmart.ca',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://www.walmart.ca/search?q=playstation+5+console&f=10000041&c=10012+6000201024440+6000202239918&price=0-1000',
    'accept-language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
}

data = '{"fsa":"M1M","products":[{"productId":"6000201790922","skuIds":["6000201790923"]},{"productId":"6000202198823","skuIds":["6000202198824"]},{"productId":"6000202198562","skuIds":["6000202198563"]},{"productId":"6000202283428","skuIds":["6000202283429"]},{"productId":"6000202282463","skuIds":["6000202282464"]}],"lang":"en","pricingStoreId":"3053","fulfillmentStoreId":"3195","experience":"whiteGM"}'

def wmbot():
    print(datetime.now())
    threading.Timer(10.0, wmbot).start()
    r = requests.post('https://www.walmart.ca/api/bsp/v2/price-offer', headers=headers, cookies=cookies, data=data)

    j = r.json()

    offers = j['offers']

    base_url = "https://www.walmart.ca/en/ip/"
    for sku in offers:
        if offers[sku]['sellerId'] == '0':
            if offers[sku]['gmAvailability'] != "OutOfStock":
                print("Success!")
                print(sku)
                url = base_url + sku
                webbrowser.open(url)

wmbot()