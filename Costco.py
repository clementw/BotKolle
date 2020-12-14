from lxml import html
import requests
from time import sleep
import time
import schedule
from telegram import telegram_send
import webbrowser
from datetime import datetime
from requests_html import HTMLSession
import threading
from bs4 import BeautifulSoup
ws_url = "ws://127.0.0.1:9222/devtools/browser/c4b26550-8edf-42fe-918d-8d448fb4ecf2"
from pyppeteer import launch, connect
import asyncio
import beepy

ps5 = 'https://www.costco.ca/playstation-5-console-bundle.product.100696941.html'
test = 'https://www.costco.ca/.product.1343367.html'
choco = 'https://www.costco.ca/.product.293701.html'
ccfield = '#creditcard-block-form'
urls = [ps5]

cvv = '#securityCode'
checkout = 'https://www.costco.ca/SinglePageCheckoutView'
cart = 'https://www.costco.ca/CheckoutCartView'
a2c = '#add-to-cart-btn'
co = '#shopCartCheckoutSubmitButton'
co_js = "COSTCO.OrderSummaryCart.submitCart('https://www.costco.ca/ManageShoppingCartCmd?actionType=expressCheckout');"
apply_promo_js = ''
promo_field = '#enter-promo-code-input'
iframe = '#cc_cvv_div > iframe'
already_bought = []
promo = 'NXP5MM8'
place_order = '#checkout-button-wrapper > input'
async def costco():
    browser = await connect(browserWSEndpoint=ws_url)
    page = await browser.newPage()
    await page._client.send('Emulation.clearDeviceMetricsOverride')

    while True:
        for url in urls:
            print(datetime.now())
            await page.goto(url)
            a2c_txt = await page.evaluate('document.querySelector("#add-to-cart-btn").getAttribute("value")')
            if a2c_txt != "Out of Stock" and url not in already_bought:
                # beepy.beep()
                print("In Stock!")
                telegram_send(url)
                already_bought.append(url)

                await page.evaluate('document.querySelector("#add-to-cart-btn").click()')
                await page.waitForResponse('https://www.costco.ca/AjaxManageShoppingCartCmd')

                await page.goto(cart)

                await page.evaluate(co_js)
                await page.waitForNavigation()

                # await page.waitForSelector(iframe)
                # frame_element = await page.querySelector(iframe)
                # frame = await frame_element.contentFrame()
                # print("Inside CVV IFrame")
                # await page.waitForSelector(cvv)
                # await page.click(cvv)
                # await page.type(cvv, '844')
                # print("CVV Typed")

                await page.focus(promo_field)
                await page.type(promo_field, promo)

                telegram_send("Type CVV!")

                await asyncio.sleep(30)

                await page.waitForSelector(place_order)
                await page.click(place_order)
            else:
                print("Not in stock :(")
                await asyncio.sleep(5)
        await asyncio.sleep(5)

asyncio.get_event_loop().run_until_complete(costco())
