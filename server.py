from fetch import Fetch
from parsing import Parser
from flask import Flask, Response, json, request
import json

# Todo User System.
# Todo 2 Database Implentation.

newFetcher = Fetch()

app = Flask(__name__)

@app.route("/", methods=['GET'])
def index():
    r = {
        'success': True,
        'msg': "Server Index Point ..."
    }
    resp = Response(json.dumps(r))
    resp.headers['Content-Type'] = 'application/json'
    return resp

@app.route("/add", methods=['POST'])
def addURL():
    content = request.json
    newFetcher.addURL(content['URL'])

    r = {
        'success': True,
        'msg': "URL Added ..."
    }
    
    resp = Response(json.dumps(r))
    resp.headers['Content-Type'] = 'application/json'
    return resp

@app.route("/get", methods=['GET'])
def getAllRSS():
    datas = newFetcher.fetchAll()
    rssList = []    

    for data in datas:
        rss = Parser.convertFromXML(data)
        d = {
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
    
    return resp

@app.route("/getone", methods=['POST'])
def getOneRSS():
    content = request.json
    data = newFetcher.fetchOne(content['URL'])

    rss = Parser.convertFromXML(data)
    d = {
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
    
    return resp


if __name__ == '__main__':
    app.run(debug=True)