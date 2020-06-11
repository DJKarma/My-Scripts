from flask import Flask, request, render_template, session, redirect
import pandas as pd


from newsapi.newsapi_client import NewsApiClient

app = Flask(__name__)

@app.route('/', methods=("POST", "GET"))
def html_table():
    df=pd.DataFrame()
    dj=pd.DataFrame()
    supplierdf=pd.read_excel('suppp.xlsx',headers=True)
    supplierdf['name'] = supplierdf['name'].str.strip()
    supplierlist=supplierdf['name'].values.tolist()
    supplierlist= [k.lower() for k in supplierlist]

    newsapi = NewsApiClient(api_key='b320e2b793644396bdbeded93ff9d702')

    for i in range(len(supplierlist)):
        all_articles = newsapi.get_everything(q=supplierlist[i],language='en')
        for article in all_articles['articles']:
            df=df.from_dict(article)
            df['Supplier Name']=supplierlist[i]
            dj=dj.append(df)

    newsdf=dj.drop_duplicates(subset='title', keep="first")
    newsdf=newsdf.reset_index()
    newsdf=newsdf.drop(columns=['index'])
    return render_template('simple.html',  tables=[newsdf.to_html(classes='data')], titles=newsdf.columns.values)

if __name__ == '__main__':
    app.run()
