# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from facebook_scraper import get_posts
import pandas as pd

dj=pd.Series()

for post in get_posts('iamforloveofwater', pages=10,extra_info=True):
    temp=pd.Series(post)
    v = temp.to_frame().T    
    dj=dj.append(v,ignore_index=False)
   
dj.to_excel("Fbextracts.xlsx")
