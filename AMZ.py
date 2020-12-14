from lxml import html
import requests
from time import sleep
import time
import schedule
from telegram import *
import webbrowser
from datetime import datetime
from requests_html import HTMLSession
import threading
from bs4 import BeautifulSoup
import aioify
import urllib
import re

ws_url = "ws://127.0.0.1:9222/devtools/browser/c4b26550-8edf-42fe-918d-8d448fb4ecf2"
from pyppeteer import launch, connect
import asyncio
import beepy

already_bought = []
headers = {
    'authority': 'www.amazon.ca',
    'pragma': 'no-cache',
    'cache-control': 'no-cache',
    'rtt': '50',
    'downlink': '10',
    'ect': '4g',
    'sec-ch-ua': '"Chromium";v="86", "\\"Not\\\\A;Brand";v="99", "Google Chrome";v="86"',
    'sec-ch-ua-mobile': '?0',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'service-worker-navigation-preload': 'true',
    'sec-fetch-site': 'none',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'sec-fetch-dest': 'document',
    'accept-language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
}

session = HTMLSession()


def check_stock_page(asin):
    base = "https://www.amazon.ca/dp/"
    url = base + asin
    page = requests.get(url, headers=headers)

    sleep(3)

    # parsing the html content
    doc = html.fromstring(page.content)

    # checking availaility
    xpath = '//div[@id ="availability"]//text()'
    seller_xpath = '//*[@id="merchant-info"]//text()'
    availability = doc.xpath(xpath)
    seller = doc.xpath(seller_xpath)
    AVAILABILITY = ''.join(availability).strip() if availability else None
    seller = ''.join(seller).strip() if seller else None
    return AVAILABILITY, seller


def check_listings_page(asin):
    listings_url = 'https://www.amazon.ca/gp/offer-listing/' + asin + '/'
    r = session.request("GET", listings_url, headers=headers)
    raw_html = r.html.html.replace('\n', '')
    print(raw_html)
    return 'alt="Amazon.ca"' in raw_html or 'alt="Warehouse Deals"' in raw_html

test_instantpot = 'B07RCNHTLS'
ps5 = "B08GSC5D9G"
ps5d = "B08GS1N24H"
xsx = "B08H75RTZ8"

amd = ["B0815XFSGK", "B08164VTWH", "B08166SLDF"]
rtx3080 = ['B08HH5WF97', 'B08HR3Y5GQ', 'B08HR7SV3M', 'B08HJNKT3P', 'B08J6F174Z']
rtx3070 = ['B08LF1CWT2', 'B08KWN2LZG', 'B08LW46GH2']
rx6800 = ['B08N6ZLX9B', 'B08MNZM5TK']
checkout = 'https://www.amazon.ca/gp/buy/spc/handlers/display.html?hasWorkingJavascript=1'

# clicking problems on a2c button
firsta2c = '#a-autoid-0'

url_90 = 'https://www.amazon.ca/stores/GeForce/RTX3090_GEFORCERTX30SERIES/page/CFF83A4D-9DEC-4003-AC7E-96DF4170CED0'
url_80 = 'https://www.amazon.ca/stores/GeForce/RTX3080_GEFORCERTX30SERIES/page/6B204EA4-AAAC-4776-82B1-D7C3BD9DDC82'
session = HTMLSession()
sku_regex = '(?<=dp/).*'
# new gpu tracking
def sku_find(u):
    skus = []

    r = session.get(u)

    item_urls = r.html.find("a")

    for url in item_urls:
        if "href" in url.attrs:
            h = url.attrs['href']
            if '/dp/' in h:
                sku = re.search(sku_regex, h).group()[:10]
                if sku != 'B07MJM4F44':
                    skus.append(sku)

    return skus

async def amz():
    browser = await connect(browserWSEndpoint=ws_url)
    page = await browser.newPage()
    await page._client.send('Emulation.clearDeviceMetricsOverride')

    asins = sku_find(url_90) + sku_find(url_80) + rx6800
    while True:
        for asin in asins:
            print(datetime.now())
            url = 'https://www.amazon.ca/gp/offer-listing/' + asin + '/ref=olp_f_primeEligible?f_primeEligible=true'
            await page.goto(url)
            content = await page.content()
            warehouse = await page.querySelectorAll('[alt="Warehouse Deals"]')
            new = await page.querySelectorAll('[alt="Amazon.ca"]')
            if len(warehouse) != 0 or len(new) != 0:
                print("In Stock!")
                beepy.beep()
                # telegram_send('https://www.amazon.ca/gp/offer-listing/' + asin)
                already_bought.append(asin)

                # click first a2c
                await page.evaluate("document.querySelector('#a-autoid-0 > span > input').click()")

                await asyncio.sleep(30)

                # await page.waitForNavigation()
                #
                # # proceed to checkout
                #
                # # await page.click('#hlb-ptc-btn-native')
                # #
                # # telegram_send(url)
                # #
                # # await page.waitForNavigation()
                #
                # await asyncio.sleep(5)
                # # click on fs
                # if page.url == checkout:
                #     await page.click('#spc-orders > div.a-box > div > div.shipment '
                #                      '> div > div > div:nth-child(2) > div:nth-child(2) '
                #                      '> div.a-row.shipping-speeds > fieldset > div:nth-child(3) > input')
                #
                #     await page.waitForSelector('#subtotals-marketplace-table > tbody > tr:nth-child(3) > td:nth-child(1) > span')
                #
                #     # click place order
                #     await page.click('#placeYourOrder > span > input')
            else:
                print("Not in stock :(")
            await asyncio.sleep(10)
    # scheduling same code to run multiple


asyncio.get_event_loop().run_until_complete(amz())
