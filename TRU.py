stock_base = 'https://www.toysrus.ca/en/stores-getatsvalue?pid={}&quantitySelected=1'
store_base = 'https://www.toysrus.ca/en/{}.html'
checkout = 'https://www.toysrus.ca/en/checkout-login'
pymts = 'https://www.toysrus.ca/en/checkout?stage=payment#payment'

ws_url = "ws://127.0.0.1:9222/devtools/browser/c4b26550-8edf-42fe-918d-8d448fb4ecf2"
a2c = '#maincontent > div > div.b-product_primary.js-pdp-container > div.b-product_primary-section.m-section2 > div > div.b-product_details-actions.js-product-cta-btns > div.b-product_details-shipping-container > div.b-product_details-cta.js-add-to-cart-main > button'
a2c_response = 'https://www.toysrus.ca/on/demandware.store/Sites-toys-ca-Site/en_CA/Cart-AddProduct'
amount = '#maincontent > div > div.b-product_primary.js-pdp-container > div.b-product_primary-section.m-section2 > div > div.b-product_details-quantity > div > div > input'
place_order = '#js-stage-scroll-anchor-3 > div.b-checkout_section-btns.js-next-step-button > button.b-button.m-green.place-order'
cvvfield = '#saved-payment-security-code'
review = '#js-stage-scroll-anchor-3 > div.b-checkout_section-btns.js-next-step-button > button.b-button.btn-block.submit-payment'
import asyncio

import requests
from pyppeteer import connect
from datetime import datetime
from telegram import telegram_send
import beepy

skus = ['C443A89B']

async def tru():
    browser = await connect(browserWSEndpoint=ws_url)

    while True:
        print(datetime.now())
        for sku in skus:
            stock = stock_base.format(sku)
            store = store_base.format(sku)
            r = requests.get(stock)

            j = r.json()
            stock = j['ats']['homeDelivery']

            if stock != 0:
                telegram_send(store)
                telegram_send(str(stock))

                page = await browser.newPage()
                await page._client.send('Emulation.clearDeviceMetricsOverride')


                await page.goto(store)
                # await page.type(amount, str(stock))

                await page.click(a2c)

                await asyncio.sleep(2)

                await page.goto(pymts)

                await page.waitForSelector(cvvfield)
                await page.type(cvvfield, '844')

                await page.click(review)
                await page.waitForSelector(place_order)
                await page.click(place_order)
            else:
                print("Not in stock :(")
        await asyncio.sleep(15)


asyncio.get_event_loop().run_until_complete(tru())
