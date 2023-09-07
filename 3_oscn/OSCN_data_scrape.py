from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd
import math
from collections import OrderedDict



# PATH="C:\Program Files (x86)\chromedriver.exe"
# driver=webdriver.Chrome(PATH)


from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(ChromeDriverManager().install())


# URL format

# https://www.oscn.net/dockets/Results.aspx
# ?db=oklahoma
# &number=
# &lname=
# &fname=
# &mname=
# &DoBMin=
# &DoBMax=
# &partytype=
# &apct=
# &dcct=26
# &FiledDateL=08%2F01%2F2020
# &FiledDateH=08%2F15%2F2020
# &ClosedDateL=
# &ClosedDateH=
# &iLC=
# &iLCType=
# &iYear=
# &iNumber=
# &citation=


# define variables
caseName=[]
caseURL=""
caseURLlist=[]
i=0
j=0
k=0
hasWas=0
docket_list=[]
issueOut=0

# define desired county and date range
county="cleveland"
L_date="11/01/2021"
H_date="11/15/2021"
# put dates into URL format
L_date=L_date.replace("/","%2F")
H_date=H_date.replace("/","%2F")

searchURL="https://www.oscn.net/dockets/Results.aspx?db=%s&number=&lname=&fname=&mname=&DoBMin=&DoBMax=&partytype=&apct=&dcct=26&FiledDateL=%s&FiledDateH=%s&ClosedDateL=&ClosedDateH=&iLC=&iLCType=&iYear=&iNumber=&citation=" % (county,L_date,H_date)

driver.get(searchURL)

#get each case URL
caseURL=driver.find_elements_by_xpath('//*[@id="TABLE_1"]/tbody/tr/td[3]/a')

# get URL and case name
for i in range(0,len(caseURL)): 
	caseURLlist.append(caseURL[i].get_attribute("href")) #get URL
	caseName.append(caseURL[i].text) #get case name

#remove duplicate URLS/case names from lists and keep in proper order
caseName=list(OrderedDict.fromkeys(caseName))
caseURLlist=list(OrderedDict.fromkeys(caseURLlist))

	
# browse to each URL and check for issue and writ of assistance	
for i in range(0,len(caseURLlist)):
	driver.get(caseURLlist[i])
	issue=driver.find_elements_by_xpath('//*[@id="TABLE_4"]/tbody/tr/td[2]')
	hasWas=""
	for j in range(0,len(issue)):
		issueTest=issue[j].text
		if(issueTest.find("INDEBTEDNESS")>0 or issueTest.find("FORCIBLE ENTRY & DETAINER")>0):
			issueOut=issueTest
			docket=driver.find_elements_by_xpath('//*[@id="TABLE_6"]/tbody/tr/td[2]/font/nobr')
			for k in range(0,len(docket)):
				if(docket[k].text=='WAS'): # check for writ of assistance
					hasWas='WAS'
					break

					
	docket_item = {
		'Case Name': caseName[i],
		'Issue': issueOut,
		'Case URL': caseURLlist[i],
		'Writ of Assistance?': hasWas
		}
	docket_list.append(docket_item)
			

df=pd.DataFrame(docket_list)		
with pd.ExcelWriter(r'C:\Users\ke5ol\Desktop\OTU Evictions\OSCN_data.xlsx', engine='openpyxl', mode='w') as writer:
			df.to_excel(writer, sheet_name="OSCN Data",index=False)

print("\n")
print("DONE")
print("\n")
driver.close()


