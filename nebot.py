from requests_html import HTMLSession
import webbrowser
import threading
from datetime import datetime

session = HTMLSession()

link_3080 = "https://www.newegg.ca/p/pl?d=rtx+3000&N=100007708%208000&isdeptsrh=1&PageSize=96"


def nebot():
    print(datetime.now())
    threading.Timer(15.0, nebot).start()

    r = session.get(link_3080)

    item_containers = r.html.find(".item-container")

    for item in item_containers:
        btn_text = item.find(".btn-mini", first=True).full_text
        if btn_text != "Sold Out" and btn_text != "Auto Notify ":
            item_url = item.find('a')[0].attrs['href']
            r1 = session.get(item_url)
            if r1.html.find(".btn-wide", first=True).full_text != "Sold Out":
                print('Yay!')
                webbrowser.open(item_url)


nebot()