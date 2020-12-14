oos_xpath = '//*[@id="prodMain"]/div[1]/div[2]/div[2]/div[2]/div[2]/table/tbody/tr[1]/td[1]/a[2]'

from requests_html import HTMLSession
import webbrowser
import threading
from datetime import datetime
import beepy
from telegram import telegram_send

test = 'https://www.gamestop.ca/Accessories/Games/876251/biogenik-20-ps5-players-pack'
ps5d = "https://www.gamestop.ca/PS5/Games/877523"
ps5 = "https://www.gamestop.ca/PS5/Games/877522"
xsx = "https://www.gamestop.ca/Xbox%20Series%20X/Games/877779"

ps5b = 'https://www.gamestop.ca/PS5/Games/877752/playstation-5-with-extra-dualsense-controller'
ps5db = 'https://www.gamestop.ca/PS5/Games/877753/playstation-5-digital-edition-with-extra-dualsense-controller'
links = [ps5b, ps5db]

session = HTMLSession()

cookies = {
}

headers = {
    'authority': 'www.gamestop.ca',
    'content-length': '0',
    'pragma': 'no-cache',
    'cache-control': 'no-cache',
    'sec-ch-ua': '"Chromium";v="86", "\\"Not\\\\A;Brand";v="99", "Google Chrome";v="86"',
    'accept': '*/*',
    'x-newrelic-id': 'Vw4FUFNRGwEEVlVTAwEF',
    'x-requested-with': 'XMLHttpRequest',
    'sec-ch-ua-mobile': '?0',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
    'origin': 'https://www.gamestop.ca',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://www.gamestop.ca/Home/Index',
    'accept-language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
}

params = (
    ('pvid', '100641'),
)

a2clink = 'https://www.gamestop.ca/api/cart/AddProduct?pvid='

prod_selected = '#prodMain > div.mainInfo > div.addCartBar > div.prodRightBlock > div.buySection > div.singleVariantDetails.singleProductItem > div.productSelected'
def eb():
    print(datetime.now())
    threading.Timer(15.0, eb).start()

    for link in links:
        r = session.get(link)
        if r.status_code != 302 and r.url != 'https://www.gamestop.ca/Home/Index':
            oos_button = r.html.find("#btnAddToCart", first=True)
            no_show = "display:none;"
            if oos_button.attrs["style"] != no_show:
                beepy.beep()
                try:
                    sku = r.html.find('.productSelected', first=True).attrs['name'][-6:]
                    print(sku)
                except:
                    print("Get SKU Error!")
                telegram_send(link)
                webbrowser.open(link)
                # a2c(link)

# def a2c(link):
#     sku = link[-6:]
#     url = a2clink + sku
#     r = session.request('POST', url, cookies=cookies, data=headers)
#     if r.status_code != '400':
#
#     return link

eb()