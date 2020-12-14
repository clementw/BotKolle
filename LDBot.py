from requests_html import HTMLSession
import webbrowser
import threading
from datetime import datetime
import asyncio
from pyppeteer import launch, connect
from telegram import telegram_send
import beepy
xsx = "https://www.londondrugs.com/xbox-series-x/L1236749.html"
ps5 = "https://www.londondrugs.com/playstation-5-console/L1230429.html"
test = 'https://www.londondrugs.com/profusion-25-days-to-sleigh-advent-calendar/L1201958.html?cgid=christmas-advent'
links = [xsx, ps5]
ordered = []
ws_url = "ws://127.0.0.1:9222/devtools/browser/c4b26550-8edf-42fe-918d-8d448fb4ecf2"
async def get_stock(page, link):
    await page.goto(link)
    await page.waitFor(10000)
    stock = await page.querySelector('p.availability.primary-msg.alert-msg')

    if stock != None:
        stock_level = await page.evaluate('(element) => element.textContent', stock)
        return stock_level
    else:
        return None

async def captcha(page):
    t = page.url

    if t == 'https://www.londondrugs.com/on/demandware.store/Sites-LondonDrugs-Site/default/DDUser-Challenge':
        await page.waitFor(60000)


a2c_btn = '//*[@id="add-to-cart"]'
cvv_xpath = '/html/body/main/div/div/form/div[4]/div[1]/label/div[2]/ul/li[1]/div[4]/div/div/input'
tick_xpath = '/html/body/main/div/div/div/section/form/div[3]/div[1]/label'


async def ldbot():
    browser = await connect(browserWSEndpoint=ws_url)
    page = await browser.newPage()
    await page._client.send('Emulation.clearDeviceMetricsOverride')

    while True:
        for link in links:
            print(datetime.now())

            stock = await get_stock(page, link)
            print(stock)
            if stock != "Out of Stock" and stock != "Store Pickup Only" and stock != None:
                beepy.beep()

                await page.waitForSelector('#add-to-cart')
                await page.click('#add-to-cart')

                await asyncio.sleep(3)

                await page.goto('https://www.londondrugs.com/cart/')

                # checkout btn
                await page.click('#cart-items-form > fieldset > div > div.shopping-cart__order-processing > div > div.cart-total__payment-section > fieldset > button')

                await asyncio.sleep(3)

                # review billing
                await page.click('#dwfrm_singleshipping_shippingAddress > button')

                await page.waitForXPath(cvv_xpath)

                # type cvv
                cvv_field = await page.xpath(cvv_xpath)
                await cvv_field[0].type('5155')

                await asyncio.sleep(3)

                # review order
                await page.click('#dwfrm_billing > button')

                await page.waitForXPath(tick_xpath)
                tickbox = await page.xpath(tick_xpath)
                await tickbox[0].click()

                # place order
                await page.click('body > main > div > div > div > section > form > '
                                 'div.ch-place-order-confirm > div.ch-place-order__action-button-bottom > button')

                await asyncio.sleep(5)

                telegram_send("LD Checkout")
            else:
                print("Not in stock :(")
                await asyncio.sleep(5)
            await asyncio.sleep(15)


asyncio.get_event_loop().run_until_complete(ldbot())
