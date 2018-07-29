from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from google_flights_iata_code import iata_codes
import csv
import datetime

def find_iata_code(city):
	code="NULL"
	if city in iata_codes.keys():
		code=iata_codes[city][0]
	else:
		for key in iata_codes.keys():
			if city in key:
				code=iata_codes[key][0]
				break
	return code

driver=webdriver.Firefox()
driver.implicitly_wait(30)

src=input("from:")
src_code=find_iata_code(src)

while(src_code=="NULL"):
	print("Invalid source location!!!\nTry Again.")
	src=input("from:")
	src_code=find_iata_code(src)

dest=input("to:")
dest_code=find_iata_code(dest)

while(dest_code=="NULL"):
	print("Invalid destination location!!!\nTry Again.")
	dest=input("to:")
	dest_code=find_iata_code(dest)

journey_d=input("Journey date(yyyy-mm-dd):")


base_url = 'https://www.google.co.in/flights/#search'
#url='https://www.google.co.in/flights/#search;f=PNQ;t=BLR;d=2016-09-05;r=2016-09-09;eo=e'
#current urls
#standard format, currency indian
#https://www.google.co.in/flights/#flt=/m/019flv.r/m/02j9z.2018-08-14*r/m/02j9z./m/019flv.2018-08-18;c:INR;e:1;sd:1;t:e
#class as premium
#https://www.google.co.in/flights/#flt=/m/019flv.r/m/02j9z.2018-08-14*r/m/02j9z./m/019flv.2018-08-18;c:INR;e:1;sc:p;sd:1;t:e
#ONe-way trip, no of passenger(px) as 2 
#https://www.google.co.in/flights/#flt=/m/019flv.r/m/02j9z.2018-08-14;c:INR;e:1;px:2;sc:p;sd:1;t:e;tt:o
url = base_url+";f="+find_iata_code(src)+ ";t="+find_iata_code(dest)+";d="+journey_d+";tt=o;so=t;eo=e"


driver.get(url)

try:
	
	title=driver.execute_script('return document.title')
	prices=driver.find_elements_by_class_name('IHTR26B-d-yb')
	flights=driver.find_elements_by_class_name('IHTR26B-d-j')
	time =  driver.find_elements_by_class_name("IHTR26B-d-Xb")

except TimeoutException as e:
	print("TimeOut...\nCheck Network Connection!!!")

#f=open("googl_flight_html.txt","w")
#f.write(html1)
#f.write("\n\n------------------------------------\n\n")


msg="\n*****Flights from %s to %s on %s*****" % (src.title(),dest.title(),journey_d)
print(msg)
print("-"*len(msg))

airline_time = []

for i in range(len(prices)):
	airline_time.append(flights[i].text+time[i].text)
#	print("%20s\t%s" % (flights[i].text,prices[i].text))

# for i in range(len(airline_time)):
# 	print (airline_time[i])

#----------------------2nd link--------------------------------------------------------------------
#next day string
date = datetime.datetime(int(journey_d[:4]),int(journey_d[5:7]),int(journey_d[8:10]))
date += datetime.timedelta(days=1)
next_d = date.strftime('%Y-%m-%d')


# for next day
url2= base_url+";f="+find_iata_code(src)+ ";t="+find_iata_code(dest)+";d="+next_d+";tt=o;so=t;eo=e"

#--------------------------------------------------------------------------------------------------

# opening new driver
driver2=webdriver.Firefox()
driver2.implicitly_wait(30)


driver2.get(url2)

#---------------------------------------------------------------------------------------------------
try:
	
	title2=driver2.execute_script('return document.title')
	prices2=driver2.find_elements_by_class_name('IHTR26B-d-yb')
	flights2=driver2.find_elements_by_class_name('IHTR26B-d-j')
	time2 =  driver2.find_elements_by_class_name("IHTR26B-d-Xb")

except TimeoutException as e:
	print("TimeOut...\nCheck Network Connection!!!")

#f=open("googl_flight_html.txt","w")
#f.write(html1)
#f.write("\n\n------------------------------------\n\n")


msg="\n*****Flights from %s to %s on %s*****" % (src.title(),dest.title(),next_d)
print(msg)
print("-"*len(msg))

airline_time2 = []

# for i in range(len(prices2)):
# 	airline_time2.append(flights2[i].text+time2[i].text)
# 	print("%20s\t%s" % (flights2[i].text,prices2[i].text))

# for i in range(len(airline_time2)):
# 	print (airline_time2[i])

#save to the zip file rahul.gz
with gzip.open('rahul' + ".gz", "wb") as outfile:
    outfile.write(bytes(airline_time2, 'UTF-8'))

#-------------------format--------------------------------------------------------------------------------
# 								(airline,time)columns 
# 					   value1	value2		value3		value4
# date   				   
# 1					   cost		cost		cost
# 2					   cost  	cost  		cost
# 3
#                      evevry row is stored in a list. so date1_cost=[],date2_cost[] , and airlinetime_columns=[]

# airlinetime_columns= airline_time[:]  # 1st names of columns initialized using 1st link
# date1_cost         = prices[:]        # 1st cost row initialized

# date2_cost=[]
# for i in range(len(airline_time)):
# 	date2_cost.append(0)


# for i in range(len(airline_time2)):
# 	found= False
# 	for j in range(len(airlinetime_columns)):
# 		if(airline_time2[i]==airlinetime_columns[j]):
# 			date2_cost[j]=prices2[i]
# 			found = True
# 	if not found :
# 		airlinetime_columns.append(airline_time2[i])
# 		date2_cost.append(prices2[i])


# for i in range(1,5):
# 	print(airlinetime_columns[i])
# 	print(date1_cost[i])
# 	print(date2_cost[i])


"""
OUTPUT:-)
from:hyderabed
Invalid source location!!!
Try Again.

from:hyderabed

to:mumbai

Journey date(yyyy-mm-dd):2016-09-13

*****Flights from hyderabed to Mumbai on 2016-09-13*****
--------------------------------------------------------
            SpiceJet     2,318

"""
