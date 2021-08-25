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
import re
import json




options = Options()
options.headless = False
options.add_argument("user-agent=Mozilla/5.0 (Windows Phone 10.0; Android 4.2.1; Microsoft; Lumia 640 XL LTE) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Mobile Safari/537.36 Edge/12.10166")
driver= webdriver.Firefox(options=options,executable_path="/usr/local/bin/geckodriver")

with open("testertested.json", 'r') as read_file:
	data=json.load(read_file)

flag=True

for title, content in data.items():

	driver.get("https://www.paraphraser.io/")

	WebDriverWait(driver,10).until(EC.presence_of_element_located((By.ID,"input-content"))).send_keys(content)

	time.sleep(0.3)

	WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH, "//*[text()='Paraphrase Now ']"))).click()

	time.sleep(8)

	rephrased=(WebDriverWait(driver,10).until(EC.presence_of_element_located((By.ID,"output-content"))).text)

	if not flag:
		with open("tt_rephrased.json",'r') as new_read_file:
			new_data=json.load(new_read_file)

	else:
		flag=False
		new_data=dict()

	new_data[title]=rephrased
	

	with open("tt_rephrased.json",'w') as write_file:
		json.dump(new_data,write_file)
	
driver.quit()


