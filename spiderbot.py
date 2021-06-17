import requests
import validators
import time
import uuid
from datetime import datetime, timedelta
from urllib.parse import urljoin
from bs4 import BeautifulSoup as bs    # using allias bs
from pymongo import MongoClient
from concurrent.futures import ThreadPoolExecutor
import dns


def db_conn():
    client = MongoClient("mongodb+srv://test:<password>@cluster0.0del1.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
    # Connection to Mongodb
    # accessing MongoDB Atlas with pymongo MongoClient
    # creating an instance of Mongoclient
    db = client.get_database('shikha_db')
    #connecting to my database 'shikha_db' using get_database through object 'db'
    # now db is an reference of shikha_db databsse
    collection = db.web_scraper
    # testing collection connection
    # connecting to the collection (web_scraper) via db object (shikha_db)
    return collection
    ##cnt = records.count_documents({})
    ##if cnt >= 5000:
     ##   print("Maximum limit Reached")
    ##print('Count before Insertion:',cnt)
    #count_documents is a method to get the count of documents under
    #collections(records)


def write_html(lnk):
    response = requests.get(lnk)                                         
    f = open("Html", "wb")                                               #Open a new file for writing
    f.write(response.content)                                            #write content in the file "Html"
    f.close()
    
    
 # check for already existing links
def already_exists(url, collection):
    al_lnk = collection.find({ "Link": url})                              #finding a particular document providing key value pair using find_one method
        #finding all the documents using find method so this becomes an iterator and using type conversion to list we get
        #a list of iterative objects 
    for i in al_lnk:                                                       
        return True
    return False

def Insert_lnk(url, collection, source_Link):
    try:
        res = requests.get(url)
        if not already_exists(res.url, collection):
            soup = BeautifulSoup(res.content, 'html5lib')                       # Create a BeautifulSoup object& parsing all html tags using html.parser
              lnk = {
                'Link': res.url,
                'Source_Link': source_Link,
                'Is_Crawled': False,
                'Last_Crawl_Dt': '',
                'Created_at': datetime.now()
            }
            collection.insert_one(lnk)                      
                #insert_one method to insert one single document
                #records.insert_one(link)
                ##link2 = [{'cbjsab':'gh'},{'ahdujhn':'fg'}]
                ##records.insert_many(link2)
                ##insert_many method to insert multiple documents  
            print(res.url)
    except Exception as error:
        print(error)
        pass
    
 # function to keep a track of links which hasnt been inserted
def notins_lnk(collection):
    links = collection.find({"$or": [{"Is_Crawled": False},{"Last_Crawl_Dt":{ "$lt": datetime.now() - timedelta(days=1)}}]})
    return links

# function to update the document
def modify_coll(document, collection):
    #updateOne() method updates a first matched document within the collection based on the given query. 
    # updating your document the value of the _id field remains unchanged. 
    collection.update_one({ "_id": document["_id"]}, { "$set": {
        'Is_Crawled': True,
        'Last_Crawl_Dt': datetime.now()
    }})

 #function to crawl all the links
def crawl(document, collection):
    modify_coll(document, collection)
    response = getResponse(document["Link"], 10)
    links = getValidLinks(response)
    for link in links:
        if documentCount(collection) >=5000:
            #crawling the links if it exceeds the recursion limit , raise an exception
            raise Exception("Maximum Limit Reached")
        Insert_lnk(link, collection, document["Link"])


#function to validate links
def getValidLinks(response):
    links = []        
    #creating an empty list links
    soup = BeautifulSoup(response.content, 'html5lib')         # Create a BeautifulSoup object& parsing all html tags using html.parser
    # finding all anchor tags having href attribute
    href = soup.find_all('a', href = True)            # retrieved all the links having href attribute
        #finding all the documents using find method so this becomes an iterator and using type conversion to list we get
        #a list of iterative objects  
    for i in href:
        x = i.get('href')
        if x.startswith("#") or href.get('href').startswith("tel:") or href.get('href').startswith("javascript:;") or href.get('href').startswith(" "):
            continue
        #condition check for absolute urls
        # if condition to check whether href attribute starts with these particular extensions so ignore them
        if x.startswith("https://") or href.get('href').startswith("http://"):
            links.append(href.get('href'))
            continue
         # if condition to check whether href attribute starts with these particular extensions https or http append them to the links list
        if x.startswith("/"):
            # if condition to check whether href attribute starts with / i.e. checking whether it's a relative url
            temp_url = response.url
            temp_index = find_index(temp_url)
            newurl = temp_url.replace(temp_url[temp_index:],"") + href.get('href').replace("/","")
            links.append(newurl)
    
    return links

#main() function 
if __name__ == '__main__' :       
        url = "https://flinkhub.com/"             #define the sourceLink
        write_html(url)
        collection = db_conn()
        Insert_lnk(url, collection, "")

        while True:
            cnt = collection.count_documents({})   
            #count_documents is a method to get the count of documents under
             #collections(records)
            if cnt >= 5000:                
                print("Maximum limit Reached")
            documents = notins_lnk(collection)
            all_crawled = True
            with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:           #ThreadPoolExecutor is library in python which is used to implement multithreading
                futures = []
                try:
                    for document in documents:
                        all_crawled = False
                        futures.append(executor.submit(crawl, document, collection))
                    for future in concurrent.futures.as_completed(futures):
                        future.result()
                except Exception as error:
                    print(error)
                    break
            if all_crawled:
                print("All links are crawled!")
                break
