from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import MoveTargetOutOfBoundsException
import time
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup as soup 
from selenium.webdriver.common.keys import Keys
from dotenv import load_dotenv
import os
import pickle



class Github():

	def __init__(self,driver):
		self.driver=driver
		self.driver.get("https://www.github.com/")

	def load_cookies(self,filename):
		cookies = pickle.load(open(filename, "rb"))
		for cookie in cookies:
		    driver.add_cookie(cookie)

	def login(self,username,password):

		self.driver.get("https://www.github.com/login")

		self.driver.find_element_by_id("login_field").send_keys(username)

		self.driver.find_element_by_id("password").send_keys(password)

		self.driver.find_element_by_class_name("btn.btn-primary.btn-block").click()

		time.sleep(2)

	def get_repository(self,username):
		self.driver.get(f"https://www.github.com/{username}")

		try:

			reps=WebDriverWait(self.driver,5).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "span.repo")))
		except:
			self.repo='repository'
			return

		for repo in reps:
			if repo.text.endswith('...'):
				continue
			else:
				self.repo=repo.text
				break
		else:
			self.repo='repository'
		



	def get_following(self,username):

		l=[]

		try:

			self.driver.get(f"https://www.github.com/{username}?tab=following")

			#followings=WebDriverWait(self.driver,5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.mb-3")))
			followings=WebDriverWait(self.driver,5).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "span.text-bold.color-text-primary")))[1].text
			if 'k' in followings:
				followings=int(followings[:-1])*1000
			else:
				followings=int(followings)

			print (f"followings: {followings}")


			if followings==0:
				return []

			


			

			usernames=WebDriverWait(self.driver,5).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "span.Link--secondary.pl-1")))
			for user in usernames:
				l.append(user.text)

			if followings>50:
				upto=(followings//50)+1
				upto=2
				for page_num in range(2,upto+1):
					self.driver.get(f"https://www.github.com/{username}?page={page_num}&tab=following")
					usernames=WebDriverWait(self.driver,5).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "span.Link--secondary.pl-1")))
					for user in usernames:
						l.append(user.text)
					time.sleep(2)
		except:
			return (l)
					





		return (l)



	def get_followers(self,username):

		l=[]

		try:


			self.driver.get(f"https://www.github.com/{username}?tab=followers")

			#followers=WebDriverWait(self.driver,5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.mb-3")))
			followers=WebDriverWait(self.driver,5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "span.text-bold.color-text-primary"))).text
			if 'k' in followers:
				followers=int(followers[:-1])*1000
			else:
				followers=int(followers)

			print (f"followers: {followers}")

			if followers==0:
				return []
			

			

			usernames=WebDriverWait(self.driver,5).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "span.Link--secondary.pl-1")))
			for user in usernames:
				l.append(user.text)

			if followers>50:
				#upto=(followers//50)+1
				upto=2

				for page_num in range(2,upto+1):
					self.driver.get(f"https://www.github.com/{username}?page={page_num}&tab=followers")
					usernames=WebDriverWait(self.driver,5).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "span.Link--secondary.pl-1")))
					for user in usernames:
						l.append(user.text)
					time.sleep(3)
		except:
			return (l)






		return (l)


	def check_login_status(self):
		try:
			WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.XPATH, "//*[text()='Sign in to view email']")))
			return "logged_out"
		except:
			return "logged_in"



	def get_details(self,username):

		try:
			self.driver.get(f"https://www.github.com/{username}")
		except:
			self.Email=np.nan
			self.Name=np.nan
			
		
		try:
			self.Email=WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "a.u-email.Link--primary "))).text
		except:
			self.Email=np.nan

		

		try:
			self.Name=WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "span.p-name.vcard-fullname.d-block.overflow-hidden"))).text
		except:
			self.Name=np.nan
		
		
		
			

	def get_topic_usernames(self,url):
		self.driver.get(url)
		flag=True
		while flag:
			self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
			time.sleep(5)
			try:
				WebDriverWait(self.driver,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.ajax-pagination-btn.btn.btn-outline.color-border-tertiary.f6.mt-0.width-full"))).click()
			except:
				flag=False
    
		elements=WebDriverWait(self.driver,5).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "article.border.rounded.color-shadow-small.color-bg-secondary.my-4")))
		print (len(elements))
		l=[]
		for element in elements:
			user=WebDriverWait(element,5).until(EC.presence_of_element_located((By.TAG_NAME, "a"))).text
			l.append(user)
			print (user)
		return l


if __name__=='__main__':
	options = Options()
	options.headless = False
	driver= webdriver.Firefox(options=options)
	git_obj=Github(driver)
	git_obj.login("Manikaran20","@Manikaran20")


	df=pd.read_csv("github_testers_dataset.csv")

	r=open("github_testers.txt",'r')
	l=[i.strip() for i in r]
	r.close()

	#w=open("github_testers.txt",'a')
	count=3055

	for username in l[count:]:
		git_obj.get_details(username)
		print (git_obj.Name,git_obj.Email)
		df=pd.concat([df,pd.DataFrame({"Name":[git_obj.Name],"Github":[username],"Email":[git_obj.Email]})],axis=0)
		df.to_csv("github_testers_dataset.csv",index=False)
		count+=1
		print (count)




		'''
	for i in df['Github']:
		for j in git_obj.get_following(i):
			w.write(j+'\n')
		w.close()
		w=open("github_testers.txt",'a')
		for j in git_obj.get_followers(i):
			w.write(j+'\n')
		w.close()
		w=open("github_testers.txt",'a')
		'''


	'''
	w=open("test_pages.txt",'w')

	for i in l:
		print (i)
		try:
			git_obj.get_details(i)
			print (git_obj.Name,git_obj.Email)
			df=pd.concat([df,pd.DataFrame({"Name":[git_obj.Name],"Github":[i],"Email":[git_obj.Email]})],axis=0)
			df.to_csv("github_testers_dataset.csv",index=False)
		except:
			w.write(i+'\n')
			w.close()
			w=open("test_pages.txt",'a')
	'''
	



