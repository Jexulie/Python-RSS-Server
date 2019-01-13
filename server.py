from fetch import Fetch
from parsing import Parser, idGenerator
from flask import Flask, Response, json, request
from database import addDB, updateDB, removeDBbyCID, removeDBbyURL, getDBbyCID, getDBbyURL, getAllDB
import json
import re

# Todo User System.
# Todo 2 Database Implentation.
# Todo 3 on Wrong RSS remove added URL and send back response.
# Todo 4 If URL already exists reject
# Todo 5 Proper Err msging and on resp

newFetcher = Fetch()

app = Flask(__name__)

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
    resp.headers['Access-Control-Allow-Methods'] = 'GET'
    return resp

@app.route("/add", methods=['POST', 'OPTIONS'])
def addURL():
    # Todo Do this to every route - pitfall rescue
    content = request.json
    try:
        url = content['URL']
        # future Test URL HERE THEN RESPOND
        if checkURL(url):
            r = {
                'success': True,
                'msg': "URL Added ..."
            }
            try:
                if getDBbyURL(url) is None:
                    addDB(idGenerator(15), url)
                else:
                    r = {
                        'success': False,
                        'msg': 'Duplicate URL ...'
                    }
            except Exception as err:
                print(err)
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
        resp.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
        resp.headers['Access-Control-Allow-Headers'] =  'Origin, X-Requested-With, Content-Type, Accept' 

        return resp
    except Exception as err:
        print(err)
        r = {
            'success': False,
            'request': content,
            'msg': "Wrong Parameters"   
        }
        
        resp = Response(json.dumps(r))
        resp.headers['Content-Type'] = 'application/json'
        resp.headers['Access-Control-Allow-Origin'] =  '*' #! CORS
        resp.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
        resp.headers['Access-Control-Allow-Headers'] =  'Origin, X-Requested-With, Content-Type, Accept' 

        return resp

