import requests
import os
from dotenv import load_dotenv
import json
import time
from collections import OrderedDict
import pandas as pd
import numpy as np
load_dotenv()


########################
# keep your tokens here
########################
token = os.getenv("Medium_Bugasura_Access_Token") 
userId=os.getenv("Medium_Bugasura_UserId")
########################

# End point for yout requests
url = "https://api.medium.com/v1"

# header requred
header = {
    "Accept":	"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Encoding"	:"gzip, deflate, br",
    "Accept-Language"	:"en-US,en;q=0.5",
    "Connection"	:"keep-alive",
    "Host"	:"api.medium.com",
    "TE"	:"Trailers",
    "Authorization": f"Bearer {token}",
    "Upgrade-Insecure-Requests":	"1",
    "User-Agent":	"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0"
}

########################
# This is title
########################



if __name__ == "__main__":


    with open ("tt_rephrased.json", 'r') as read_file:
        tt=json.load(read_file)

    published=pd.read_csv("published.csv")

    last_title=list(pd.read_csv("published.csv")['Title'])[-1]
    print(last_title)

    r=open("Titles.txt",'r')
    l=[i.strip() for i in r]
    r.close()

    w=open("Titles.txt",'r')
    subs=l.index(last_title)
    subs+=1

    titles=list(tt.keys())[subs:subs+12]
    values=list(tt.values())[subs:subs+12]
    print (len(titles),len(values))

    for title,content in zip(titles,values):
        print (1)

        print (title)
        data = {
        "title": title ,
        "contentFormat": "html",
        "content": content, #"<p>this content 1.</p><p> This is content 2.</p>",
        "tags": ["bug tracker", "bug tracking", "software testing", 'testing', "issue tracker", "issue tracking", "defect management", "project management"],
        "publishStatus": "public"   # "public" will publish to gibubfor putting draft use value "draft"
            }
        
        response = requests.post(
            url= f"{url}/users/{userId}/posts",  #https://api.medium.com/me/users/{userId}/posts
            headers=header,
            data=data
        )
        print (2)
        print(response.text)
        print (3)
        response_json = response.json()
        print (4)
        url = response_json["data"]["url"]
        print(5)
        print(url)       # this url where you can acess your url
        published=pd.concat([published,pd.DataFrame({"Title":[title.strip()],"Published_Url":[url]})],axis=0)
        published.to_csv("published.csv",index=False)


        time.sleep(60)