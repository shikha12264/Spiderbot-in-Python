from cfg import databaseName, MAX_LINK_LIMIT
from pymongo import MongoClient
from datetime import datetime

def connectToDatabase():
    client = MongoClient()                                             #instablish a MongoDB connection
    db = client[databaseName]                                          #define the MongoDB collection
    return db

def insertLinkInDatabase(l, sourceLink, response, filePath, lastCrawlDt) :
    db = connectToDatabase()
    document = {
            'link': l,
            'sourceLink': sourceLink,
            'isCrawled': False,
            'lastCrawlDt': lastCrawlDt,
            'responseStatus': response.status_code if response else '',
            'contentType': response.headers['Content-Type'] if "Content-Type" in response.headers else '',
            'contentLength': response.headers['Content-Length']  if "Content-Length" in response.headers else '',
            'filePath': filePath,
            'createdAt': datetime.today().replace(microsecond=0)          #if URL is valid and not present in database, insert link and time into database
    }
    db.Links.insert_one(document)

    if db.Links.count_documents({}) >= MAX_LINK_LIMIT:
        print("Maximum limit reached")
        

def getLinks() :
    db = connectToDatabase()
    pendingLinks = []
    for i in db.Links.find():
        pendingLinks.append(i['link'])
    return pendingLinks