@app.route("/get", methods=['GET'])
def getAllRSS():
    resp = getAllDB()
    datas = newFetcher.fetchAll(resp)

    rssList = []

    for data in datas:
        rss = Parser.convertFromXML(data['xml'])
        if rss != False:
            d = {
                'cid': data['cid'],
                'url': data['url'],
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
    resp.headers['Access-Control-Allow-Methods'] = 'GET'
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
            resp.headers['Access-Control-Allow-Methods'] = 'OPTIONS, POST'
            resp.headers['Access-Control-Allow-Headers'] =  'Origin, X-Requested-With, Content-Type, Accept' 

            return resp

        if rss == False:
            removeDBbyURL(content['URL'])
            r = {
                'success': False,
                'msg': "Parsing Error ..."
            }

            resp = Response(json.dumps(r))
            resp.headers['Content-Type'] = 'application/json'
            resp.headers['Access-Control-Allow-Origin'] =  '*' #! CORS
            resp.headers['Access-Control-Allow-Methods'] = 'OPTIONS, POST'
            resp.headers['Access-Control-Allow-Headers'] =  'Origin, X-Requested-With, Content-Type, Accept' 

            return resp
        else:
            db_resp = getDBbyURL(content['URL'])
            if db_resp is None:
                cid = idGenerator(15)
                r = addDB(cid, content['URL'])
                if r == False:
                    a = updateDB(cid, content['URL'])
                    print(a, r)
            d = {
                'cid': db_resp['cid'],
                'url': content['URL'],
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
            resp.headers['Access-Control-Allow-Methods'] = 'OPTIONS, POST'
            resp.headers['Access-Control-Allow-Headers'] =  'Origin, X-Requested-With, Content-Type, Accept' 
    
            return resp

    except Exception as err:
        print(err)
        r = {
            'success': False,
            'request': content,
            'msg': "Wrong Parameters"
        }
        
        resp = Response(json.dumps(r))
        resp.headers['Content-Type'] = 'application/json'
        resp.headers['Access-Control-Allow-Origin'] =  '*' #! CORS
        resp.headers['Access-Control-Allow-Methods'] = 'OPTIONS, POST'
        resp.headers['Access-Control-Allow-Headers'] =  'Origin, X-Requested-With, Content-Type, Accept'  
    
        return resp

@app.route("/refresh", methods=['POST', 'OPTIONS'])
def refresh():
    try:
        content = request.json
        cid_req = content['CID']

        url = getDBbyCID(cid_req)

        if url is not None:
            data = newFetcher.fetchOne(url)
            new_rss = Parser.convertFromXML(data)
            d = {
                'cid': cid_req,
                'url': url,
                'title': new_rss.title,
                'link': new_rss.link,
                'description': new_rss.desc,
                'itemList': new_rss.itemList
            }
            r = {
                'success': True,
                'data': d
            }
            resp = Response(json.dumps(r))
            resp.headers['Content-Type'] = 'application/json'
            resp.headers['Access-Control-Allow-Origin'] =  '*' #! CORS
            resp.headers['Access-Control-Allow-Methods'] = 'OPTIONS, POST'
            resp.headers['Access-Control-Allow-Headers'] =  'Origin, X-Requested-With, Content-Type, Accept' 
            return resp
        
        r = {
            'success': False,
            'msg': "RSS Not Found ..."
        }

        resp = Response(json.dumps(r))
        resp.headers['Content-Type'] = 'application/json'
        resp.headers['Access-Control-Allow-Origin'] =  '*' #! CORS
        resp.headers['Access-Control-Allow-Methods'] = 'OPTIONS, POST'
        resp.headers['Access-Control-Allow-Headers'] =  'Origin, X-Requested-With, Content-Type, Accept' 

        return resp
    except Exception as err: 
        print(err)   
        r = {
            'success': False,
            'msg': "Wrong Parameters ..."
        }

        resp = Response(json.dumps(r))
        resp.headers['Content-Type'] = 'application/json'
        resp.headers['Access-Control-Allow-Origin'] =  '*' #! CORS
        resp.headers['Access-Control-Allow-Methods'] = 'OPTIONS, POST'
        resp.headers['Access-Control-Allow-Headers'] =  'Origin, X-Requested-With, Content-Type, Accept' 

        return resp

@app.route("/remove", methods=['DELETE', 'OPTIONS'])
def remove():
    if request.method == 'OPTIONS':
        resp = Response()
        resp.headers['Content-Type'] = 'application/json'
        resp.headers['Access-Control-Allow-Origin'] =  '*' #! CORS
        resp.headers['Access-Control-Allow-Methods'] = 'OPTIONS, DELETE'
        resp.headers['Access-Control-Allow-Headers'] =  'Origin, X-Requested-With, Content-Type, Accept'
        return resp 
    else:
        try:
            content = request.json
            print(content)
            a = removeDBbyCID(content['CID'])
            print(a)
            r = {
                'success': True,
                'msg': "RSS Removed ..."
            }
            
            resp = Response(json.dumps(r))
            resp.headers['Content-Type'] = 'application/json'
            resp.headers['Access-Control-Allow-Origin'] =  '*' #! CORS
            resp.headers['Access-Control-Allow-Methods'] = 'OPTIONS, DELETE'
            resp.headers['Access-Control-Allow-Headers'] =  'Origin, X-Requested-With, Content-Type,    Accept'  
        
            return resp
        except Exception as err:
            print(err)
            r = {
                'success': False,
                'request': content,
                'msg': "Wrong Parameters"
            }
            
            resp = Response(json.dumps(r))
            resp.headers['Content-Type'] = 'application/json'
            resp.headers['Access-Control-Allow-Origin'] =  '*' #! CORS
            resp.headers['Access-Control-Allow-Methods'] = 'OPTIONS, DELETE'
            resp.headers['Access-Control-Allow-Headers'] =  'Origin, X-Requested-With, Content-Type,    Accept'  
        
            return resp

if __name__ == '__main__':
    app.run(debug=True)