from selenium import webdriver   									
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from google_flights_iata_code import iata_codes
import csv
import datetime

def find_iata_code(city):
	code = "NULL"
	if city in iata_codes.keys():
		code = iata_codes[city][0]
	else 
		for key in iata_codes.keys():
			if city in key:
				code = iata_codes[key][0]
				break
	return code

driver=webdriver.Firefox()
driver.implicitly_wait(30)

src_code="NULL"


while(src_code not equal )
