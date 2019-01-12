import xmltodict

class RSS(object):
    def __init__(self, title, link, desc, itemList):
        self.title = title
        self.link = link
        self.desc = desc
        self.itemList = itemList

class Parser(object):
    @classmethod
    def convertFromXML(self, data):
        doc = xmltodict.parse(data)
        channel = doc['rss']['channel']
        items = doc['rss']['channel']['item']

        channelTitle = channel['title']
        channelLink = channel['link']
        channelDesc = channel['description']

        itemList = []

        for i in items:
            # Future remove html tags from nodes ...


            #! Standard Tags
            if isinstance(i['guid'],dict):
                item = {
                    'title': i['title'],
                    'pubDate': i['pubDate'],
                    'description': i['description'],
                    'guid': i['guid']['#text']
                }
            else:
                item = {
                    'title': i['title'],
                    'pubDate': i['pubDate'],
                    'description': i['description'],
                    'guid': i['guid']
                }
            #! Other Tags
            try:
                item['category'] = i['category']
            except:
                pass

            itemList.append(item)

        return RSS(
            channelTitle,
            channelLink,
            channelDesc,
            itemList
            )


