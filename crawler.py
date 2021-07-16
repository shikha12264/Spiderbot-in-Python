import requests
import validators
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from database import insertLinkInDatabase, connectToDatabase
from cfg import SLEEP_INTERVAL
import time
import uuid


#function to count time at 24 hours ago
def time24HoursAgo() :
        today = datetime.today()                                  #it gives todays date and time
        BackTo24Hours = today - timedelta(days=1)                 #it calculates time for 24 hours ago & stores it in 'days_back' variable
        return BackTo24Hours                                      #return datetime


        
#function to check whether link already exists
def isCrawledBefore(sourceLink):
    db = connectToDatabase()
    criteria = { '$and' : [{"link":sourceLink},{"createdAt": {"$gte": time24HoursAgo()}}] }     # '$and' operator joins two or more queries with a logical AND and returns the documents that match all the conditions.
    if (db.Links.count_documents(criteria) > 0) :                                               #find documents with given link and created time is less than24 hours
        db.Links.update_many({"link":sourceLink}, {"$set" : {
                'isCrawled': True,
                'lastCrawlDt': datetime.today().replace(microsecond=0),
                }})
        return True
    else :
        return False


#fuction to get HTML response and to store that response in the file 
def getResponse(sourceLink):
    response = requests.get(sourceLink)                                  #send request to server and server will send 'response HTLML'
    return response

    
def saveFile(sourceLink):
    response = getResponse(sourceLink)    
    filename = str(uuid.uuid4().hex)                                     #produce a random name for the file
    filePath = "HTML_response/{}.html".format(filename)
    f = open(filePath, "wb")             #Open file from the current directory for reading
    f.write(response.content)                                            #write content in the file
    f.close()
    return filePath


#funtion is defined for crawling process
def scrapeCycle(sourceLink): 
    response = getResponse(sourceLink)  
    parse_content = BeautifulSoup(response.text, 'html5lib')             #parse 'response HTML' using BeautifulSoup
    count = 0                                                            #'count' is defined to count no of links scraped in a cycle
            
    for i in parse_content.find_all('a', href=True):                     #extract <a> tag from parse content
        if(i['href'].startswith("/")):
            temp = sourceLink + i['href']
            if ( not isCrawledBefore(temp) ):                                  #if link is not crawled in last 24 hours then insert it to the database
                insertLinkInDatabase(temp, sourceLink, getResponse(temp), saveFile(temp), '')
                count+=1                              

        elif(i['href'].startswith('h')) :
            if ( not isCrawledBefore(i['href']) ):
                insertLinkInDatabase(i['href'], sourceLink, getResponse(i['href']), saveFile(i['href']), '')
                count+=1

    if (count==0):
        print("All links crawled")
    
    time.sleep(SLEEP_INTERVAL)


    

