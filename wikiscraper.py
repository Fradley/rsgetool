import requests
from numpy import NaN
import datetime as datetime
from bs4 import BeautifulSoup
import re
import locale


def getInfo(url):

	item = requests.get(url)
	item = BeautifulSoup(item.text, 'html.parser')
	
	itemdata = {'itemid'	: NaN,
							'itemname': '',
							'url'			: url,
							'buylimit': NaN,
							'highalch': NaN,
							'lowalch'	: NaN,
							'price'		: NaN,
							'updated'	: datetime.datetime.now,
							'series'	: []
							}
	
	locale.setlocale( locale.LC_ALL, 'en_US.UTF-8' ) 
	
	#grab values from the html
	values = [item.find(id='exchange-itemid').text, 
						item.find(class_='gemw-name').text,
						item.find(id='exchange-highalch').text, 
						item.find(id='exchange-lowalch').text,
						item.find(class_='gemw-price').text,
						item.find(id='exchange-limit').text
						]
	
	#try-except blocks to allow default values to override if non-int is passed
	try:
		itemdata['itemid'] = int(values[0])
	except (TypeError, ValueError):
		pass
	
	if values[1]:
		itemdata['itemname'] = values[1]
	
	try:
		itemdata['highalch'] = int(locale.atoi(values[2]))
	except (TypeError, ValueError):
		pass
	
	try:
		itemdata['lowalch'] = int(locale.atoi(values[3]))
	except (TypeError, ValueError):
		pass
	
	
	itemdata['price'] = int(locale.atoi(values[4]))
	
	date = item.find(class_='gemw-updated')['data-date']
	
	#Fix when able to tell if month is given as Aug or August
	try:
		dt = datetime.datetime.strptime(date, '%d %b %Y, %H:%M (%Z)')
	except ValueError:
		dt = datetime.datetime.strptime(date, '%d %B %Y, %H:%M (%Z)')
		
	
	itemdata['updated'] = dt
	
	try:
		itemdata['buylimit'] = int(locale.atoi(values[5]))
	except (TypeError, ValueError):
		pass
	
	
	return itemdata
	

def getLinks(url, prefix, pattern):
	
	page = requests.get(url)
	regex = re.compile(pattern)
	pagesoup = BeautifulSoup(page.text, features='lxml')
	links = []
	for link in pagesoup.find_all('a', attrs={'href': regex}):
		links.append(prefix + link.get('href'))
	return links
	
	
def getItemPrice(url):
	
	item = requests.get(url)
	item = BeautifulSoup(item.text, 'html.parser')
	locale.setlocale( locale.LC_ALL, 'en_US.UTF-8' )
	
	try:
		price = int(locale.atoi(item.find(class_='gemw-price').text))
	except (TypeError, ValueError):
		price = NaN
	return price
	
	
