import pickle
import wikiscraper
import time
import requests
from pymongo import MongoClient
import datetime


client = MongoClient('localhost', 27017)
db = client['itemdb']

items = pickle.load(open('items.p', 'rb'))

#remove duplicate items
items = set(items)

count = len(items)

ticker = 0.0

ts = time.time()
for item in items:
	ticker += 1

	try:
		post = wikiscraper.getInfo(item)
		db['items'].insert_one(post)
	except requests.exceptions.ConnectionError:
		print('bad link ' + link)
		
	
	pcnt = int((ticker / count) * 100.0)
	tn = time.time() - ts
	if ticker % 10 == 0:
		elapsed = int(tn)
		estlen = int((count / ticker) * tn)
		s = str(pcnt) + " % complete.\tElapsed: " + str(elapsed) + "\tETA: " + str(datetime.timedelta(seconds=(estlen - elapsed)))
		print(s)
