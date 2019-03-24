import requests
from time import localtime, strftime
from bs4 import BeautifulSoup
import json


url = 'https://www.pulkovoairport.ru/f/flights/cur/en_dep_1.js'
page = requests.get(url)
t = json.loads(page.text)['data']

t1 = [flight for flight in t if (flight['company']=='Rossiya' or flight['company']=='Aeroflot')]

def led_cleaner(flight_data,params):
    clrd_flight_data = {}
    for p in params:
        clrd_flight_data[p] = flight_data[p]
    return clrd_flight_data

params = ['number','status','company','airport','date','aircraft_type_code']
t2 = [led_cleaner(flight,params) for flight in t1]
print(t2)