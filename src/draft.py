import re, sqlite3, requests
from bs4 import BeautifulSoup
from lxml import etree

def split_HomesData(url: str) -> list:
    # get the response
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
    headers = {'User-Agent': user_agent}
    with requests.Session() as s:
        r = s.get(url, headers=headers)
        if r.status_code == 200:
            dom = etree.HTML(str(BeautifulSoup(r.content, features='lxml')))

    # parse the content
    tag_content = re.sub(r'\\', '', dom.xpath("//script")[-2].text)
    text = re.findall(r"\"homes\":.*,\"dataSources\"", tag_content)
    x1 = re.sub(r",\"dataSources\"",'', text[0])[8:]
    x2 = re.sub(r"false", "False", x1)
    x3 = re.sub(r"true", "True", x2)

    # split
    eles = re.split(r',\"isViewedListing\":False},', x3[1:-1])
    eles = [ele.strip() for ele in eles if ele.strip() != '']

    return eles