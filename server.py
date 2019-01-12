from fetch import Fetch
from parsing import Parser
from flask import Flask, Response, json, request
import json
import re

# Todo User System.
# Todo 2 Database Implentation.
# Todo 3 on Wrong RSS remove added URL and send back response.
# Todo 4 If URL already exists reject

newFetcher = Fetch()

app = Flask(__name__)

def checkDubs(url):
    if url in newFetcher.URL_LIST:
        return True
    return False

def checkURL(url):
    match = re.match(r'http[s]?://.*', url)
    if match:
        return True
    else:
        return False

@app.route("/", methods=['GET'])
def index():
    r = {
        'success': True,
        'msg': "Server Index Point ..."
    }
    resp = Response(json.dumps(r))
    resp.headers['Content-Type'] = 'application/json'
    resp.headers['Access-Control-Allow-Origin'] =  '*' #! CORS
    return resp

@app.route("/add", methods=['POST', 'OPTIONS'])
def addURL():
    # Todo Do this to every route - pitfall rescue
    content = request.json
    try:
        url = content['URL']
        # future Test URL HERE THEN RESPOND
        if checkDubs(url):
            r = {
                'success': False,
                'msg': "Duplicate URL ..."
            }
        else:
            if checkURL(url):
                r = {
                    'success': True,
                    'msg': "URL Added ..."
                }
                try:
                    newFetcher.addURL(url)
                except:
                    r = {
                        'success': False,
                        'msg': "RSS Fetch Error ..."
                    }
            else:
                r = {
                    'success': False,
                    'msg': "Wrong URL Type ..."
                }

        resp = Response(json.dumps(r))
        resp.headers['Content-Type'] = 'application/json'
        resp.headers['Access-Control-Allow-Origin'] =  '*' #! CORS
        resp.headers['Access-Control-Allow-Headers'] =  'Origin, X-Requested-With, Content-Type, Accept' 

        return resp
    except:
        r = {
            'success': False,
            'request': content,
            'msg': "Wrong Parameters"            
        }
        
        resp = Response(json.dumps(r))
        resp.headers['Content-Type'] = 'application/json'
        resp.headers['Access-Control-Allow-Origin'] =  '*' #! CORS
        resp.headers['Access-Control-Allow-Headers'] =  'Origin, X-Requested-With, Content-Type, Accept' 

        return resp

@app.route("/get", methods=['GET'])
def getAllRSS():
    datas = newFetcher.fetchAll()
    rssList = []    

    for data in datas:
        rss = Parser.convertFromXML(data)
        if rss != False:
            d = {
                'cid': rss.cid,
                'title': rss.title,
                'link': rss.link,
                'description': rss.desc,
                'itemList': rss.itemList
            }
            rssList.append(d)

    r = {
        'success': True,
        'data': rssList
    }

    resp = Response(json.dumps(r))
    resp.headers['Content-Type'] = 'application/json'
    resp.headers['Access-Control-Allow-Origin'] =  '*' #! CORS
    resp.headers['Access-Control-Allow-Headers'] =  'Origin, X-Requested-With, Content-Type, Accept' 
    
    return resp

@app.route("/getone", methods=['POST', 'OPTIONS'])
def getOneRSS():
    content = request.json
    try:
        data = newFetcher.fetchOne(content['URL'])
        if data is not None:
            rss = Parser.convertFromXML(data)
        else:
            r = {
                'success': False,
                'msg': "RSS Fetch Error ..."
            }

            resp = Response(json.dumps(r))
            resp.headers['Content-Type'] = 'application/json'
            resp.headers['Access-Control-Allow-Origin'] =  '*' #! CORS
            resp.headers['Access-Control-Allow-Headers'] =  'Origin, X-Requested-With, Content-Type, Accept' 

            return resp

        if rss == False:
            r = {
                'success': False,
                'msg': "Parsing Error ..."
            }

            resp = Response(json.dumps(r))
            resp.headers['Content-Type'] = 'application/json'
            resp.headers['Access-Control-Allow-Origin'] =  '*' #! CORS
            resp.headers['Access-Control-Allow-Headers'] =  'Origin, X-Requested-With, Content-Type, Accept' 

            return resp

        d = {
            'cid': rss.cid,
            'title': rss.title,
            'link': rss.link,
            'description': rss.desc,
            'itemList': rss.itemList
        }

        r = {
            'success': True,
            'data': d
        }

        resp = Response(json.dumps(r))
        resp.headers['Content-Type'] = 'application/json'
        resp.headers['Access-Control-Allow-Origin'] =  '*' #! CORS
        resp.headers['Access-Control-Allow-Headers'] =  'Origin, X-Requested-With, Content-Type, Accept' 
    
        return resp
    except:
        r = {
            'success': False,
            'request': content,
            'msg': "Wrong Parameters"            
        }
        
        resp = Response(json.dumps(r))
        resp.headers['Content-Type'] = 'application/json'
        resp.headers['Access-Control-Allow-Origin'] =  '*' #! CORS
        resp.headers['Access-Control-Allow-Headers'] =  'Origin, X-Requested-With, Content-Type, Accept'  
    
        return resp


if __name__ == '__main__':
    app.run(debug=True)