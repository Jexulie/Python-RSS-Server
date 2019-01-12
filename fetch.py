from urllib.request import Request, urlopen

class Fetch(object):

    URL_LIST = []

    def __init__(self):
        pass

    def addURL(self, url):
        self.URL_LIST.append(url)
    
    def fetchAll(self):
        dataList = []
        for url in self.URL_LIST:
            try:
                data = urlopen(url)
                dataList.append(data.read())
            except:
                pass
        return dataList

    def fetchOne(self, url):
        try:
            data = urlopen(url)
            return data.read()
        except:
            return None
