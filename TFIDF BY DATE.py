import nltk
import numpy as np
import datetime
import pandas as pd
from progressbar import ProgressBar
from datetime import datetime
from datetime import timedelta
from dateutil.relativedelta import relativedelta
from wordcloud import STOPWORDS
import warnings # to ignore warnings from displaying
warnings.filterwarnings("ignore")

pbar = ProgressBar()
chat= pd.read_excel(r'temp.xlsx')
a=0
tempdftoappend=pd.DataFrame()
datedf=pd.DataFrame()
tfidfkadf=pd.DataFrame()

tfidfkadf['Datee']=0



for chat in chat.groupby('bu'):
    df=chat[1].Comments #this is imp.
    tempdftoappend=chat[1].bu
    a=a+1
    print(a)

    #READING THE CHAT FILE

    df=df.str.replace('[^ a-zA-Z0-9]', '')
    df= df.apply(lambda x:str(x).lower()) #LOWERING CAPITALS FOR CONSISTENCY
    textlist=df.T.tolist() #CONVERTING AGAIN TO LIST TO PERFORM FURTHER ANAYSIS
    text = " ".join(str(x) for x in textlist)

    stop_words = set(STOPWORDS)
    stop_words.update(('order','argos','delivery','please','because','already','anything','someone','should','us','sometime','certain','actually','taking','another','thanks','sometimes','people','nan','xxxxx','hi','name','contact','contacting','conversation','that','xxxxxxxx','will','that','hesitate','thank','today','ok','im','now','thats','want','yes'))

    ###############################################################################
    #USING NLTK TO REMOVE STOPWORDS AND FIND TF-IDF , HERE TRI-GRAMS ARE USED BY SPECIFYING NGRAM RANGE
    def tfidf(templist):
        from nltk import sent_tokenize
        from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
        tfidf_vectorizer = TfidfVectorizer(norm=None, ngram_range=(3,3),max_features=20,stop_words=stop_words)

        #templist=[templist]
        vectorizer = TfidfVectorizer()
        new_term_freq_matrix = tfidf_vectorizer.fit_transform(templist)

        t_list=[] #creating a blank list
        t_list=tfidf_vectorizer.vocabulary_ #t_list contains tfidf with count and keywords

        #EXTRACTING SENTENCES BASED ON TFIDF KEYWORDS
        te_list = list(dict.fromkeys(t_list))   #removing duplicates from keywords if any, and making a list from t_list dictionary
        te_list=list(filter(str.strip, te_list))#removing any empty spaces to avoid matching those.


        commentlist=[]
        keywordlist=[]
        i=0
        index=0

        for i in range(len(te_list)):
            temptext=te_list[i] #converting keywords to list
            temptext=str.split(temptext) #splitting each keyword

            for j in range(len(temptext)):
                for index in range(len(templist)):
                    if all(word in templist[index] for word in temptext): #checking if keywords appear in the text
                        commentlist.append(templist[index]) #if they do comment is extracted
                        keywordlist.append(temptext) #if they do keywords which detected it are extraceted as well


                        #making dataframe out of it
        keywordmatchdf=pd.DataFrame(columns={"Comments"},data=commentlist)
        listforvaluecounts=keywordmatchdf.Comments.value_counts()
        keywordmatchdf["Keywords"]=keywordlist
        keywordmatchdf=keywordmatchdf.drop_duplicates(subset='Comments', keep="first") #removing duplicates if any

        return(keywordmatchdf)


    alltfidf=tfidf(textlist)
    tfidfkadf= tfidfkadf.append(alltfidf,ignore_index=True)




    def commonwords(tempostring):
        from collections import Counter
        from nltk import ngrams
        from nltk.tokenize import word_tokenize
        dfngrams=pd.DataFrame()

        word_tokens = word_tokenize(tempostring)

        filtered_sentence = [w for w in word_tokens if not w in stop_words]
        tempostring=" ".join(str(x) for x in filtered_sentence)


        x=1

        for x in range(4):

            ngram_counts = Counter(ngrams(tempostring.split(), x))
            ngram_counts.most_common(5)
            df = pd.DataFrame(ngram_counts.most_common(5)) #edit this number to print top n-grams
            dfngrams = df.append(dfngrams)

        dfngrams=dfngrams.rename(columns={0:"N-Grams",1: "Frequency Count"})
        dfngrams=dfngrams.drop_duplicates(subset='N-Grams', keep="first")
        dfngrams=dfngrams.sort_values(by=['Frequency Count'],ascending=False)

        return(dfngrams)


    allcommonwords=commonwords(text)
    tfidfkadf= tfidfkadf.append(allcommonwords,ignore_index=True)
    datedf=chat[1].bu
    datedf=datedf.to_frame()
    tempv=datedf.values.astype(str)
    tempv=tempv[1]

    print(tempv)
    tfidfkadf['Datee'] =tfidfkadf['Datee'].astype(str)

    tfidfkadf['Datee'] = np.where(tfidfkadf['Datee']=='nan', tempv,tfidfkadf['Datee'] )



writer = pd.ExcelWriter('bu.xlsx', engine='xlsxwriter')

tfidfkadf.to_excel(writer, sheet_name='ALL TFIDF' ,index=False)
#allcommonwords.to_excel(writer, sheet_name='ALL Common Words')

writer.save()

