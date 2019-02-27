# a little crawler in python
class Article():

    nzz_id = None
    title = None
    author = None
    department = None
    datetime = None
    def __init__(self, nzz_id=None, title=None, author=None):
        self.nzz_id = nzz_id
        self.title = title
        self.author = author

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
import re

doc = BeautifulSoup(r.text, "html.parser")

def get_article_html_from_teaser(teaser):
    a = teaser.find("a", class_="teaser__link", href=True)
    article_html = BeautifulSoup(requests.get(a["href"]).text, "html.parser")
    return article_html

i = 0
for teaser in doc.find_all(attrs={"data-article": True}):
    # get nzzId from teaser
    nzz_id = json.loads(teaser["data-article"])["nzzId"]
    department = json.loads(teaser["data-article"])["department"]

    article_html = get_article_html_from_teaser(teaser)

    title = article_html.find("div", class_="title__name").text
    author_metainfo = article_html.find("span", class_="metainfo__author")
    author = None
    pattern = "\({1}[A-Za-z/]+\){1}"
    repl_pattern = "\(\)]"
    if author_metainfo:
        author = author_metainfo.text
    else:
        agency = article_html.find("em", class_="source__wrapper")
        if agency:
            author = re.sub(repl_pattern, "", agency.text)
        else:
            author = re.search(pattern, article_html.find("em").text).group(0)
            # print(article_html.find("em").text)
            # print(author)
            author = re.sub(repl_pattern, "", author)

    datetime = article_html.find("span", class_="metainfo__date")['datetime']

    article = Article(nzz_id, title, author)

    article.department = department
    article.datetime = datetime
    print(article.__repr__())
    print(article.department)
    print(article.title)
    print(article.author)
    print()
    i += 1