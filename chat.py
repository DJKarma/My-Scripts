import nltk
import pandas as pd
from progressbar import ProgressBar
from datetime import datetime
pbar = ProgressBar()

#READING THE CHAT FILE
chat= pd.read_excel(r'chat.xlsx',sheet_name='Transcripts')

###############################################################################
#DEFINING THE FUNCTION TO CALCULATE CHAT TIME PER CHAT ID
def calcChatDur(chat):
    lstChatids = chat["ID"].unique()
    chatdur = {}
    c = 0
    temp = 0
    for j in range(len(lstChatids)):
        for i in range(chat.shape[0]):
            if chat["ID"][i] == lstChatids[j]:
                fst = chat["time"][c]
                last = chat["time"][i]
                temp += 1
        c = temp
        #Calculate the difference between start and End times to keep note of chat duration.
        chatdur[str(lstChatids[j])] = datetime.strptime(last,'%I:%M:%S %p')  - datetime.strptime(fst,'%I:%M:%S %p')
    a = pd.DataFrame(data = chatdur,columns=chatdur.keys(),index=[0])

    return(a)

timedf=calcChatDur(chat) #CALLING THE FUNCTION AND SAVING THE RESULTS RETURNED IN DF
timedf=timedf.transpose() #TRANSPOSING THE DF, THIS DF CONTAINS TIME W.R.T CHAT ID
timedf=timedf[0].astype(str) #the date time is converted to str type so that is shows in EXCEL


###############################################################################
# CLEANING THE COMMENTS WITH BOT CHAT
chat['Comments'].dropna(inplace=True)
temp_list=["bot: Hi,"] #USING PATTERN AS BOT CHATS START WITH BOT:HI
chat["temp"]=chat['Comments'].apply(lambda x: any([k in x for k in temp_list]))
chat = chat[chat['temp'] == False]
chat=chat.drop(['temp'],axis=1)

#SELECTING ONLY THE END USER POSTS FOR FURTHER ANALYSIS
enduser = chat[chat["event"] == "End-user Post"]
enduserlist = enduser['Comments'].T.tolist() #CONVERTING TO LIST
endusermsg=" ".join(str(x) for x in pbar(enduserlist)) #CONVERTING TO STRING
chat['Comments'].dropna(inplace=True)
chat['Comments'] = chat['Comments'].apply(lambda x:str(x).lower()) #LOWERING CAPITALS FOR CONSISTENCY
text=chat['Comments'].T.tolist() #CONVERTING AGAIN TO LIST TO PERFORM FURTHER ANAYSIS

###############################################################################
#USING NLTK TO REMOVE STOPWORDS AND FIND TF-IDF , HERE TRI-GRAMS ARE USED BY SPECIFYING NGRAM RANGE
from nltk import sent_tokenize
from wordcloud import STOPWORDS
stop_words = set(STOPWORDS)
stop_words.update(('xxxxxxbot','xxxxxbot','please','because','already','anything','someone','should','us','sometime','certain','actually','taking','another','thanks','sometimes','people','nan','xxxxx','hi','name','contact','contacting','conversation','that','xxxxxxxx','will','that','hesitate','thank','today','ok','im','now','thats','want','yes'))

from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
tfidf_vectorizer = TfidfVectorizer(norm=None, ngram_range=(3,3),max_features=20,stop_words=stop_words)

endusermsg=[endusermsg]
vectorizer = TfidfVectorizer()
new_term_freq_matrix = tfidf_vectorizer.fit_transform(endusermsg)

t_list=[] #creating a blank list
t_list=tfidf_vectorizer.vocabulary_ #t_list contains tfidf with count and keywords

#EXTRACTING SENTENCES BASED ON TFIDF KEYWORDS
te_list = list(dict.fromkeys(t_list))   #removing duplicates from keywords if any, and making a list from t_list dictionary
te_list=list(filter(str.strip, te_list))#removing any empty spaces to avoid matching those.

enduserlist = enduser['Comments'].T.tolist()
endusermsg=" ".join(str(x) for x in enduserlist)
commentlist=[]
keywordlist=[]

i=0
index=0

for i in range(len(te_list)):
    temptext=te_list[i] #converting keywords to list
    temptext=str.split(temptext) #splitting each keyword

    for j in range(len(temptext)):
        for index in range(len(enduserlist)):
            if all(word in enduserlist[index] for word in temptext): #checking if keywords appear in the text
                commentlist.append(enduserlist[index]) #if they do comment is extracted
                keywordlist.append(temptext) #if they do keywords which detected it are extraceted as well


#making dataframe out of it
keywordmatchdf=pd.DataFrame(columns={"Comments"},data=commentlist)
listforvaluecounts=keywordmatchdf.Comments.value_counts()
keywordmatchdf["Keywords"]=keywordlist
keywordmatchdf=keywordmatchdf.drop_duplicates(subset='Comments', keep="first") #removing duplicates if any


###############################################################################
#Most common words with count
from collections import Counter
from nltk import ngrams
from nltk.tokenize import word_tokenize
dfngrams=pd.DataFrame()
enduser = chat[chat["event"] == "End-user Post"]
enduser['Comments']=enduser['Comments'].str.replace('[^a-zA-Z0-9 \n]', '') #removing special characters
enduserlist = enduser['Comments'].T.tolist() #CONVERTING TO LIST
endusermsg=" ".join(str(x) for x in enduserlist)
word_tokens = word_tokenize(endusermsg)

