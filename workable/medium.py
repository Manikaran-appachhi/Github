import requests
import os
from dotenv import load_dotenv
import json
import time
from collections import OrderedDict
import pandas as pd
import numpy as np
load_dotenv()



token = os.getenv("Medium_Manikaran_Access_Token") 
userId=os.getenv("Medium_Manikaran_UserId")


class Medium():

    def __init__(self,token,user_id):

        self.url = "https://api.medium.com/v1"

        self.header = {
            "Accept":   "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Encoding"   :"gzip, deflate, br",
            "Accept-Language"   :"en-US,en;q=0.5",
            "Connection"    :"keep-alive",
            "Host"  :"api.medium.com",
            "TE"    :"Trailers",
            "Authorization": f"Bearer {token}",
            "Upgrade-Insecure-Requests":    "1",
            "User-Agent":   "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0"
        }
        self.userId=user_id

    def post_article(self,Title,Content):

        data = {
        "title": Title ,
        "contentFormat": "html",
        "content": Content, #"<p>this content 1.</p><p> This is content 2.</p>",
        "tags": ["bug tracker", "bug tracking", "software testing", 'testing', "issue tracker", "issue tracking", "defect management", "project management"],
        "publishStatus": "public" ,  # "public" will publish to gibubfor putting draft use value "draft"
            }
        
        response = requests.post(
            url= f"{self.url}/users/{self.userId}/posts",  #https://api.medium.com/me/users/{userId}/posts
            headers=self.header,
            data=data
        )
        print(response.text)
        response_json = response.json()
        self.published_url = response_json["data"]["url"]



########################
# This is title
########################



if __name__ == "__main__":

    medium_obj=Medium(token,userId)

    with open ("tt_rephrased.json", 'r') as read_file:
        tt=json.load(read_file)

    published=pd.read_csv("published.csv")


    last_title=list(pd.read_csv("published.csv")['Title'])[-1]
    print(last_title)

    r=open("Titles.txt",'r')
    l=[i.strip() for i in r]
    r.close()

    subs=l.index(last_title)
    subs+=1

    titles=list(tt.keys())[subs:subs+12]
    values=list(tt.values())[subs:subs+12]
    print (len(titles),len(values))

    for title,content in zip(titles,values):
        medium_obj.post_article(title,content)
       
       
        published=pd.concat([published,pd.DataFrame({"Title":[title.strip()],"Published_Url":[medium_obj.published_url]})],axis=0)
        published.to_csv("published.csv",index=False)


        time.sleep(6)