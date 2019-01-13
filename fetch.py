from urllib.request import Request, urlopen

class Fetch(object):

    REQHEADER = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'
    }
    
    def fetchAll(self, urlList):
        dataList = []
        for elem in urlList:
            try:
                req = Request(elem['url'], headers=self.REQHEADER)
                data = urlopen(req)
                dataList.append({'url': elem['url'], 'cid': elem['cid'], 'xml': data.read()})
            except Exception as err:
                print(err)
        return dataList

    def fetchOne(self, url):
        try:
            req = Request(url, headers=self.REQHEADER)
            data = urlopen(req)
            return data.read()
        except Exception as err:
            print(err)
            return None
