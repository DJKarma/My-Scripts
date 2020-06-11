import pandas as pd
import numpy as np

import re

df=pd.read_excel('C:/Users/P10472266/OneDrive - Capita/DJ Other Projects/kURT/Project Plans.xlsx')
df['Operator Notes']
final=pd.DataFrame()
df=df.fillna(np.nan)
finalchat=[]

for i in range(len(df)):
    if df['Operator Notes'][i] is not np.nan:
        print(i)
        customerchats=re.findall(r'\bCustomer :.*\b',df['Operator Notes'][i])
        agentchats=re.findall(r'\bMadhura :.*\b',df['Operator Notes'][i])
        customerchats.extend(agentchats)
        djf=pd.DataFrame(customerchats)
        djf['id']=df['tempUID'][i]
        final=final.append(djf)
        customerchat=[]
        agentchats=[]







final.to_excel('C:/Users/P10472266/OneDrive - Capita/DJ Other Projects/kURT/final.xlsx')

len(df)





bla=sent_tokenize(djf[0][0])





customerchats=re.findall(r'\bCustomer :.*\b',df['Operator Notes'][0])
agentchats=re.findall(r'\bMichelle :.*\b',df['Operator Notes'][0])


















import re
alphabets= "([A-Za-z])"
prefixes = "(Mr|St|Mrs|Ms|Dr)[.]"
suffixes = "(Inc|Ltd|Jr|Sr|Co)"
starters = "(Mr|Mrs|Ms|Dr|He\s|She\s|It\s|They\s|Their\s|Our\s|We\s|But\s|However\s|That\s|This\s|Wherever)"
acronyms = "([A-Z][.][A-Z][.](?:[A-Z][.])?)"
websites = "[.](com|net|org|io|gov)"

def split_into_sentences(text):
    text = " " + text + "  "
    text = text.replace("\n"," ")
    text = re.sub(prefixes,"\\1<prd>",text)
    text = re.sub(websites,"<prd>\\1",text)
    if "Ph.D" in text: text = text.replace("Ph.D.","Ph<prd>D<prd>")
    text = re.sub("\s" + alphabets + "[.] "," \\1<prd> ",text)
    text = re.sub(acronyms+" "+starters,"\\1<stop> \\2",text)
    text = re.sub(alphabets + "[.]" + alphabets + "[.]" + alphabets + "[.]","\\1<prd>\\2<prd>\\3<prd>",text)
    text = re.sub(alphabets + "[.]" + alphabets + "[.]","\\1<prd>\\2<prd>",text)
    text = re.sub(" "+suffixes+"[.] "+starters," \\1<stop> \\2",text)
    text = re.sub(" "+suffixes+"[.]"," \\1<prd>",text)
    text = re.sub(" " + alphabets + "[.]"," \\1<prd>",text)
    if "”" in text: text = text.replace(".”","”.")
    if "\"" in text: text = text.replace(".\"","\".")
    if "!" in text: text = text.replace("!\"","\"!")
    if "?" in text: text = text.replace("?\"","\"?")
    text = text.replace(".",".<stop>")
    text = text.replace("?","?<stop>")
    text = text.replace("!","!<stop>")
    text = text.replace("<prd>",".")
    sentences = text.split("<stop>")
    sentences = sentences[:-1]
    sentences = [s.strip() for s in sentences]
    return sentences


