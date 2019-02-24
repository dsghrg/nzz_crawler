# a little crawler in python

import requests

r = requests.get("https://www.nzz.ch/neueste-artikel/")


#print(r.text)

from bs4 import BeautifulSoup

doc = BeautifulSoup(r.text, "html.parser")


i = 0
for p in doc.find_all(attrs={"data-article": True}):
    a = p.find("a", class_="teaser__link", href=True)
    article_html = BeautifulSoup(requests.get(a['href']).text, "html.parser")
    print(article_html.find("div", class_="title__name").text)
    i += 1
    