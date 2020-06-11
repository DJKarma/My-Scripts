from newsapi import NewsApiClient
import pandas as pd

df=pd.DataFrame()
dj=pd.DataFrame()
supplierdf=pd.read_excel('suppp.xlsx',headers=True)
supplierdf['name'] = supplierdf['name'].str.strip()
supplierlist=supplierdf['name'].values.tolist()
supplierlist= [k.lower() for k in supplierlist]



newsapi = NewsApiClient(api_key='0267866eef6b46f49fe5acae98951d1f')

for i in range(len(supplierlist)):
    all_articles = newsapi.get_everything(q=supplierlist[i],language='en')
    for article in all_articles['articles']:
        df=df.from_dict(article)
        df['Supplier Name']=supplierlist[i]
        dj=dj.append(df)

newsdf=dj.drop_duplicates(subset='title', keep="first")
newsdf=newsdf.reset_index()
newsdf=newsdf.drop(columns=['index'])

newsdf.to_excel("NewsScraped2.xlsx")

