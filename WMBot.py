import requests
import webbrowser
import json
import requests
import codecs
import threading
from datetime import datetime
import beepy
from telegram import telegram_send
from pyppeteer import launch, connect
import asyncio
import json

ws_url = "ws://127.0.0.1:9222/devtools/browser/c4b26550-8edf-42fe-918d-8d448fb4ecf2"

headers = {
    'authority': 'www.walmart.ca',
    'pragma': 'no-cache',
    'cache-control': 'no-cache',
    'sec-ch-ua': '"Chromium";v="86", "\\"Not\\\\A;Brand";v="99", "Google Chrome";v="86"',
    'accept': 'application/json',
    'content-type': 'application/json',
    'sec-ch-ua-mobile': '?0',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
    'wm_qos.correlation_id': 'cdd98ee9-026-1762aa16bfeb34,cdd98ee9-026-1762aa16bfe207,cdd98ee9-026-1762aa16bfe207',
    'origin': 'https://www.walmart.ca',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://www.walmart.ca/en/ip/apple-pencil/6000196133985?rrid=richrelevance',
    'accept-language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
}

ps5 = '{"fsa":"M1M","products":[{"productId":"6000201790922","skuIds":["6000201790923"]},{"productId":"6000202198823","skuIds":["6000202198824"]},{"productId":"6000202198562","skuIds":["6000202198563"]},{"productId":"6000202283428","skuIds":["6000202283429"]},{"productId":"6000202282463","skuIds":["6000202282464"]}],"lang":"en","pricingStoreId":"3053","fulfillmentStoreId":"3195","experience":"whiteGM"}'

checkout = 'https://www.walmart.ca/checkout'
base_url = "https://www.walmart.ca/en/ip/"


def get_items():
    try:
        r = requests.post('https://www.walmart.ca/api/bsp/v2/price-offer', headers=headers, cookies=cookies, data=ps5)
        print(r.url)
        j = r.json()
        offers = j['offers']
        return offers
    except:
        print('Error!')
        return None

select_payment_xpath = '//*[@id="section-payment-summary-edit-link"]'

a2c_selector = 'body > div.js-content.privacy-open > div > div:nth-child(4) > div > div > div.css-0.eewy8oa0 > div.css-12rl50h.eewy8oa2 > div.css-18f77yw.eewy8oa4 > div > div.cta.css-t5h6pw.e61xtbo0 > div:nth-child(2) > div > button.css-1i45fk4.edzik9p0'
gc_apply_more_selector = '#step3 > div.css-10nwg10.e1vdg7k72 > div.css-k008qs.e11c4i080 > div.css-ieri5n.e11c4i082 > div > div > button'

async def buy(page, sku):
    print("Success!")
    print(sku)
    url = base_url + sku
    telegram_send(url)
    await page.goto(url)

    if "blocked" in page.url:
        print('captcha')
        await page.waitForNavigation()
    print('prod page')


    navigationPromise = asyncio.ensure_future(page.waitForSelector(a2c_selector))
    await page.click(a2c_selector)
    await navigationPromise  # wait until navigation finishes

    await page.goto(checkout)
    await page.waitForNavigation()

    # gc logic to be fixed
    # if gcs != []:
    #     num = gcs[0][0]
    #     pin = gcs[0][1]
    #     # check if edit payment exists
    #     select = await page.xpath(select_payment_xpath)
    #     if select != []:
    #         print("click on edit payment")
    #         await page.click(select[0])
    #
    #     print("type gc")
    #     # type gc number and pin
    #     await page.type('#cardNumber', num)
    #     await page.type('#cardPin', pin)
    #     # pay with gc
    #     await page.click('#step3 > div.css-10nwg10.e1vdg7k72 > div.css-k008qs.e11c4i080 > div.css-1rr4qq7.e11c4i081 > div:nth-child(3) > button > div')
    #
    #     # apply gc
    #     await page.click('#payments_add_gift_card > div.css-1bnvp8n.e1f06pdh3 > button')
    #
    #     # wait for gc to be applied
    #     await page.waitForSelector(gc_apply_more_selector)
    #     print("gc applied")
    #     gcs.pop(0)
    #     print(gcs)

    # click on place order
    await page.click('body > div.js-content > div > div > div.css-1yml32t.e9pe5pm0 > div.css-1pv5w2k.edp9pj60 > div > div > div > button')

async def wmbot():
    browser = await connect(browserWSEndpoint=ws_url)

    while True:
        print(datetime.now())
        offers = None
        while offers == None:
            print(datetime.now())
            offers = get_items()
            await asyncio.sleep(120)
        for sku in offers:
            if offers[sku]['sellerId'] == '0':
                print(sku)
                availability = offers[sku]['gmAvailability']
                print(availability)
                if availability != "OutOfStock":
                    page = await browser.newPage()
                    await page._client.send('Emulation.clearDeviceMetricsOverride')
                    try:
                        await buy(page, sku)
                    except:
                        print("Blocked!")

        await asyncio.sleep(5)

xbox_controller_sku = '6000197512235'

asyncio.get_event_loop().run_until_complete(wmbot())
