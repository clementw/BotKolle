link = 'https://www.amd.com/en/direct-buy/ca'

import threading
import webbrowser
from datetime import datetime

from requests_html import HTMLSession

from telegram import telegram_send

session = HTMLSession()
oos = "OUT OF STOCK"
na = "not available"

def amd():
    print(datetime.now())
    threading.Timer(30.0, amd).start()

    r = session.get(link)

    if oos not in str(r.content) and na not in str(r.content):
        webbrowser.open(link)
        telegram_send(link)


amd()
