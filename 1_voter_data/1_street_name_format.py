import pandas as pd
import numpy as np
import math
import os
import time
import sys

os.system("cls")
start_time=time.time()

df=pd.read_csv(r"C:\Users\ke5ol\Documents\norman property list\2023_07_22_run\CTY14_vr.csv",sep=",",encoding='cp1252',dtype=str)
dfFilter=df[df['City']=="NORMAN"]
dfFilter=dfFilter.reset_index(drop=True)

StreetDir=dfFilter['StreetDir']
StreetDir=StreetDir.replace({np.nan: ''})
StreetName=dfFilter['StreetName']
StreetType=dfFilter['StreetType']
StreetType=StreetType.replace({np.nan: ''})


# define variables
i=0
nameOut=0
# fullStreetName={}
fullStreetName=pd.DataFrame(columns=["STREET"])


# iterate through street and format numerical streetnames with suffix
# for index, name in enumerate(StreetName):
for n in range(0,len(StreetName)):
	name=StreetName.iloc[n]
	if(name.isnumeric()==True):
			print('\n')
			print("iteration: %i" % n)
			print(name)
			print(name[-1])
			print(name[-2:])
			print(type(name[-2:]))
			print('\n')
		if(len(name)<=2):
			if(name[-1] == "1" and name != "11"):
				nameOut=str(name+"ST")
			elif(name[-1] == "2" and name != "12"):
				nameOut=str(name+"ND")
			elif(name[-1] == "3" and name != "13"):
				nameOut=str(name+"RD")
			else:
				nameOut=str(name+"TH")
		elif(len(name)>=3):

			if(name[-1] == "1" and name[-2:] != "11"):
				print('\n')
				print(name[-1])
				print(name[-2:])
				print('\n')
				nameOut=str(name+"ST")
				print('\n')
				print(nameOut)
				print('\n')
			elif(name[-1] == "2" and name[-2:] != "12"):
				print('\n')
				print(name[-1])
				print(name[-2:])
				print('\n')
				nameOut=str(name+"ND")
				print('\n')
				print(nameOut)
				print('\n')
			elif(name[-1] == "3" and name[-2:] != "13"):
				print('\n')
				print(name[-1])
				print(name[-2:])
				print('\n')
				nameOut=str(name+"RD")
				print('\n')
				print(nameOut)
				print('\n')
			elif(name[-2:] == "11" or name[-2:] == "12" or name[-2:] == "13"):
				print('\n')
				print(name[-1])
				print(name[-2:])
				print('\n')
				nameOut=str(name+"TH")	
				print('\n')
				print(nameOut)
				print('\n')				
		
	# handle outlier numeric names
	elif(name=="8 AVENUE"):
		nameOut="8TH AVENUE"
	else:
		nameOut=name
	# assemble full street name
	# [direction] + [street name] + [street type]
	fullStreetName.loc[i]=pd.Series({"STREET":(('"'+((str(StreetDir.iloc[n])+" "+str(nameOut)+" "+str(StreetType.iloc[n])).strip())+'"').replace('nan','')).strip()})
	i+=1

# remove duplicate street names
# fullStreetName=pd.DataFrame(fullStreetName)
fullStreetName=fullStreetName.drop_duplicates()
fullStreetName=fullStreetName.reset_index(drop=True)
# print(fullStreetName)
fullStreetName.to_csv('outputStreetTest.csv', index=False)
print("Run time: %s mins" % str((time.time() - start_time)/60))