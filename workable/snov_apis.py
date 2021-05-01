import requests
import json
from dotenv import load_dotenv
import os
import numpy as np
import pandas as pd
import time

load_dotenv()


def get_access_token():
  params = {
        'grant_type':'client_credentials',
        'client_id': os.getenv("Snov_API_UID"),
        'client_secret': os.getenv("Snov_API_SECRET")
      }

  res = requests.post('https://api.snov.io/v1/oauth/access_token', data=params)
  resText = res.text.encode('ascii','ignore')

  return json.loads(resText)['access_token']






def add_prospect_to_list(listId=6418691,email=np.nan,fullName=np.nan,firstName=np.nan):
  token = get_access_token()
  params = {'access_token':token,
            'email':email,
            'fullName': fullName,
            'firstName':firstName,
            #'lastName':lastName,
            'updateContact':1,
            'listId':listId
  }

  res = requests.post('https://api.snov.io/v1/add-prospect-to-list', data=params)

  return json.loads(res.text)




if __name__=='__main__':
  df=pd.read_csv("new_testers_dataset.csv")
  for i in range(df.shape[0]):
    add_prospect_to_list(email=df.loc[i,'Email'], fullName=df.loc[i,'Name'],listId=6418691)
    time.sleep(5)
