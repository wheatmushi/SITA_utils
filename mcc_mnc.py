import requests
from time import localtime, strftime
from bs4 import BeautifulSoup


url = 'http://www.mcc-mnc.com/'
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')

t = soup.find(id='mncmccTable')
table = t.select('tr')
table = [string.select('td') for string in table[1:]]
table = [[str(elem.string).replace(';','') for elem in string] for string in table]
table = [t[0:2] + [t[0] + t[1]] + t[2:] for t in table]
table_of_strings = [(';'.join(string)+'\n') for string in table]

date = strftime("%Y-%b-%d", localtime())
file = open('MNC-MCC '+date+'.csv', 'w')

file.write('MCC;MNC;MCC+MNC;ISO;Country;Country Code;Network\n')
for line in table_of_strings:
    file.write(line)

file.close()

print("\ninfo successfully extracted to 'MNC-MCC "+date+".csv'\n")