filtered_sentence = [w for w in word_tokens if not w in stop_words]
endusermsg=" ".join(str(x) for x in filtered_sentence)


x=1

for x in range(4):

    ngram_counts = Counter(ngrams(endusermsg.split(), x))
    ngram_counts.most_common(30)
    df = pd.DataFrame(ngram_counts.most_common(30)) #edit this number to print top n-grams
    dfngrams = df.append(dfngrams)

dfngrams=dfngrams.rename(columns={0:"N-Grams",1: "Frequency Count"})
dfngrams=dfngrams.drop_duplicates(subset='N-Grams', keep="first")
dfngrams=dfngrams.sort_values(by=['Frequency Count'],ascending=False)



#Sentiment Analysis
###############################################################################
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from textblob import TextBlob
import numpy as np
def SM(dataframe):

    dfsenti=dataframe
    dfsenti=dfsenti.drop_duplicates(keep="first")
    final=pd.DataFrame()
    dff=pd.DataFrame()

    analyser = SentimentIntensityAnalyzer() #instantiating sentiment analyser and calculating sentiment scores by using NLTK

    #loop to calculate sentiment scores by NLTK
    for index in range(dfsenti.shape[0]):
        score = analyser.polarity_scores(dfsenti.iloc[index]) #score is dict
        tempdf = pd.DataFrame([score], columns=score.keys()) #tempdf to convert score dict to df
        final= final.append(tempdf,ignore_index=True) #appending to final df

    #merging sentiment data with its comments
    dff=dfsenti.reset_index() #resetting index data before merging.
    dff=dff.merge(final,right_index=True,left_index=True)

    #Implementing textblob text analytics, can be made visible later.
    def sentiment_pol(text):
            try:
                return TextBlob(text).sentiment.polarity
            except:
                return None

    def sentiment_subj(text):
        try:
            return TextBlob(text).sentiment.subjectivity
        except:
            return None
    dff['TextBlobpolarity'] = dff["Comments"].apply(sentiment_pol)

    #categorizing scores to sentiments such as positive,negative and neutral.
    #len=dff.shape[0] #getting length of dataframe for counter value
    dff['Sentiment'] = np.nan #declaring a dataframe with empty Sentiment Column
    dff['TBSentiment']=np.nan
    dff=dff.drop_duplicates(subset='Comments', keep="last")
    dff['compound']=dff['compound']*5 #normalizing score to -5 to 5 for category into v.p+ and v.n-
    dff['TextBlobpolarity']=dff['TextBlobpolarity']*5 #normalizing score to -5 to 5 for category into v.p+ and v.n-
    #loop to categorize NLTK values to sentiment by score intervals
    #print("\n\nNLTK Processing")

    dff['Sentiment'] = np.where(dff['compound'].between(-0.5,0.5), "Neutral", dff['Sentiment'])
    dff['Sentiment'] = np.where(dff['compound'].between(-3.0,-0.5), "Negative", dff['Sentiment'])
    dff['Sentiment'] = np.where(dff['compound']<-3.0, "V.Negative", dff['Sentiment'])
    dff['Sentiment'] = np.where(dff['compound'].between(0.5,3.0), "Positive", dff['Sentiment'])
    dff['Sentiment'] = np.where(dff['compound']>3.0, "V.Positive", dff['Sentiment'])

    #dff['TextBlobsubj'] = dff[0].apply(sentiment_subj) # enable this if subjectivity is required in future.

    #print("\nTextBloB Processing")

    dff['TBSentiment'] = np.where(dff['TextBlobpolarity'].between(-0.5,0.5), "Neutral", dff['TBSentiment'])
    dff['TBSentiment'] = np.where(dff['TextBlobpolarity'].between(-3.0,-0.5), "Negative", dff['TBSentiment'])
    dff['TBSentiment'] = np.where(dff['TextBlobpolarity']<-3.0, "V.Negative", dff['TBSentiment'])
    dff['TBSentiment'] = np.where(dff['TextBlobpolarity'].between(0.5,3.0), "Positive", dff['TBSentiment'])
    dff['TBSentiment'] = np.where(dff['TextBlobpolarity']>3.0, "V.Positive", dff['TBSentiment'])


    return(dff) #to return dataframe back to function to further append and export

sentidf=SM(chat['Comments'])
sentidf=sentidf.drop(columns=['index'])
sentidf=sentidf.rename(columns={"Comments": "Comments", "compound": "Sentiment Score"}) #renaming some columns for user friendliness
final=sentidf[['Comments','Sentiment Score','Sentiment','TextBlobpolarity','TBSentiment']]

##############################################################################
#creating a final dataframe collating all the results
writer = pd.ExcelWriter('Chat Collated.xlsx', engine='xlsxwriter')

dfngrams.to_excel(writer, sheet_name='N-Grams' ,index=False)
keywordmatchdf.to_excel(writer, sheet_name='TF-IDF')
timedf.to_excel(writer, sheet_name='Chat Time')
final.to_excel(writer, sheet_name='Sentiment Analysis')
writer.save()



