# from fetch import Fetch
# from parsing import Parser
# import json

RLSLOG = "http://www.rlslog.net/category/ebooks/ebook/feed/"
MILLIYET = "http://www.milliyet.com.tr/rss/rssNew/SonDakikaRss.xml"
HURRIYET = "http://www.hurriyet.com.tr/rss/gundem"
XKCD = "https://xkcd.com/rss.xml"
CSSTRICKS = "https://css-tricks.com/feed/"
BBC = "http://feeds.bbci.co.uk/news/video_and_audio/news_front_page/rss.xml?edition=uk"
STEAM = "https://store.steampowered.com/feeds/newreleases.xml"
HT = "https://www.haberturk.com/rss/manset.xml"
# RADIKAL = "http://www.radikal.com.tr/d/rss/RssSD.xml"#! PARSE ERROR
CNNTURK = "https://www.cnnturk.com/feed/rss/all/news"
# GAMESPOT = "https://www.gamespot.com/feeds/mashup/" #! HORRIBLE
ROCKPAPERSHOTGUN = "http://feeds.feedburner.com/RockPaperShotgun"
KOTAKU = "https://kotaku.com/rss"
FITGIRL = "http://fitgirl-repacks.site/feed/"

# newFetcher = Fetch()

# newFetcher.addURL(RLSLOG)
# newFetcher.addURL(MILLIYET)
# newFetcher.addURL(HURRIYET)
# newFetcher.addURL(XKCD)
# newFetcher.addURL(CSSTRICKS)

# datas = newFetcher.fetchAll()

# rsslist = []

# for data in datas:
#     print()
#     rss = Parser.convertFromXML(data)
#     print(rss.title)
#     print(rss.desc)
#     print(rss.link)
#     print(rss.itemList)