import requests
import validators
import time
from bs4 import BeautifulSoup as bs # using allias bs
url = "https://flinkhub.com/"
lst = []
#getting request from url
lnk = requests.get(url)
print("Flinkhub Link:",lnk.url)   #printing url
print("Html Tags:",lnk.text)  #printing raw content of the specified url

# Create a BeautifulSoup object
 
soup = bs(lnk.text, 'html.parser') #parsing all html tags
   
for i in soup.find_all("a", href=True): #finding all anchor tags 
    #retrieved all the links
    x = i["href"]
    valid = validators.url(x)  #retrieving all valid links
    if valid == True:
        lst.append(x)
print(lst)
