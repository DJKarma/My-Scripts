
# importing the necessery modules
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import csv
import re
import nltk
from collections import Counter
from nltk import ngrams
import pandas as pd

# file object is created
file_ob = open(r"temp.csv")

# reader object is created
reader_ob = csv.reader(file_ob)

# contents of reader object is stored .
# data is stored in list of list format.
reader_contents = list(reader_ob)

# empty string is declare
text = ""
stopwords = set(STOPWORDS)
stopwords.update(('now','wont','im','got','going','said','go','come','hi','well','never','dont','better','will','thank','today','need','thanks','regards','please','and','I','A','And','So','arnt','This','When','It','many','Many','so','cant','Yes','yes','No','no','These','these'))


# iterating through list of rows
for row in reader_contents :

    # iterating through words in the row
    for word in row :

        # concatenate the words
        text = text + " " + word


#splitting all text data to words and storing it in unique_string
words = text.split()
import string
lowerText = text.lower() # lowercase
# this line will remove all punctuations
cleanText = lowerText.translate(string.punctuation)
words = cleanText.split()
#words=words.replace('[^ a-zA-Z0-9]', '')

# remove Python , Matplotlib , Geeks Words from WordCloud .
wordcloud = WordCloud(normalize_plurals=True,collocations=True,width=480, height=480,
                      stopwords=stopwords).generate(text)
wordcloud.words_


type(words)
"""
#method by frequency of words
from collections import Counter
word_could_dict=Counter(words)
wordcloud = WordCloud(width = 1000, height = 500,stopwords=stopwords).generate_from_frequencies(word_could_dict)
"""

# plot the WordCloud image
plt.figure()
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.margins(x=0, y=0)
plt.show()

#to print freq of words present in cloud (wordcloud.words_)

sorted(wordcloud.words_.items(), key=lambda pair: pair[1], reverse=True)[:20]

#Finding the top words with frequency count , edit it min and max length of words below this line
match_pattern = re.findall(r'\b[a-z]{7,15}\b',text) #edit here
frequency = {}
for word in match_pattern:
    count = frequency.get(word,0)
    frequency[word] = count + 1

frequency_list = frequency.keys()
fdist = nltk.FreqDist(match_pattern) # creates a frequency distribution  from a list
most_common = fdist.max()    # returns a single element
top = fdist.most_common(60)# returns a list
print(top) #prints the top 10 words
type(top)
df = pd.DataFrame(top)
print(df) #print this

#this is to find n-grams
bigtxt = open('temp.csv').read()
bigtxt=bigtxt.lower()

#removing stopwords from here as well
bigtxt= bigtxt.split()
resultwords  = [word for word in bigtxt if word.lower() not in stopwords]
bigtxt = ' '.join(resultwords)


ngram_counts = Counter(ngrams(bigtxt.split(), 4))
ngram_counts.most_common(20)
df = pd.DataFrame(ngram_counts.most_common(40))
print(df) #print this
