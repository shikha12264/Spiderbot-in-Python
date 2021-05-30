import requests
import validators
import time
from datetime import datetime, timedelta
from urllib.parse import urljoin
from bs4 import BeautifulSoup as bs    # using allias bs
from pymongo import MongoClient
import dns

url = "https://flinkhub.com/"

#getting request from url
lnk = requests.get(url)

print("Flinkhub Link:",lnk.url)
#printing url

print("Html Tags:",lnk.text)
#printing raw content of the specified url

client = MongoClient("mongodb+srv://test:test@cluster0.0del1.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client.get_database('shikha_db')
records = db.web_scraper
cnt = records.count_documents({})
print('Count:',cnt)

                                      #return datetime
        
#validate an URL using try & catch mechanism
def Validlnk(sourceLink) :
    try:
        response = requests.get(sourceLink)
        return True
    except:
        return False

#function to check whether link already exists

def alreadyExists(lnk):
    try :
        filtr =(list(records.find({"Link":lnk})))
        if records.count_documents(filtr) > 0 :
            return True                   
    except :
         return False
    
soup = bs(lnk.text, 'html.parser')
atags = soup.find_all("a", href=True)

for i in atags:   
    atag = i["href"]    
    if (atag != ' '):        
            if (Validlnk(atag) and  not alreadyExists(atag)):             
                records.insert_one({"Link": atag, "createdAt":datetime.today().replace(microsecond=0)})
                print("Inserted link")
            
    else:
        print("Issue")
           

print("Done")
z = records.count_documents({})
print('Count after insertion:',z)


            
