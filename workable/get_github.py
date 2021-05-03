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
import subprocess
import pickle
from collections import OrderedDict
import re
from dotenv import load_dotenv
import os
from snov_apis import *
import random
import json


load_dotenv() #loading enviornment variables


def remove_duplicate(filename): #func that takes a file name and removes duplicates while keeping the order
	b = list(OrderedDict.fromkeys([i.strip() for i in open(filename, 'r')]))
	w=open(filename, 'w')

	for i in b:
		w.write(i+'\n')
	w.close()



def verify_email(email): #takes email as input use bouncer api to verify status
	
	url = f"https://api.usebouncer.com/v1/email/verify?email={email}&timeout=10"

	payload={}
	headers = {
	  'x-api-key': os.getenv("BOUNCER_API_KEY")
	}

	response = requests.request("GET", url, headers=headers, data=payload)

	return(json.loads(response.text))





print ("execution started")
options = Options()
print ("options called")
options.headless = True
options.add_argument("user-agent=Mozilla/5.0 (Windows Phone 10.0; Android 4.2.1; Microsoft; Lumia 640 XL LTE) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Mobile Safari/537.36 Edge/12.10166")
print ("user-agents added")
driver= webdriver.Firefox(options=options,executable_path="/usr/local/bin/geckodriver")
print("driver started")

git_obj=Github(driver)

try:

	print ("github class object created")

	''' Can load previously generated sessions's cookies
	cookies = pickle.load(open("Github_cookies.pkl", "rb"))
	for cookie in cookies:
	   driver.add_cookie(cookie)
	 '''
	git_obj.login(os.getenv("GIT_USR"),os.getenv("GIT_PWD"))

	#time.sleep(5)
	#pickle.dump( driver.get_cookies() , open("Github_cookies.pkl","wb"))

	print ("logged in to Github")



	df=pd.read_csv("new_testers_dataset.csv")
	new_df=pd.DataFrame(columns=["Name","Github","Email"])
	while flag:
		remove_duplicate('new_testers.txt')
		start_user=list(df['Github'])[-1]

		print ("removed duplicates from new_testers.txt")

		testers=open('new_testers.txt', 'r')
		there=[i.strip() for i in testers]
		testers.close()

		testers=open('new_testers.txt', 'a')


		to_start=there.index(start_user)+1
		print (f"start index {to_start}")

		print (f"number testers to get in this loop {len(there)}")

		nan_count=0

		for num,tester in enumerate(there[to_start:]):
			print (f"getting tester {tester}")
			time.sleep(3)

			
			if git_obj.check_login_status()=='logged_out':
				print ("we got logged out")
				git_obj.login(os.getenv("GIT_USR"),os.getenv("GIT_PWD"))
				print ("now logged it")	
				
			else:
				print ("logged in probably")
				pass

			git_obj.get_details(tester)
			print ("got details")

			if type(git_obj.Name)==float:
				if nan_count==0:
					flag=True
				if nan_count<5:
					if flag==True:
						print (f"name is nan {nan_count+1}")
						nan_count+=1
						continue
					
				else:
					git_obj.login(os.getenv("GIT_USR"),os.getenv("GIT_PWD"))
					print ("loged in")
					git_obj.get_details(tester)
					print ("got details again")
					nan_count=0
					flag=False
			else:
				flag=False
				nan_count=0





			df=pd.concat([df,pd.DataFrame({"Name":[git_obj.Name], "Github":[tester], "Email":[git_obj.Email]})],axis=0)
			print ("added to dataset")
			df.drop_duplicates(subset='Email', keep='first',inplace=True)
			df.to_csv("new_testers_dataset.csv", index=False)
			print ("saved dataset")

			if (type(git_obj.Email)!=float):
				print ("email is present")

				if git_obj.Email == list(df['Email'])[-1]:


					print (git_obj.Email)
					
					if verify_email(git_obj.Email)['status'] in ['deliverable', 'risky']:
						print(' either email is deliverable or risky')

						if num % 2==0:
							listId=random.choice(['6123215','6283504','6283507','6283509'])
							print ("adding to campaigns")
						else:
							listId='6291305'
							print ("adding to Pradeep's list")
						try:
							add_prospect_to_list(email=git_obj.Email,firstName=git_obj.Name.split(' ')[0], fullName=git_obj.Name,listId=listId)
							print ('added')
						except:
							print ('error, could not add')

					else:
						print ("email is undeliverable")

				else:
					print ("email already exists in dataset")

			else:
				print ("email isn't present")	


			time.sleep(4)

			for user in git_obj.get_followers(tester):
				testers.write(user+'\n')
			testers.close()
			testers=open('new_testers.txt', 'a')

			time.sleep(5)

			for user in git_obj.get_following(tester):
				testers.write(user+'\n')
			testers.close()
			testers=open('new_testers.txt', 'a')

			print ("followers and followings added to the testers.txt")


			time.sleep(4)

		print ("one read of tester.txt executed")


except:
	flag= False
	driver.close()
	driver.quit()
	l=[]
	for i in (subprocess.check_output('ps -ef | grep geckodriver',shell=True).decode('utf-8')).split('\n')[:-2]:# stdout=subprocess.PIPE).stdout.decode('utf-8'))
		l.append (i.split()[1])
	for i in l:
		print (f"killing {i}")
		os.system(f"kill -9 {int(i)}")
		os.system("nohup python3 -u get_github.py > github.logs 2>&1 &")




























#t=time.localtime(time.time())
					#print (f"{t.tm_mday}-{t.tm_mon}-{t.tm_year}")




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
