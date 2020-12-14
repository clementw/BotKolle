checkout = 'https://www.tsc.ca/pages/expresscheckout'
ps5 = "https://www.tsc.ca/PlayStation-5-Launch-Bundle-with-Extra-Controller-and-SpiderMan-Miles-Morales-Ultimate-Edition/pages/productdetails?nav=R:643762"

from requests_html import HTMLSession
import webbrowser
import threading
from datetime import datetime
import asyncio
from pyppeteer import launch, connect
from telegram import telegram_send
import requests
ws_url = "ws://127.0.0.1:9222/devtools/browser/c4b26550-8edf-42fe-918d-8d448fb4ecf2"
links = [ps5]

easypay = '#expressCheckout > div > div.checkoutWrap > article > div.paymentOptionWrap > div.paymentoption__description > div > select'
easypay_container = '#expressCheckout > div > div.checkoutWrap > aside > div > div > div.ordersummary__container > div.OrderSummaryWrap > div > div.easypay__container'
place_order = '#expressCheckout > div > div.checkoutWrap > aside > div > div > div.ordersummary__container > div.placeorder__wrap.button--sticky > button'
async def tsc():
    browser = await connect(browserWSEndpoint=ws_url)
    page = await browser.newPage()
    await page._client.send('Emulation.clearDeviceMetricsOverride')

    while True:
        for link in links:
            await page.goto(link)
            print(datetime.now())

            stock = await page.querySelector('#lblSoldOut')
            if stock != None:
                stock_level = await page.evaluate('(element) => element.textContent', stock)
                if await stock_level != "SOLD OUT":
                    await page.waitForSelector('#btnAddToCart')
                    await page.click('#btnAddToCart')
                    await page.waitForSelector('#tagCartContainer > div.cart-section')
                    await page.goto(checkout)
                    await page.waitForSelector('#expressCheckout > div > div.checkoutWrap > aside > div > div > div.ordersummary__container')

                    # if ezpay is not selected
                    ezpay_container = await page.querySelector(easypay_container)
                    if ezpay_container == None:
                        await page.select(easypay, '12')
                        await page.waitForSelector(easypay_container)

                    promo = await page.querySelector('#promo')
                    # if promo code is not typed:
                    if promo != None:
                        await page.type('#promo', 'SHIP150')
                        await page.click('#expressCheckout > div > div.checkoutWrap > aside > div > div > div.ordersummary__container > div.promocode__container.formWrap > button')
                        await page.waitForSelector('#expressCheckout > div > div.checkoutWrap > aside > div > div > div.ordersummary__container > div.promocode__container.formWrap > div > button')

                    print("Success!")
                    # await page.click(place_order)
                else:
                    print("Not in stock :(")
                    await asyncio.sleep(5)
            await asyncio.sleep(5)



asyncio.get_event_loop().run_until_complete(tsc())
