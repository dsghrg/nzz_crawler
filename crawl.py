# a little crawler in python
class Article():

    nzz_id = None
    title = None
    def __init__(self, nzz_id=None, title=None):
        self.nzz_id = nzz_id
        self.title = title 

    def __repr__(self):
        return "NZZ_ID: " + str(self.nzz_id)
    def __str__(self):
        return "Title: " + str(self.title)
    def __eq__(self, other):
        return self.nzz_id == other.nzz_id


import requests

r = requests.get("https://www.nzz.ch/neueste-artikel/")


#print(r.text)

from bs4 import BeautifulSoup
import json

doc = BeautifulSoup(r.text, "html.parser")

def get_article_html_from_teaser(teaser):
    a = teaser.find("a", class_="teaser__link", href=True)
    article_html = BeautifulSoup(requests.get(a['href']).text, "html.parser")
    return article_html

i = 0
for teaser in doc.find_all(attrs={"data-article": True}):
    # get nzzId from teaser
    nzz_id = json.loads(teaser["data-article"])["nzzId"]
    article_html = get_article_html_from_teaser(teaser)
    title = article_html.find("div", class_="title__name").text
    article = Article(nzz_id, title)
    print(article.__repr__())
    print(article)
    i += 1