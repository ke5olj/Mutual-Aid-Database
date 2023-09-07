import tkinter as tk
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException  
from selenium.webdriver import ActionChains
import pandas as pd
import math
from collections import OrderedDict
import datetime
from datetime import datetime
import time
import os
import openpyxl as xl
import win32clipboard
import sqlite3
import argparse


# define argument parser settings
parser=argparse.ArgumentParser()
parser.add_argument('--hl',action='store_true', help='input -hl to open chrome in headless mode')
parser.add_argument('--d',action='store_true', help='debug mode')
args=parser.parse_args()






# conn=sqlite3.connect("test.db")
conn=sqlite3.connect("cc_county_assessor.db")
c=conn.cursor()
# c.execute("""CREATE TABLE scraped_data (
				# scrpd_acct_data text,
				# acct_num text,
				# owner text,
				# value text,
				# local_addrs text,
				# parcel_ID text,
				# land_size text,
				# property_class text,
				# neighborhood text,
				# mail_addrs1 text,
				# mail_addrs2 text,
				# description text,
				# acrage text,
				# sqft text,
				# business text,
				# lat text,
				# long text,
				# url text
				# )""")


os.system("cls")
start_time=time.time()



if args.hl:
	# ***************************** HEADLESS MODE *****************************
	from selenium.webdriver.chrome.options import Options
	from selenium.webdriver.common.by import By
	from webdriver_manager.chrome import ChromeDriverManager
	chrome_options=Options()
	chrome_options.add_argument("--headless")
	chrome_options.add_argument('--no-sandbox') #should resolve the "SBOX_FATAL_MEMORY_EXCEEDED" error
	driver = webdriver.Chrome(ChromeDriverManager().install(),chrome_options=chrome_options)
	# *************************************************************************
else:
	# ***************************** HEADED MODE *******************************
	from webdriver_manager.chrome import ChromeDriverManager
	chrome_options=Options()
	chrome_options.add_argument('--no-sandbox')
	driver = webdriver.Chrome(ChromeDriverManager().install(),chrome_options=chrome_options)
	# *************************************************************************






# ***************************** HEADED MODE *******************************
# from webdriver_manager.chrome import ChromeDriverManager
# driver = webdriver.Chrome(ChromeDriverManager().install())
# # # *************************************************************************


# ***************************** HEADLESS MODE *****************************
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By
# from webdriver_manager.chrome import ChromeDriverManager
# chrome_options=Options()
# chrome_options.add_argument("--headless")
# driver = webdriver.Chrome(ChromeDriverManager().install(),chrome_options=chrome_options)
# *************************************************************************



sleepSec=5

#read in from property data spreadsheet
if args.d:
	dfProp=pd.read_excel(r"C:\Users\ke5ol\Documents\norman property list\test_merged_prop_list.xlsx",sheet_name='Sheet1')
else:	
	dfProp=pd.read_excel(r"C:\Users\ke5ol\Documents\norman property list\master_merged_prop_list.xlsx",sheet_name='pass_2')




#read in from property data spreadsheet
dfProp=pd.read_excel(r"C:\Users\ke5ol\Documents\norman property list\master_merged_prop_list.xlsx",sheet_name='Sheet1')
# dfProp=pd.read_excel(r"C:\Users\ke5ol\Documents\norman property list\test_merged_prop_list.xlsx",sheet_name='Sheet1')
owner=[]
localAddrs=[]
value=[]
parcelID=[]
website=[]
links=[]
owner=dfProp['Owner '].to_dict()
localAddrs=dfProp['Address'].to_dict()
value=dfProp['Market Value '].to_dict()
parcelID=dfProp['Parcel ID'].to_dict()
website=dfProp['Website'].to_dict()
links=dfProp['Account # '].to_dict()


# click initial button
firstURL="https://property.spatialest.com/ok/cleveland/#/"
driver.get(firstURL)
submit_button=driver.find_element_by_xpath("//button[@class='submitButton btn btn-primary']")
submit_button.click()



