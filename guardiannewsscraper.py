import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
import re



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
len(coverpage_news)

number_of_articles = 20

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