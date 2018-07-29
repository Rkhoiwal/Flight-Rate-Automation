from selenium import webdriver
	from selenium.webdriver.support.ui import WebDriverWait
	from selenium.common.exceptions import TimeoutException
	from google_flights_iata_code import iata_codes
	import csv
	import datetime



	#-------------------checks city inside kyes of dictionary------
	""" 
		parameter -  city name
		return - iata_codes[city][0] //1st value
	"""
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

	#---------------date range-------------
	def daterange(start_date, days_count):
	    for n in range(int(days_count)):
	        yield start_date + datetime.timedelta(n)
	#-------------------------------------------------------

	while(True):
		source = input("From :\t ")
		source_code = find_iata_code(source)
		if(source_code=="NULL"):
			print ("invalid city name")
			continue
		else:
			destination= input("To :\t")
			destination_code = find_iata_code(destination)
			if(destination_code=="NULL"):
				continue
		if(source_code and destination_code):
			break

	#------------- sample url -> #url='https://www.google.co.in/flights/#search;f=PNQ;t=BLR;d=2016-09-05;r=2016-09-09;eo=e'
	base_url = 'https://www.google.co.in/flights/#search'



	start_d    = input("start date(yyyy-mm-dd)  :  ")
	days_count = input("Data of how many days?  :  ")
	start_date =  datetime.datetime(int(start_d[:4]),int(start_d[5:7]),int(start_d[8:10]))


	sheet   =[] 
	airline =[]
	airtime =[]
	cost	=[]
	for i in range(0,100000):
		cost.append(0)


	#----------------------------------------------------------------------------------------------------------------------
	for single_date in daterange(start_date, days_count):
		driver=webdriver.Firefox()
		url = base_url+";f="+source_code+ ";t="+destination_code+";d="+single_date.strftime("%Y-%m-%d")+";tt=o;so=p;eo=e"
		driver.get(url)
		try:
			
			title = None
			prices = None
			flights = None
			time = None

			title=driver.execute_script('return document.title')
			prices=driver.find_elements_by_class_name('IHTR26B-d-yb')
			flights=driver.find_elements_by_class_name('IHTR26B-d-j')
			time =  driver.find_elements_by_class_name("IHTR26B-d-Xb")

		except TimeoutException as e:
			print("TimeOut...\nCheck Network Connection!")
		
		for i in range(0,100000):
			cost[i]=0

		for i in range(len(flights)):
			found = False
			for j in range(len(airline)):  
				if(airline[j]==flights[i].text and airtime[j]==time[i].text ):
					found = True
					cost[j]= prices[i].text
					break
			if (not found):
				airline.append(flights[i].text)
				airtime.append(time[i].text)
				try:
					cost[len(airline)]=prices[i].text
				except :
					print("Index out of bound")




		sheet.append(cost)
		driver.close()
