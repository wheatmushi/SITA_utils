import requests
from time import localtime, strftime
from bs4 import BeautifulSoup
import json


date = '14-9'


def url_former(date, airport):
    if airport == 'svo':
        return ('http://svo.aero/en/timetable/today/?text=su&day=' + date, None)
    if airport == 'led':
        return ('https://www.pulkovoairport.ru/f/flights/cur/en_dep_1.js', None)
    if airport == 'vko':
        return ('http://www.vnukovo.ru/en/flights/online-timetable/#tab-sortie', 'arDF_sf[current_day]=today')

def separator(strtag):
    n = strtag.string
    if n:
        return n
    else:
        m = list(strtag.children)
        return [i.string for i in m if i.string not in (None,'\n',' ')]

def flatter(unflist):
    flist = []
    for i in range(len(unflist)):
        if type(unflist[i]) == list:
            for j in unflist[i]: flist.append(j)
        else:
            flist.append(unflist[i])
    return flist

def led_cleaner(flight_data,params):
    clrd_flight_data = {}
    for p in params:
        clrd_flight_data[p] = flight_data[p]
    return clrd_flight_data

def data_parser(date, airport):
    urlparams = url_former(date,airport)
    page = requests.get(urlparams[0],urlparams[1])
    soup = BeautifulSoup(page.content, 'html.parser')
    if airport == 'svo':
        t = soup.select('table')[1]
        table = t.select('tr')
        table = [string.select('td') for string in table[1:]]
        table = [[(f.string).replace(u'\xa0', u' ') for f in string if f.string != None] for string in table]
        table = [string if len(string)==7 else string + [''] for string in table]
    elif airport == 'vko':
        t = soup.select('table')[1]
        table = t.select('tr')
        table = [string.select('td') for string in table]
        table = [[separator(elem) for elem in string] for string in table[:-1]]
        table = [flatter(string) for string in table]
        table = [string for string in table if ('Aeroflot' in string[3] or 'Rossiya Airlines' in string[3])]
    elif airport == 'led':
        table = json.loads(page.text)['data']
        params = ['number', 'status', 'company', 'airport', 'date', 'aircraft_type_code']
        table = [led_cleaner(flight, params) for flight in table if (flight['company'] == 'Rossiya' or flight['company'] == 'Aeroflot')]

    return table


def formatter(table,airport):
    if airport == 'svo':
        ftable = [(u'{0:>12}{1:>8}{2:>5}{3:>7}{4:>22}{5:>4}{6:>18}').format(*string) for string in table]
    elif airport == 'vko':
        ftable = [(u'{0:>6}{1:>12}{2:>9}{3:>32}{4:>32}{5:>3}{6:>43}').format(*string) for string in table]
    elif airport == 'led':
        ftable = [(u'{0:>7}{1:>12}{2:>11}{3:>22}{4:>23}{5:>6}').format(s['date'], s['number'], s['company'],
                                                                      s['airport'], s['status'],
                                                                      s['aircraft_type_code'])
        for s in table]
    return ftable

def file_writer(table,airport):
    name = airport.upper() + '  ' + datetime
    f = open(name + '.txt','w', encoding='utf-8')
    f.write(name + '\n\n')
    for string in table:
        f.writelines(string + '\n')
    f.close()


airport = ''
while airport not in ('led', 'svo', 'vko'):
    airport = input('enter \'led\' or \'svo\' or \'vko\' to choose airport\n')
datetime = strftime("%Y-%b-%d  %H-%M-%S", localtime())

table = data_parser(date, airport)
file_writer(formatter(table,airport),airport)
