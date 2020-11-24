from requests_html import HTMLSession
import webbrowser
import threading
from datetime import datetime
import asyncio
from pyppeteer import launch

link_xsx = "https://www.londondrugs.com/xbox-series-x/L1236749.html"
link_ps5 = "https://www.londondrugs.com/playstation-5-console/L1230429.html"

links = [link_ps5, link_xsx]

headers = {
    'authority': 'www.londondrugs.com',
    'pragma': 'no-cache',
    'cache-control': 'no-cache',
    'sec-ch-ua': '"Chromium";v="86", "\\"Not\\\\A;Brand";v="99", "Google Chrome";v="86"',
    'sec-ch-ua-mobile': '?0',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'cross-site',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'sec-fetch-dest': 'document',
    'accept-language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
    'cookie': ''}

async def get_stock(page, link):
    await page.goto(link)
    await page.waitFor(15000)
    stock = await page.querySelector('p.availability.primary-msg.alert-msg')

    stock_level = await page.evaluate('(element) => element.textContent', stock)
    return stock_level

async def captcha(page):
    t = page.url

    if t == 'https://www.londondrugs.com/on/demandware.store/Sites-LondonDrugs-Site/default/DDUser-Challenge':
        await page.waitFor(60000)

async def ldbot():
    browser = await launch(headless=False, args=['--window-size=1200,800'])
    page = (await browser.pages())[0]
    await page._client.send('Emulation.clearDeviceMetricsOverride');

    await page.setExtraHTTPHeaders(headers)
    await page.goto('https://www.londondrugs.com')

    await page.waitFor(15000)
    await captcha(page)

    while True:
        await asyncio.sleep(15)
        for link in links:
            if await get_stock(page, link) != "Out of Stock":
                webbrowser.open(link)
                await captcha(page)
                await asyncio.sleep(15)
            else:
                print("Not in stock :(")

asyncio.get_event_loop().run_until_complete(ldbot())