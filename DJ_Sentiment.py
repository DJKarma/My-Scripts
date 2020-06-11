
"""
NLTK SENTIMENT -
positive sentiment: compound score >= 0.05
neutral sentiment: (compound score > -0.05) and (compound score < 0.05)
negative sentiment: compound score <= -0.05

TEXTBLOB -
Each word in the lexicon has scores for:
1)     polarity: negative vs. positive    (-1.0 => +1.0)
2)     subjectivity: objective vs. subjective (+0.0 => +1.0)
3)     intensity: modifies next word?      (x0.5 => x2.0)

"""

import pandas as pd
from progressbar import ProgressBar
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from textblob import TextBlob
import numpy as np


pbar = ProgressBar()
df = pd.read_excel('final.xlsx',dtype=str) #filename/filepath here
df['Comments']=df['Comments'].astype(str)
analyser = SentimentIntensityAnalyzer()

# add Text blob sentiment analysis column
df[['polarity', 'subjectivity']] = df['Comments'].apply(lambda Text: pd.Series(TextBlob(Text).sentiment))

# Add vander sentiment analysis column
df[['Negative', 'Neautral','Positive','compound']]=df['Comments'].apply(lambda Text: pd.Series(analyser.polarity_scores(Text)))

df['Sentiment']=np.nan
df['TBSentiment']=np.nan
df['Sentiment'] = np.where(df['compound'].between(-0.25,0.25), "Neutral", df['Sentiment'])
df['Sentiment'] = np.where(df['compound'].between(-0.25,-0.75), "Negative", df['Sentiment'])
df['Sentiment'] = np.where(df['compound']<-0.75, "V.Negative", df['Sentiment'])
df['Sentiment'] = np.where(df['compound'].between(0.25,0.75), "Positive", df['Sentiment'])
df['Sentiment'] = np.where(df['compound']>0.75, "V.Positive", df['Sentiment'])

df['TBSentiment'] = np.where(df['polarity'].between(-0.25,0.25), "Neutral", df['TBSentiment'])
df['TBSentiment'] = np.where(df['polarity'].between(-0.25,-0.75), "Negative", df['TBSentiment'])
df['TBSentiment'] = np.where(df['polarity']<-0.75, "V.Negative", df['TBSentiment'])
df['TBSentiment'] = np.where(df['polarity'].between(0.25,0.75), "Positive", df['TBSentiment'])
df['TBSentiment'] = np.where(df['polarity']>0.75 ,"V.Positive", df['TBSentiment'])


#dff=df.filter(items=['Comment', 'three'])



# Create a Pandas Excel writer using XlsxWriter as the engine.
writer = pd.ExcelWriter('finalsenti.xlsx', engine='xlsxwriter')

# Convert the dataframe to an XlsxWriter Excel object.
df.to_excel(writer, sheet_name='Sheet1')

# Close the Pandas Excel writer and output the Excel file.
writer.save()

###########################################
###########################################
"""
IBM FINAL -
import json

import Features, EntitiesOptions, KeywordsOptions, EmotionOptions,SentimentOptions
from watson_developer_cloud import NaturalLanguageUnderstandingV1
from watson_developer_cloud.natural_language_understanding_v1 \
import json
import pandas as pd
from watson_developer_cloud import NaturalLanguageUnderstandingV1
from watson_developer_cloud import NaturalLanguageClassifierV1
from watson_developer_cloud.natural_language_understanding_v1 \
import Features, EntitiesOptions, KeywordsOptions,EmotionOptions,SentimentOptions
from watson_developer_cloud.natural_language_understanding_v1 import Features, CategoriesOptions


natural_language_understanding = NaturalLanguageUnderstandingV1(
    version='2018-03-16',
    iam_apikey='7Mi6cxnueNv4eKCkBwuaDofzS5oVEUKsgZL0K8fqpxBr',
    url='https://gateway-fra.watsonplatform.net/natural-language-understanding/api'
)


df = pd.read_excel('temp.xlsx', header=None,dtype=str)
text=df.values.T.tolist()
text= [[k.lower()] for l in text for k in l]
dct = {}
djct={}

import spacy
len(text)

for index in range(len(text)):
    dj=text[index]
    djs=' '.join(dj)
    response = natural_language_understanding.analyze(
            language='en',
            text=djs,
            features=Features(emotion=EmotionOptions(),sentiment=SentimentOptions())).get_result()
    print(index)
    dct[index]= response["sentiment"].get("document").get("label")

#loop for emotion

for index in range(len(text)):
    dj=text[index]
    djs=' '.join(dj)
    response = natural_language_understanding.analyze(
            language='en',
            text=djs,
            features=Features(emotion=EmotionOptions())).get_result()
    print(index)
    djct[index]= response["emotion"].get("document").get("emotion")


djct
df = pd.DataFrame(data=djct)
df = (df.T)

df.to_excel('ibmoutputemotion.xlsx')

dct
df = pd.DataFrame(data=dct,index=[0])
df = (df.T)

df.to_excel('ibmoutputsentiment.xlsx')

###########################################
###########################################

def enrichNLU(text):
    utf8text = text.encode("utf-8")
    # In python3, need to decode to string
    utf8text = utf8text.decode('utf-8')

    try:
        result = nlu.analyze(text = utf8text, features = Features(sentiment=SentimentOptions(),keywords=KeywordsOptions()))
        sentiment = result['sentiment']['document']['score']
        sentiment_label = result['sentiment']['document']['label']
        keywords = list(result['keywords'])
    except WatsonException:
        result = None
        sentiment = 0.0
        sentiment_label = None
        keywords = None
    return sentiment, sentiment_label, keywords






Implementing paralleldots text analytics

import paralleldots
paralleldots.set_api_key( "1WQT8H7fjt4ewwxvVtn4hADPlDxNZbbp8IMBuvfD6pk" )
print( paralleldots.sentiment("the restaurant was so good that i will never visit it again"))
print( paralleldots.emotion("the restaurant was so good that i will never visit it again"))

"""