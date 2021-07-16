# File to store info about all variables related to application configuration

"""
main.py        -  file which has the main function
crawler.py     -  file which content user defined functions to carry out scraping
database.py    -  file which contest user defined functions to perform database operations
"""

# The url to start with
root_URL = https://flinkhub.com/

# Folder for storing retrieved html pages
HTML_response

# Maximum link limit that can be added in a database
MAX_LINK_LIMIT = 5000

# Database Name
databaseName = "Crawler"

# Table Name which stores data
tableName = Links


# Count of maximum thread that can be executed simultaneously
threadCount = 5

# Process will stop for specified amount of time after updates of all links i.e. each update cycle
# Format: in seconds
SLEEP_INTERVAL = 5
