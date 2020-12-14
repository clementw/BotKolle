from requests_html import HTMLSession
import webbrowser
import threading
from datetime import datetime
import beepy
from telegram import telegram_send
import requests


ps5 = "https://www.thesource.ca/en-ca/gaming/playstation/ps5/playstation%c2%ae5-console/p/108090499"
ps5d = "https://www.thesource.ca/en-ca/gaming/playstation/ps5/playstation%C2%AE5-digital-edition-console/p/108090498"
xsx = "https://www.thesource.ca/en-ca/gaming/xbox/xbox-series-x/xbox-series-x-/p/108090646"
links = [ps5, ps5d, xsx]

scs = [404, 504, 500]
def ts():
    print(datetime.now())
    threading.Timer(60.0, ts).start()

    for link in links:
        r = requests.get(link)

        sc = r.status_code
        print(sc)

        if sc not in scs:
            telegram_send(link)
            webbrowser.open(link)


ts()
