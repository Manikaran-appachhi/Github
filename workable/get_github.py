import urllib.request
from bs4 import BeautifulSoup as soup 
from lxml import html
import requests
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import MoveTargetOutOfBoundsException
from get_github_sel import Github
import time
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup as soup 
from selenium.webdriver.common.keys import Keys
from dotenv import load_dotenv
import os
import pickle
from collections import OrderedDict
import re
from dotenv import load_dotenv
import os
from snov_apis import *
import random
import json




















load_dotenv()



def remove_duplicate(filename):
	b = list(OrderedDict.fromkeys([i.strip() for i in open(filename, 'r')]))
	w=open(filename, 'w')

	for i in b:
		w.write(i+'\n')
	w.close()



def verify_email(email):
	
	url = f"https://api.usebouncer.com/v1/email/verify?email={email}&timeout=10"

	payload={}
	headers = {
	  'x-api-key': os.getenv("BOUNCER_API_KEY")
	}

	response = requests.request("GET", url, headers=headers, data=payload)

	return(json.loads(response.text))






options = Options()
options.headless = True

driver= webdriver.Firefox(options=options,executable_path="/usr/local/bin/geckodriver")
git_obj=Github(driver)
git_obj.login(os.getenv("GIT_USR"),os.getenv("GIT_PWD"))



flag=True

df=pd.read_csv("new_testers_dataset.csv")
new_df=pd.DataFrame(columns=["Name","Github","Email"])

while flag:
	remove_duplicate('new_testers.txt')
	start_user=list(df['Github'])[-1]



	testers=open('new_testers.txt', 'r')
	there=[i.strip() for i in testers]
	testers.close()

	testers=open('new_testers.txt', 'a')


	to_start=there.index(start_user)+1

	print (len(there), len(set(there)))

	for num,tester in enumerate(there[to_start:]):

		git_obj.get_details(tester)
		df=pd.concat([df,pd.DataFrame({"Name":[git_obj.Name], "Github":[tester], "Email":[git_obj.Email]})],axis=0)
		df.drop_duplicates(subset='Email', keep='first',inplace=True)
		df.to_csv("new_testers_dataset.csv", index=False)


		if (type(git_obj.Email)!=float):

			if git_obj.Email == list(df['Email'])[-1]:

			
			#t=time.localtime(time.time())
			#print (f"{t.tm_mday}-{t.tm_mon}-{t.tm_year}")

				if verify_email(git_obj.Email)['status'] in ['deliverable', 'risky']:
					print('deliverable ya risky')

					if num % 2==0:
						listId=random.choice(['6123215','6283504','6283507','6283509'])
						#new_df=pd.concat([new_df,pd.DataFrame({"Name":[git_obj.Name], "Github":[tester], "Email":[git_obj.Email]})],axis=0)		
					else:
						listId='6291305'

					add_prospect_to_list(email=git_obj.Email,firstName=git_obj.Name[0], fullName=git_obj.Name,listId=listId)

			




		for user in git_obj.get_followers(tester):
			testers.write(user+'\n')
		testers.close()
		testers=open('new_testers.txt', 'a')

		#time.sleep(5)

		for user in git_obj.get_following(tester):
			testers.write(user+'\n')
		testers.close()
		testers=open('new_testers.txt', 'a')

		print (f"tester: {tester}")

		#time.sleep(4)

	to_start=tester
	print (f"to_start: {to_start}")



































'''
			if df.shape[0]%2000==0:
				start=df.shape[0]-2000
				end=start+2000
				t=time.localtime(time.time())
				df[start:end].to_csv(f"{t.tm_mday}-{t.tm_mon}-{t.tm_year}.csv", index=False)
'''















































#Github Login

'''
driver.get("https://www.github.com/login")

driver.find_element_by_id("login_field").send_keys("manikaran20")

driver.find_element_by_id("password").send_keys("@manikaran20")

driver.find_element_by_class_name("btn.btn-primary.btn-block").click()
'''

#Get users from testing repos
'''
testers=[]


for i in range(2,101):
	url=f"https://github.com/search?p={i}&q=testing&type=Repositories"
	try:
		with urllib.request.urlopen(url) as my_url:
		    page_html = my_url.read()
		    page_soup = soup(page_html, "html.parser")

		repos=page_soup.findAll('a', {"class":"v-align-middle"})
		for repo in repos:
			try:
				testers.append(soup(urllib.request.urlopen(f'https://www.github.com{repo["href"]}').read(),"html.parser").find('a',{"class":"commit-author user-mention"}).text)
			except:
				pass
			time.sleep(1.4)
	except:
		continue
	w=open('new_testers.txt', 'a')

	for tester in testers:
		w.write(tester+'\n')
	w.close()
'''
