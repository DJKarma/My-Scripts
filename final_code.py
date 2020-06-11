
#In[1]:

import pandas as pd
import numpy as np
from nltk.util import ngrams
from nltk.tokenize import RegexpTokenizer
from nltk.probability import FreqDist
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
import re
import nltk
import collections
import time
import datetime
from datetime import date


def cleaned_tweet():
    tweet= pd.read_excel(r'C:\Users\P10496990\Documents\Copy of Next_Tweets.xlsx')
    #cleaning location
    tweet['Location']= tweet['Location'].apply(lambda x:str(x).lower())
    tweet['Location'].fillna("No_Location", inplace = True)

    tweet['Location']=tweet['Location'].replace('^nan$',"No_Location",regex=True)
    tweet['Location']=tweet['Location'].replace('uk',"united kingdom",regex=True)
    tweet['Location']=tweet['Location'].replace('UK',"united kingdom",regex=True)
    tweet['Location']=tweet['Location'].replace('U.K.',"united kingdom",regex=True)
    tweet['Location']=tweet['Location'].replace('u.k.',"united kingdom",regex=True)

    tweet.loc[tweet['Location'].str.contains('london',case=False),'Location']='london'
    tweet.loc[tweet['Location'].str.contains('manchester',case=False),'Location']='manchester'
    tweet.loc[tweet['Location'].str.contains('glasgow',case=False),'Location'] = 'glasgow'
    tweet.loc[tweet['Location'].str.contains('dublin',case=False),'Location'] = 'dublin'
    tweet.loc[tweet['Location'].str.contains('liverpool',case=False),'Location'] = 'liverpool'
    tweet.loc[tweet['Location'].str.contains('leeds',case=False),'Location'] = 'leeds'
    tweet.loc[tweet['Location'].str.contains('yorkshire',case=False),'Location'] = 'yorkshire'
    tweet.loc[tweet['Location'].str.contains('cardiff',case=False),'Location'] = 'cardiff'
    tweet.loc[tweet['Location'].str.contains('dundee',case=False),'Location'] = 'dundee'
    tweet.loc[tweet['Location'].str.contains('birmingham',case=False),'Location'] = 'birmingham'
    tweet.loc[tweet['Location'].str.contains('barry',case=False),'Location'] = 'barry'
    tweet.loc[tweet['Location'].str.contains('edinburgh',case=False),'Location'] = 'edinburgh'
    tweet.loc[tweet['Location'].str.contains('midlands',case=False),'Location'] = 'midlands'
    tweet.loc[tweet['Location'].str.contains('scotland',case=False),'Location'] = 'scotland'
    tweet.loc[tweet['Location'].str.contains('ireland',case=False),'Location'] = 'ireland'
    tweet.loc[tweet['Location'].str.contains('wales',case=False),'Location'] = 'wales'
    tweet.loc[tweet['Location'].str.contains('england',case=False),'Location'] = 'england'
    tweet.loc[tweet['Location'].str.contains('united kingdom',case=False),'Location'] = 'unitedkingdom'
    
    

    tweet['Location']= tweet['Location'].apply(lambda x:str(x).lower())
    tweet['Week Start'] = (tweet['TwittedAt'] - pd.offsets.Week(weekday=0)).dt.strftime('%m/%d/%Y')
    tweet['Week End'] = (tweet['TwittedAt'] + pd.offsets.Week(weekday=6)).dt.strftime('%m/%d/%Y')
    return tweet
#cleaning done

#each function needs this tweet ...cleaned one



#In[8]:
"""
Extra:

 tweet=cleaned_tweet()   
 tweet['TwittedAt'] = (tweet['TwittedAt']).dt.strftime(' %m/%d/%Y')
 tweet=tweet.groupby(['Week End','TwittedAt'])['Tweet'].count()  #weekly grouped data
 tweet
 group=tweet.groupby(['Week End']) #max tweets in a day
 group.max()
""" 




#In[4]:



def get_reach_weekly(tweet):
    tweet =tweet.groupby( pd.Grouper(key='TwittedAt', freq='W'))['Reach'].sum().reset_index().sort_values('TwittedAt')
    print(tweet)
    
def get_tweet_count_weekly(tweet):
    tweet =tweet.groupby( pd.Grouper(key='TwittedAt', freq='W'))['Tweet'].count().reset_index().sort_values('TwittedAt')
    print(tweet)
    
    
