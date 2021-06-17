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
    cnt = records.count_documents({})
    if cnt >= 5000:
        print("Maximum limit Reached")
    print('Count before Insertion:',cnt)
    #count_documents is a method to get the count of documents under
    #collections(records)


def write_html(lnk):
    response = requests.get(lnk)                                         
    f = open("Html", "wb")                                               #Open a new file for writing
    f.write(response.content)                                            #write content in the file
    f.close()

def already_exists(url, collection):
    data = collection.find({ "Link": url})
    for d in data:                                                        # check for already existing links
        return True
    return False

def Insert_lnk(url, collection, source_Link):
    try:
        res = requests.get(url)
        if not already_exists(res.url, collection):
            soup = BeautifulSoup(res.content, 'html5lib')                       # Create a BeautifulSoup object& parsing all html tags using html.parser
            random_file = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 10))        
            with open('htmlFiles/{}.html'.format(random_file), 'w', encoding="utf-8") as file:
                file.write(soup.prettify())
            file_path = ((os.path.dirname(__file__)) + '\htmlFiles\{}.html'.format(random_file)) 
            lnk = {
                'Link': res.url,
                'Source_Link': source_Link,
                'Is_Crawled': False,
                'Last_Crawl_Dt': '',
                'Created_at': datetime.now()
            }
            collection.insert_one(lnk)
            print(res.url)
    except Exception as error:
        print(error)
        pass
    
 # function for links which hasnt been inserted
def notins_lnk(collection):
    links = collection.find({"$or": [{"Is_Crawled": False},{"Last_Crawl_Dt":{ "$lt": datetime.now() - timedelta(days=1)}}]})
    return links

# function to update the document
def modify_coll(document, collection):
    collection.update_one({ "_id": document["_id"]}, { "$set": {
        'Is_Crawled': True,
        'Last_Crawl_Dt': datetime.now()
    }})

 #function to crawl links
def crawl(document, collection):
    modify_coll(document, collection)
    response = getResponse(document["Link"], 10)
    links = getValidLinks(response)
    for link in links:
        if documentCount(collection) >=5000:
            raise Exception("Maximum Limit Reached")
        Insert_lnk(link, collection, document["Link"])


#function to validate links
def getValidLinks(response):
    links = []
    soup = BeautifulSoup(response.content, 'html5lib')
    href = soup.find_all('a', href = True)

    for href in href:
        if href.get('href').startswith("#") or href.get('href').startswith("tel:") or href.get('href').startswith("javascript:;") or href.get('href').startswith(" "):
            continue

        if href.get('href').startswith("https://") or href.get('href').startswith("http://"):
            links.append(href.get('href'))
            continue

        if href.get('href').startswith("/"):
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
            if cnt >= 5000:
                print("Maximum limit Reached")
            documents = notins_lnk(collection)
            all_crawled = True
            with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
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
