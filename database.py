import psycopg2

def newConnection():
    conn = psycopg2.connect(
        database='postgres', 
        user='server_api', 
        password='CXkaLaCWmfn2ct3V!', 
        host='192.168.0.27', 
        port='5432'
    )
    return conn

def addDB(cid, url):
    conn = newConnection()
    cur = conn.cursor()
    sql = f"""INSERT INTO SERVER.RSS (CID, URL) VALUES ('{cid}', '{url}')"""
    try:
        cur.execute(sql)
        conn.commit()
        return {'success': True, 'error': None}
    except Exception as err:
        print(err)
        return {'success': False, 'error': err}
    finally:
        conn.close()

#! why!?
def updateDB(cid, url):
    conn = newConnection()
    cur = conn.cursor()
    sql = f"""update server.rss set cid = '{cid}' where url = '{url}'"""
    try:
        cur.execute(sql)
        conn.commit()
        return {'success': True, 'error': None}
    except Exception as err:
        print(err)
        return {'success': False, 'error': err}
    finally:
        conn.close()

def removeDBbyCID(cid):
    conn = newConnection()
    cur = conn.cursor()
    sql = f"""DELETE FROM SERVER.RSS WHERE CID = '{cid}'"""
    try:
        cur.execute(sql)
        conn.commit()
        return {'success': True, 'error': None}
    except Exception as err:
        print(err)
        return {'success': False, 'error': err}
    finally:
        conn.close()

def removeDBbyURL(url):
    conn = newConnection()
    cur = conn.cursor()
    sql = f"""DELETE FROM SERVER.RSS WHERE URL = '{url}'"""
    try:
        cur.execute(sql)
        conn.commit()
        return {'success': True, 'error': None}
    except Exception as err:
        print(err)
        return {'success': False, 'error': err}
    finally:
        conn.close()

def getDBbyCID(cid):
    conn = newConnection()
    cur = conn.cursor()
    sql = f"""SELECT URL FROM SERVER.RSS WHERE CID = '{cid}'"""
    try:
        cur.execute(sql)
        rows = cur.fetchall()
        for row in rows:
            return row[0]
    except Exception as err:
        print(err)
    finally:
        conn.close()

def getDBbyURL(url):
    conn = newConnection()
    cur = conn.cursor()
    sql = f"""SELECT CID, URL FROM SERVER.RSS WHERE URL = '{url}'"""
    try:
        cur.execute(sql)
        rows = cur.fetchall()
        for row in rows:
            return {'cid': row[0], 'url': row[1]}
    except Exception as err:
        print(err)
    finally:
        conn.close()

def getAllDB():
    conn = newConnection()
    cur = conn.cursor()
    sql = f"""SELECT CID, URL FROM SERVER.RSS"""
    try:
        cur.execute(sql)
        rows = cur.fetchall()
        result = []
        for row in rows:
            result.append({'cid': row[0], 'url': row[1]})
        return result
    except Exception as err:
        print(err)
    finally:
        conn.close()