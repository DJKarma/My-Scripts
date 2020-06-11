import pandas as pd
from requests import Session
session = Session()

session.head('https://thevirustracker.com/free-api?countryTimeline=IN')

response = session.get(
    url='https://thevirustracker.com/free-api?countryTimeline=IN',
    data={
        'N': '4294966750',
        'form-trigger': 'moreId',
        'moreId': '156#327',
        'pageType': 'EventClass'
    },json=True,
    headers={
        'Referer': 'https://thevirustracker.com/free-api?countryTimeline=IN'
    }
)

ll=response.json()
timeline=ll['timelineitems']
timeline=timeline[0]
dj=pd.DataFrame.from_dict(timeline)
dj=dj.T

import ft2font
