# a little crawler in python

import requests

r = requests.get("https://www.nzz.ch/neueste-artikel/")


#print(r.text)

from bs4 import BeautifulSoup

doc = BeautifulSoup(r.text, "html.parser")


i = 0
for p in doc.find_all(attrs={"data-article": True}):
    print(p)
    i += 1
    print(i)