def weekly_data(tweet):  #check for the peak day,max tweet in a day & top five words
    tweet =tweet.groupby( pd.Grouper(key='TwittedAt', freq='D'))['Tweet'].count().reset_index()
    g=tweet.groupby( pd.Grouper(key='TwittedAt', freq='W'))    #for monthly analysis ,use freq='M'
    print("----max tweet in a day per week-----")
    print(g.max())
    print("************weekly data***********")
    new=cleaned_tweet()
    for TwittedAt,TwittedAt_tweet in g:
        print(TwittedAt)
        print("--------------------")
        print(TwittedAt_tweet) 
        print("--------------------")
        print("TOP FIVE WORDS :")        
        date1=TwittedAt.strftime('%m/%d/%Y')
        y=top_five(get_text_weekly(date1,new))    
        print(y)
        print("------------------------------------------------------------------------------------")
        print("\n\n")




#In[74]:
def  get_reach_location(loc1,tweet):
    tweet =tweet.groupby( pd.Grouper(key='Location'))['Reach'].sum().reset_index()
    g=tweet.groupby('Location')  
    return  g.get_group(loc1)  
        
def  get_tweet_count_location(loc1,tweet):
    tweet =tweet.groupby( pd.Grouper(key='Location'))['Tweet'].count().reset_index()
    g=tweet.groupby('Location')  
    return g.get_group(loc1)  

def get_location_data(loc): #get whole data about tweet count and reach for the top 5 locations
    for elt in loc:
        loc1=elt[0]
        tweet=cleaned_tweet()
        m=get_tweet_count_location(loc1,tweet) #calling function for tweet count
        print(m)
        n=get_reach_location(loc1,tweet) #for reach
        print(n)
        l=top_five(get_text_location(loc1,tweet))#for top five words of that location
        print(l)
        print("----------------------------------------------------------")
        print("----------------------------------------------------------")
        print("\n\n")




#In[79]:
# getting top five words 

def get_text_location(loc1,tweet): #location_based
    tweet =tweet.groupby( pd.Grouper(key='Location'))
    tweet=tweet.get_group(loc1)
    text=tweet['Tweet'].T.tolist()
    return text

def get_text_weekly(week,tweet): #weekly
    tweet =tweet.groupby( pd.Grouper(key='TwittedAt',freq='W'))    #for monthly analysis ,use freq='M'
    tweet=tweet.get_group(week)
    text=tweet['Tweet'].T.tolist()
    return text

def top_location(tweet):  #location
    text=tweet['Location'].T.tolist()
    return text

def top_five(text):
        
        from progressbar import ProgressBar
        pbar = ProgressBar()
        djstr=" ".join(str(x) for x in pbar(text))
        k=0
        frequency = {}
        match_pattern = re.findall(r'\b[a-z]{4,20}\b', djstr) #return all the words with the number of characters in the range [3-15]
        fdist = nltk.FreqDist(match_pattern) # creates a frequency distribution  from a list
        fdist
        stopwords = set(STOPWORDS)
        stopwords.add("nextofficial")
        stopwords.add("https")
        stopwords.add("will")
        stopwords.add("store")
        stopwords.add("next")
        stopwords.add("co")

        for i in stopwords:
            try:
                fdist.pop(i)
            except:
                k=k+1
        top_five = fdist.most_common(5)# returns a list|
        wordcloud = WordCloud(background_color="black",stopwords = stopwords).generate(djstr)
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        plt.show()
        return top_five

#In[81]:

tweet=cleaned_tweet()      #weekly analysis
get_reach_weekly(tweet) 
    
#In[82]:
tweet=cleaned_tweet()
get_tweet_count_weekly(tweet)
        
#In[83]:
tweet=cleaned_tweet()
weekly_data(tweet)

#In[27]:
tweet=cleaned_tweet()     #location based analysis
x=top_five(top_location(tweet))
print(x)
print("\n\n\n")
get_location_data(x) 



#In[101]:

                                           #overall analysis
tweet=cleaned_tweet()     
tweet=tweet.groupby( pd.Grouper(key='UserName'))['Tweet'].count().reset_index()
tweet.sort_values(["Tweet"], axis=0,ascending=False, inplace=True) 
print(tweet.head(10))       #top ten most active accounts

#In[102]:
tweet=cleaned_tweet()
tweet.drop_duplicates(subset ="UserName", keep ="last", inplace = True) 
tweet.sort_values(["Reach"], axis=0,ascending=False, inplace=True) 
tweet.head(10)      #highest contributers


#In[103]:
tweet=cleaned_tweet()
tweet['Reach'].sum()    #total reach

#In[104]:
tweet=cleaned_tweet()
tweet['Tweet'].count()   #total number of tweets




"""
For trimmed file (used for Plotting):
#In[279]:
pd.set_option('display.max_rows', 1000)
tweet=cleaned_tweet()
tweet =tweet.groupby( pd.Grouper(key='Location'))['Reach'].sum().reset_index()
tweet
#In[302]:
pd.set_option('display.max_rows', 1000)
tweet=cleaned_tweet()
tweet =tweet.groupby( pd.Grouper(key='Location'))['Tweet'].count().reset_index()
tweet

"""