min_val=0
max_val=len(links)

for i in range(min_val,max_val):
# for i in range(0,len(links)):
	if(i==0):
		# select account number option in drop down
		dropDown=driver.find_element_by_xpath('//*[@id="rct-main-app"]/div[1]/div/div[2]/div/div/div/div/div[1]/div/div/div[1]/div/div[2]/div')
		dropDown.click()
		selectAcctNum=driver.find_element_by_xpath('//*[@id="rct-main-app"]/div[1]/div/div[2]/div/div/div/div/div[1]/div/div/div[1]/div/div[2]/div/div/button[2]')
		selectAcctNum.click()
		# input account number into first search box and hit enter
		inputElement = driver.find_element_by_xpath('//*[@id="primary_search"]')
		inputElement.send_keys(links[i])
		inputElement.send_keys(Keys.ENTER)
		time.sleep(sleepSec)
	else:
		# time.sleep(5)
		inputElement = driver.find_element_by_xpath('//*[@id="primary_search"]')
		inputElement.clear()
		inputElement.send_keys(links[i])
		inputElement.send_keys(Keys.ENTER)
		time.sleep(sleepSec)
		

	# get property account number for error checking (check the scraped account number vs the one from the read in spreadsheet)
	scrapedAcctData=driver.find_elements_by_xpath('/html/body/main/div/div[2]/div[1]/div[2]/div/section/div[2]/div[1]/div[2]/header/div/div/div[1]/div[1]/span')
	if(len(scrapedAcctData)==0):
		scrapedAcctDataOut="not found"
	else:
		for j in range(0,len(scrapedAcctData)):
			scrapedAcctDataOut=scrapedAcctData[j].text

	# get land size
	landSize=driver.find_elements_by_xpath('/html/body/main/div/div[2]/div[1]/div[2]/div/section/div[2]/div[4]/div/div/div/div[1]/div/div/div[2]/div/div/div/div[1]/div/div/div/div/div/ul/li[2]/p[1]/span[2]')
	if(len(landSize)==0):
		landSizeOut="not found"
	else:
		for j in range(0,len(landSize)):
			landSizeOut=landSize[j].text

	# get property class type
	propClass=driver.find_elements_by_xpath('/html/body/main/div/div[2]/div[1]/div[2]/div/section/div[2]/div[4]/div/div/div/div[1]/div/div/div[2]/div/div/div/div[1]/div/div/div/div/div/ul/li[3]/p[1]/span[2]')
	if(len(propClass)==0):
		propClassOut="not found"
	else:
		for j in range(0,len(propClass)):
			propClassOut=propClass[j].text	
	# get neighborhood type
	nghbrhood=driver.find_elements_by_xpath('/html/body/main/div/div[2]/div[1]/div[2]/div/section/div[2]/div[4]/div/div/div/div[1]/div/div/div[2]/div/div/div/div[1]/div/div/div/div/div/ul/li[5]/p[2]/span[2]')
	if(len(nghbrhood)==0):
		nghbrhoodOut="not found"
	else:
		for j in range(0,len(nghbrhood)):
			nghbrhoodOut=nghbrhood[j].text	
		
	# get mailing address
	mailAddrss=driver.find_elements_by_xpath('/html/body/main/div/div[2]/div[1]/div[2]/div/section/div[2]/div[4]/div/div/div/div[1]/div/div/div[2]/div/div/div/div[1]/div/div/div/div/div/ul/li[7]/p/span[2]')
	if(len(mailAddrss)==0):
		mailAddrssOut="not found"
	else:
		for j in range(0,len(mailAddrss)):
			mailAddrssOut=mailAddrss[j].text	
	# get mailing address state
	mailAddrss2=driver.find_elements_by_xpath('	/html/body/main/div/div[2]/div[1]/div[2]/div/section/div[2]/div[1]/div[2]/header/div/div/div[2]/div/div[2]')
	if(len(mailAddrss2)==0):
		mailAddrss2Out="not found"
	else:
		for j in range(0,len(mailAddrss2)):
			mailAddrss2Out=mailAddrss2[j].text			
	# get property description
	propDescpt=driver.find_elements_by_xpath('/html/body/main/div/div[2]/div[1]/div[2]/div/section/div[2]/div[4]/div/div/div/div[2]/div/div/div[2]/div/div/div/div/div/div/div/div/div/div/div[2]/div/div/div[2]/div/div/div/ul/li[1]/p[2]/span[2]')
	if(len(propDescpt)==0):
		propDescptOut="not found"
	else:
		for j in range(0,len(propDescpt)):
			propDescptOut=propDescpt[j].text			
	# get acrage size
	acrage=driver.find_elements_by_xpath('/html/body/main/div/div[2]/div[1]/div[2]/div/section/div[2]/div[4]/div/div/div/div[4]/div/div/div[2]/div/div/div/div/div/div/div/div/div/table/tbody/tr/td[4]')
	if(len(acrage)==0):
		acrageOut="not found"
	else:
		for j in range(0,len(acrage)):
			acrageOut=acrage[j].text		
	# get sqft
	sqft=driver.find_elements_by_xpath('/html/body/main/div/div[2]/div[1]/div[2]/div/section/div[2]/div[4]/div/div/div/div[2]/div/div/div[2]/div/div/div/div/div/div/div/div/div/div/div[2]/div/div/div[2]/div/div/div/ul/li[10]/p[2]/span[2]')
	if(len(sqft)==0):
		sqftOut="not found"
	else:
		for j in range(0,len(sqft)):
			sqftOut=sqft[j].text				
	# get business name
	bizName=driver.find_elements_by_xpath('/html/body/main/div/div[2]/div[1]/div[2]/div/section/div[2]/div[4]/div/div/div/div[5]/div/div/div[2]/div/div/div/div/div/div/div/div/div/table/tbody[1]/tr/td[1]')
	if(len(bizName)==0):
		bizNameOut="not found"
	else:
		for j in range(0,len(bizName)):
			bizNameOut=bizName[j].text	
		
	# get GPS coords
	# click dropdown in map container to copy to clipboard
	try:
		achains=ActionChains(driver)
		rClkMap=driver.find_element_by_xpath('/html/body/main/div/div[2]/div[1]/div[2]/div/section/div[2]/div[2]/div/div/div[2]/div/div[4]/div[3]/div[6]')
		achains.context_click(rClkMap).perform()
		time.sleep(1)
		getCoords=driver.find_element_by_xpath('/html/body/main/div/div[2]/div[1]/div[2]/div/section/div[2]/div[2]/div/div/div[2]/div/div[4]/div[3]/div[6]/ul/li[4]')
		getCoords.click()
		# get coords off of clipboard
		win32clipboard.OpenClipboard()
		GPSCoods = win32clipboard.GetClipboardData()
		openP=GPSCoods.find("(")
		closeP=GPSCoods.find(")")
		latLong=GPSCoods[openP:closeP]
		comma=latLong.find(",")
		openP=latLong.find("(")
		closeP=latLong.find(")")
		lat=latLong[openP+1:comma]
		long=latLong[comma+2:len(latLong)]
		win32clipboard.CloseClipboard()

	except:
		GPSCoods='not found'
		lat=""
		long=""
	
	c.execute("INSERT INTO scraped_data VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", (scrapedAcctDataOut,links[i],owner[i],value[i],localAddrs[i],parcelID[i],landSizeOut,propClassOut,nghbrhoodOut,mailAddrssOut,mailAddrss2Out,propDescptOut,acrageOut,sqftOut,bizNameOut,lat,long,website[i]))
	conn.commit()
	# print(pd.read_sql_query("SELECT * FROM scraped_data4", conn))	
	
	time.sleep(sleepSec)

conn.close()
driver.close()

print("DONE")
print("\n")
print("Run time: %s mins" % str((time.time() - start_time)/60))