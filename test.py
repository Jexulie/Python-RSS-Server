from fetch import Fetch
from parsing import Parser
import json

RLSLOG = "http://www.rlslog.net/category/ebooks/ebook/feed/"
MILLIYET = "http://www.milliyet.com.tr/rss/rssNew/SonDakikaRss.xml"
HURRIYET = "http://www.hurriyet.com.tr/rss/gundem"
XKCD = "https://xkcd.com/rss.xml"
CSSTRICKS = "https://css-tricks.com/feed/"


newFetcher = Fetch()

# newFetcher.addURL(RLSLOG)
# newFetcher.addURL(MILLIYET)
# newFetcher.addURL(HURRIYET)
newFetcher.addURL(XKCD)
# newFetcher.addURL(CSSTRICKS)

datas = newFetcher.fetchAll()

rsslist = []

for data in datas:
    print()
    rss = Parser.convertFromXML(data)
    print(rss.title)
    print(rss.desc)
    print(rss.link)
    print(rss.itemList)