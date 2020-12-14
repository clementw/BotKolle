from requests_html import HTMLSession
import webbrowser
import threading
from datetime import datetime
import beepy
from telegram import telegram_send
import requests

ps5 = "https://www.staples.ca/products/2993213-en-playstation-5-console"
xsx = "https://www.staples.ca/products/2993232-en-xbox-series-x-console"
links = [ps5, xsx]
cart = 'https://www.staples.ca/cart'

def st():
    print(datetime.now())
    threading.Timer(60.0, st).start()

    for link in links:
        r = requests.get(link)

        sc = r.status_code
        print(sc)
        if sc != 404 and sc != 500:
            telegram_send(link)
            webbrowser.open(link)
            webbrowser.open(cart)

st()
