import xmltodict
import random

# todo can improve this
def idGenerator(length):
    id = ""
    for _ in range(length):
        id += str(random.randint(0, 9))
    return id

class RSS(object):
    def __init__(self, title, link, desc, itemList):
        self.cid = idGenerator(10)
        self.title = title
        self.link = link
        self.desc = desc
        self.itemList = itemList

class Parser(object):
    @classmethod
    def convertFromXML(self, data):
        try:
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
                        'id': idGenerator(20),
                        'title': i['title'],
                        'pubDate': i['pubDate'],
                        'description': i['description'],
                        'guid': i['guid']['#text']
                    }
                else:
                    item = {
                        'id': idGenerator(20),
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
        except:
            return False


