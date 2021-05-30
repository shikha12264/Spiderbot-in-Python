import requests
import validators
import time
from datetime import datetime, timedelta
from urllib.parse import urljoin
from bs4 import BeautifulSoup as bs    
from pymongo import MongoClient
import dns

url = "https://flinkhub.com/"

#getting request from url
lnk = requests.get(url)

print("Flinkhub Link:",lnk.url)

print("Html Tags:",lnk.text)
# printing raw content of the specified url

# Connection to Mongodb
client = MongoClient("mongodb+srv://test:test@cluster0.0del1.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
# accessing MongoDB Atlas with pymongo MongoClient
# creating an instance of Mongoclient

db = client.get_database('shikha_db')
#connecting to my database 'shikha_db' using get_database through object 'db'
# now db is an reference of shikha_db databsse

records = db.web_scraper
# testing collection connection
# connecting to the collection (web_scraper) via db object (shikha_db)

cnt = records.count_documents({})
print('Count before Insertion:',cnt)
#count_documents is a method to get the count of documents under
#collections(records)
                                     
        
#validate an URL by checking whether a particular url returns a valid response or not
def Validlnk(sourceLink) :
    try:
        response = requests.get(sourceLink)
        return True
    except:
        return False

#function to check whether particular link already exists
def alreadyExists(lnk):
    try :
        filtr =(list(records.find({"Link":lnk})))
        #finding a particular document providing key value pair using find_one method
        #finding all the documents using find method so this becomes an iterator and using type conversion to list we get
        #a list of iterative objects        
        if records.count_documents(filtr) > 0 :
        #check if any such list exists previously i.e. if count is great than 0 , return true
            return True                   
    except :
         return False
    
    
    
soup = bs(lnk.text, 'html.parser')          # Create a BeautifulSoup object& parsing all html tags using html.parser
atags = soup.find_all("a", href=True)       # finding all anchor tags having href attribute

for i in atags:   
    atag = i["href"]              #retrieved all the links
    if (atag != ' '):           #check if the href attribute is not an empty element and perform only if it has content in it
        
            if (Validlnk(atag) and  not alreadyExists(atag)):       #Function calls to validate url as well as check whether url previously exists        
                records.insert_one({"Link": atag, "createdAt":datetime.today().replace(microsecond=0)})
                print("Inserted link")
                #link = {"lnk":"https://flinkhub.com/"}
                #insert_one method to insert one single document
                #records.insert_one(link)

                ##link2 = [{'cbjsab':'gh'},{'ahdujhn':'fg'}]
                ##records.insert_many(link2)
                ###insert_many method to insert multiple documents
            
    else:
        print("Issue")
           

#Count of links after insertion

cnt2 = records.count_documents({})
print('Count of links after insertion:',cnt2)


            

  
  
  
  
  
