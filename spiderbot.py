import requests
import validators
import time
from urllib.parse import urljoin
from bs4 import BeautifulSoup as bs # using allias bs
url = "https://flinkhub.com/"
lst = []
#getting request from url
lnk = requests.get(url)
print("Flinkhub Link:",lnk.url)   #printing url
print("Html Tags:",lnk.text)  #printing raw content of the specified url
# Create a BeautifulSoup object
soup = bs(lnk.text, 'html.parser') #parsing all html tags
atags = soup.find_all("a", href=True)
for i in atags: #finding all anchor tags
    #retrieved all the links
    atag = i["href"]
    # Retrieve the href attribute from the anchor tag
    if (atag != ' '):
        #check if the href attribute is not an empty element and perform only if it has content in it
        
        rellnk = urljoin("https://flinkhub.com",i["href"])     
        #If you want to know if an URL is absolute or relative link
        #in order to join it with a base URL, use urllib.parse.urljoin anyway     

        if rellnk not in lst:
            lst.append(rellnk)
            
print("List of valid links scraped:")
print(lst)

print("Length of list i.e. number of valid links present:")
print(len(lst))   #16 valid links with no repetition
