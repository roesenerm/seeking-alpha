import json
from urllib import urlopen
import re

def pull_data():

	try:
		response = urlopen("http://seekingalpha.com/analysis/all/editors-picks")
		webpage = response.read()

		patFinderTitle = re.compile("sasource='analysis_articles'>(.*)</a>")
		patFinderLink = re.compile("<a class='article_title' href='(.*)' ")

		findPatTitle = re.findall(patFinderTitle, webpage)
		findPatLink = re.compile(patFinderLink, webpage)

		for item in findPatTitle:
			split = item.split(", ")
			for title in split:
				print title

		for i in findPatLink:
			split = i.split(", ")
			for link in split:
				print link
	except:
		pass

def pull_data2():
	webpage = "http://seekingalpha.com/analysis/all/editors-picks"

	response = urlopen(webpage)
	webpage = response.read()

	patFinderLink = re.compile("sasource='analysis_articles'>(.*)</a>")

	findPatLink = re.findall(patFinderLink, webpage)

	for i in findPatLink:
		split = i.split(", ")
		for j in split:
			print j

pull_data()
#pull_data2()