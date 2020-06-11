import requests
from bs4 import BeautifulSoup
import redis
#from secret import password
import datetime
import pandas as pd
import re
import numpy as np

"""
Y NEWS

"""
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





"""
Daily Mail Scraper

"""

# url definition
url = "https://www.dailymail.co.uk"

# Request
r1 = requests.get(url)
r1.status_code

   # We'll save in coverpage the cover page content
coverpage = r1.content

   # Soup creation
soup1 = BeautifulSoup(coverpage, 'html5lib')

   # News identification
coverpage_news = soup1.find_all('h2', class_='linkro-darkred')
alldailymail=len(coverpage_news)

number_of_articles = alldailymail-10

   # Empty lists for content, links and titles
news_contents = []
list_links = []
list_titles = []

for n in np.arange(0, number_of_articles):
   # Getting the link of the article
   link = url + coverpage_news[n].find('a')['href']
   list_links.append(link)

   # Getting the title
   title = coverpage_news[n].find('a').get_text()
   list_titles.append(title)

   # Reading the content (it is divided in paragraphs)
   article = requests.get(link)
   article_content = article.content
   soup_article = BeautifulSoup(article_content, 'html5lib')
   body = soup_article.find_all('p', class_='mol-para-with-font')

   # Unifying the paragraphs
   list_paragraphs = []
   for p in np.arange(0, len(body)):
       paragraph = body[p].get_text()
       list_paragraphs.append(paragraph)
       final_article = " ".join(list_paragraphs)
       # Removing special characters
   final_article = re.sub("\\xa0", "", final_article)
   news_contents.append(final_article)



   # df_show_info
dailynewsdf= pd.DataFrame(
   {'Article Title': list_titles,
'Article Link': list_links,
'Newspaper': url,'Content':news_contents})





"""
Guardian News SCRAPER

"""
# url definition
url = "https://www.theguardian.com/uk"

# Request
r1 = requests.get(url)
r1.status_code

# We'll save in coverpage the cover page content
coverpage = r1.content

# Soup creation
soup1 = BeautifulSoup(coverpage, 'html5lib')

# News identification
coverpage_news = soup1.find_all('h3', class_='fc-item__title')
allguardian=len(coverpage_news)

number_of_articles = allguardian-10

# Empty lists for content, links and titles
news_contents = []
list_links = []
list_titles = []

for n in np.arange(0, number_of_articles):

    # We need to ignore "live" pages since they are not articles
    if "live" in coverpage_news[n].find('a')['href']:
        continue

    # Getting the link of the article
    link = coverpage_news[n].find('a')['href']
    list_links.append(link)

    # Getting the title
    title = coverpage_news[n].find('a').get_text()
    list_titles.append(title)

    # Reading the content (it is divided in paragraphs)
    article = requests.get(link)
    article_content = article.content
    soup_article = BeautifulSoup(article_content, 'html5lib')
    body = soup_article.find_all('div', class_='content__article-body from-content-api js-article__body')
    try:
        x = body[0].findall('p')
        # Unifying the paragraphs
        list_paragraphs = []
        for p in np.arange(0, len(x)):
            paragraph = x[p].get_text()
            #list_paragraphs.append(paragraph)
            final_article = " ".join(list_paragraphs)
    except:
        final_article=" "

    news_contents.append(final_article)

# df_features
gnewsdf= pd.DataFrame(
   {'Article Title': list_titles,
'Article Link': list_links,
'Newspaper': url,'Content':news_contents})





"""

Keyword Matching and Combining all DATA

"""
frames=[gnewsdf,dailynewsdf,ynewsdf]

newsdf = pd.concat(frames,ignore_index=True)
newsdf=newsdf.drop_duplicates(subset='Article Title', keep="first")
newsdf=newsdf.reset_index()
newsdf=newsdf.drop(columns=['index'])
supplierdf=pd.read_excel('supp.xlsx',headers=True)
supplierdf['name'] = supplierdf['name'].str.strip()
supplierlist=supplierdf['name'].values.tolist()

text=newsdf['Article Title'].values.T.tolist() #converting the same column to lists
text= [k.lower() for k in text]
commentlist=[]
keywordlist=[]
supplierlist= [k.lower() for k in supplierlist]

for i in range(len(supplierlist)):
    for index in range(len(text)):
        result = re.search(r'\s*\b'+supplierlist[i]+r'\W*\s', text[index])

        if result:
            commentlist.append(text[index])
            keywordlist.append(supplierlist[i])







#apikey=b320e2b793644396bdbeded93ff9d702



