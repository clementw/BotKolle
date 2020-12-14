from requests_html import HTMLSession
import webbrowser
import threading
from datetime import datetime
import beepy
from telegram import telegram_send

session = HTMLSession()

rtx3080 = "https://www.newegg.ca/p/pl?d=3080&N=8000%20100007708&isdeptsrh=1"
ryzen5k = "https://www.newegg.ca/p/pl?d=ryzen+5000&N=8000"
rx6800xt = "https://www.newegg.ca/p/pl?d=rx+6800&N=4841"
rtx3060ti = 'https://www.newegg.ca/p/pl?d=rtx+3060+ti&N=8000'
rtx3090 = 'https://www.newegg.ca/p/pl?d=rtx+3090&N=8000%20100007708&isdeptsrh=1'
links = [rtx3090, rtx3080, rtx3060ti, ryzen5k, rx6800xt]
cart = "https://secure.newegg.ca/shop/cart"

url_list = []

def nebot():
    print(datetime.now())
    threading.Timer(15.0, nebot).start()

    for link in links:
        r = session.get(link)
        item_containers = r.html.find(".item-container")

        for item in item_containers:
            btn_text = item.find(".btn-mini", first=True).full_text
            if btn_text != "Sold Out" and btn_text != "Auto Notify ":
                # beepy.beep(sound="coin")
                item_url = item.find('a')[0].attrs['href']
                if item_url not in url_list and "3070" not in item_url:
                    url_list.append(item_url)
                    telegram_send(item_url)
                    webbrowser.open(item_url)
                    telegram_send(cart)
                    print(item_url)


nebot()