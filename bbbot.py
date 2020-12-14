import asyncio
import json
import webbrowser
from datetime import datetime

import requests
from pyppeteer import connect
from requests_html import HTMLSession

from telegram import telegram_send

prod_link = "https://www.bestbuy.ca/en-ca/product/"
ws_url = "ws://127.0.0.1:9222/devtools/browser/c4b26550-8edf-42fe-918d-8d448fb4ecf2" # 3060 70 80
url_3k = "https://www.bestbuy.ca/en-ca/collection/rtx-30-series-graphic-cards/316108"

sku_ps5 = [14962185, 14962184, 'B0014217', 'B0014216']

sku_xsx = [14964951]

test = [13446573]
already_bought = []


def strnify(a):
    return [str(s) for s in a]


headers = {
    'authority': 'www.bestbuy.ca',
    'pragma': 'no-cache',
    'cache-control': 'no-cache',
    'sec-ch-ua': '"Chromium";v="86", "\\"Not\\\\A;Brand";v="99", "Google Chrome";v="86"',
    'sec-ch-ua-mobile': '?0',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
    'accept': '*/*',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'accept-language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
}

session = HTMLSession()

wants = ['3060', '3080', '3090']

# new gpu tracking
def sku_3k_gen():
    skus = []

    r = session.get(url_3k)

    item_urls = r.html.find(".link_3hcyN")

    for url in item_urls:
        prod_title = url.full_text
        if '3060' in prod_title or '3080' in prod_title or "3090" in prod_title:
            sku = url.attrs["href"][-8:]
            skus.append(sku)

    return skus


def check_stock(sku):
    params = (
        ('accept', 'application/vnd.bestbuy.standardproduct.v1+json'),
        ('accept-language', 'en-CA'),
        ('locations',
         '203|977|617|62|931|927|57|938|965|237|932|943|956|200|202|926|795|916|937|544|910|954|207|233|930|622|245|223|925|985|990|949|959|942'),
        ('postalCode', 'M6G'),
        ('skus', sku),
    )

    r = requests.get('https://www.bestbuy.ca/ecomm-api/availability/products', headers=headers, params=params)
    j = json.loads(r.text[1:])
    j = j["availabilities"]

    j = j[0]['shipping']
    return j


pp_checkout = 'https://www.bestbuy.ca/checkout/?qit=1#/en-ca/shipping/ON/M6G?expressPaypalCheckout=true'
checkout = 'https://www.bestbuy.ca/checkout/'
a2c = '#test > button'
order = '#posElement > section > section.cost-sum-section > button'
cvvfield = '#cvv'
async def bbbot():
    browser = await connect(browserWSEndpoint=ws_url)

    while True:
        print(datetime.now())
        skus = strnify(sku_ps5) + strnify(sku_3k_gen())
        print(skus)
        for sku in skus:
            item = check_stock(sku)
            try:
                status = item['purchasable']
                await asyncio.sleep(2)
                print(status)
                if status is True:
                    if sku not in already_bought:
                        # beepy.beep(sound="coin")
                        try:
                            q = item['quantityRemaining']
                            print(sku)
                            print(q)
                            telegram_send(str(q))
                        except:
                            print("Error in Quantity")
                        url = prod_link + str(sku)
                        print(item)
                        print(url)
                        #webbrowser.open(url)
                        telegram_send(url)

                        page = await browser.newPage()
                        await page._client.send('Emulation.clearDeviceMetricsOverride')
                        # await page.goto(url)
                        # webbrowser.open(url)
                        # await page.click(a2c)

                        # await page.waitForNavigation()
                        # await page.evaluate("document.querySelector('.addToCartButton').click();")
                        # await page.waitForResponse('https://www.bestbuy.ca/api/basket/v2/baskets')
                        await page.goto(checkout)
                        # await page.goto(pp_checkout)
                        # telegram_send("In cart, CO NOW")
                        # telegram_send(checkout)
                        await page.waitForSelector(cvvfield)
                        await asyncio.sleep(2)
                        await page.click(order)
                        # telegram_send("Ordered!")
                        # webbrowser.open(pp_checkout)
                        telegram_send(checkout)
                        await asyncio.sleep(15)
                        already_bought.append(sku)
            except:
                print("Error!")


asyncio.get_event_loop().run_until_complete(bbbot())
