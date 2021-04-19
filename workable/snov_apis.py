import requests
import json
from dotenv import load_dotenv
import os
import numpy as np

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






def add_prospect_to_list(email,fullName,firstName,listId):
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
  add_prospect_to_list(email="mani.da1739@gmail.com",firstName='Manikaran', lastName='Singh', fullName='Manikaran Singh',listId=6283504)
