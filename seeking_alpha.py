import json
from urllib import urlopen
import re
import pandas as pd

def pull_data():

	df = pd.DataFrame(columns = ['Date', 'Ticker', 'Title', 'Direction', 'Market Cap', 'Top', 'Disclosure'])

	article_date = "2014/11/26"

	try:
		response = urlopen("http://seekingalpha.com/analysis/all/editors-picks/"+article_date)
		webpage = response.read()

		patFinderTitle = re.compile("sasource='analysis_articles'>(.*)</a>")
		patFinderLink = re.compile("<a class='article_title' href='(.*)' ")

		findPatTitle = re.findall(patFinderTitle, webpage)
		findPatLink = re.compile(patFinderLink, webpage)

		for item in findPatTitle:
			split = item.split(", ")
			for title in split:
				df = df.append({'Title':title})

		for item in findPatLink:
			split = item.split(", ")
			for link in split:
				print link
	except:
		pass

	df.to_csv("seeking_alpha_stats.csv")

def pull_link():
	webpage = "http://seekingalpha.com/analysis/all/editors-picks"

	response = urlopen(webpage)
	webpage = response.read()

	print webpage

	patFinderLink = re.compile("<a class='article_title' href='(.*)' ")

	findPatLink = re.findall(patFinderLink, webpage)

	for item in findPatLink:
		split_item = item.split(", ")
		for link in split_item:
			print link

def pull_title():
	webpage = "http://seekingalpha.com/analysis/all/editors-picks"

	response = urlopen(webpage)
	webpage = response.read()

	#print webpage

	patFinderTitle = re.compile("sasource='analysis_articles'>(.*)</a>")

	findPatTitle = re.findall(patFinderTitle, webpage)

	for item in findPatTitle:
		split_item = item.split(", ")
		for title in split_item:
			print title


#pull_data()
pull_link()
#pull_title()