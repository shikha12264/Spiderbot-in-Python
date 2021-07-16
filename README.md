# Python-Web-Scrapper

Problem statement:

Build a spiderbot (web scraper) that continuously runs in the background and recursively scrapes all links it can find

Problem Details:

The Root URL for this project will be https://flinkhub.com . The Root URL must be manually entered into the database before the process starts. 

As soon as the process starts, it should check the “links” table for pending links to scrape. It should scrape all these links, extract all valid links (through <a> tags) 
from each of these pages, and save them in the database. It should also save the response HTML on the disk as a file with a random file name. This is considered as one 
scraping cycle. The process will then start the next cycle of scraping.

The process should sleep for 5 seconds between each cycle of scraping.

The process must be written inside an infinite loop i.e. it should never end and should start a new cycle 5 seconds after last cycle is complete.

The process should not scrape links that are scraped already in the last 24 hours.

The process should implement multithreading with 5 threads running parallelly i.e. it should be crawling up to 5 links in parallel.

The process should never crash and kill itself due to run-time errors. All run-time errors must be handled properly to keep the process running.

If all links have been scraped in last 24 hours and there are no new links, the process should just print “All links crawled” and consider that cycle as completed.

For the confines of this project, we will limit maximum number of links to 5000. i.e. Once the database has got 5000 links, the process should just print “Maximum limit reached” 
and consider that cycle as completed.
