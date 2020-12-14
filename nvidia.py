check_stock_exists = 'https://api.nvidia.partners/edge/product/search?page=1&limit=9&locale=en-us&category=GPU'
check_stock = 'https://api-prod.nvidia.com/direct-sales-shop/DR/products/en_us/CAD/'
a2c = 'https://store.nvidia.com/store/nvidia/en_US/buy/productID.{}/clearCart.yes/nextPage.QuickBuyCartPage'
cart = 'https://store.nvidia.com/store?Action=DisplayPage&Env=BASE&Locale=en_US&SiteID=nvidia&id=QuickBuyCartPage'
import webbrowser
import json
import requests
import codecs
import threading
from datetime import datetime
import beepy
from telegram import telegram_send
from requests_html import HTMLSession

def check_3060():
    print(datetime.now())
    threading.Timer(15.0, check_3060).start()

    r = requests.get(check_stock_exists)
    j = r.json()
    p = j["searchedProducts"]["productDetails"]
    for item in p:
        name = item["displayName"]
        print(name)
        if "3060" in name:
            print(item)
            id = item['digitialRiverID']
            if id != '':
                print(id)
                telegram_send(id)
                beepy.beep()
                a2c_link = a2c.format(id)
                webbrowser.open(a2c_link)
                webbrowser.open(cart)
                telegram_send(a2c_link)
                telegram_send(cart)
                break
check_3060()

