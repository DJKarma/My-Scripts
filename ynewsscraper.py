import requests
from bs4 import BeautifulSoup
import redis
#from secret import password
import datetime
import pandas as pd
import re
url='https://news.ycombinator.com/'
markup = requests.get(url).text
keywords = [' ']
soup = BeautifulSoup(markup, 'html.parser')
links = soup.findAll("a", {"class": "storylink"})
list_links=[]

#getting thaaa links baby
for i in range(len(links)):
    linkdj = links[i]['href']
    list_links.append(linkdj)


#just wrote an extra loop, i dont know why but gets the work done.
saved_links = []
for link in links:
    for keyword in keywords:
        if keyword in link.text:
            saved_links.append(link)

flink=[]
flinktext=[]

#appending everything so later to convert to df
for link in saved_links:
    flinktext.append(link.text)



#creating the dataframe
ynewsdf= pd.DataFrame(
   {'Article Title': flinktext,
'Article Link': list_links,
'Newspaper': url,'Content':''})
