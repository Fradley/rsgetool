import wikiscraper
import pickle
import time
import logging
import requests

#This script gets all of the item links and exports them to a pickle

baseurl = 'https://runescape.wiki/w/RuneScape:Grand_Exchange_Market_Watch'

prefix =  'https://runescape.wiki'

pagepattern = r'w\/RuneScape:Grand_Exchange_Market_Watch\/'

itempattern = r'w\/Exchange:'

catlinks = wikiscraper.getLinks(baseurl, prefix, pagepattern)

timer = len(catlinks)

ticker = 0.0

itemlinks = []

for link in catlinks:
	ticker += 1
	try:
		element = wikiscraper.getLinks(link, prefix, itempattern)
		itemlinks += element
	except requests.exceptions.ConnectionError:
		print('bad link ' + link)
	time.sleep(.25)
	pcnt = int((ticker / timer) * 100.0)
	if ticker % 10 == 0:
		s = str(pcnt) + " % complete."
		print(s)
	
	
pickle.dump(itemlinks, open('items.p', 'wb'))
