import json
import urllib2
from urllib2 import Request, urlopen, URLError
import re
import pandas as pd
import cookielib
from cookielib import CookieJar
import datetime
from datetime import date, timedelta as td
from yahoo_finance import Share


def pull_data():

	df = pd.DataFrame(columns = ['Date', 'Ticker', 'Title', 'Direction', 'Market Cap', 'Editor-Picks', 'Author-Followers', 'Initial-Stock-Price', 'Current-Stock-Price1', 'Current-Stock-Price5', 'Current-Stock-Price10', 'Current-Stock-Price30', 'Current-Stock-Price90', 'sp500-Price1', 'sp500-Price5', 'sp500-Price10', 'sp500-Price30', 'sp500-Price90'])

	sp500_df = pd.DataFrame.from_csv("YAHOO-INDEX_GSPC.csv")

	d1 = date(2014, 11, 20)
	d2 = date(2014, 11, 26)

	delta = d2 - d1

	value_list = []

	for i in range(delta.days + 1):
		a_date = d1 + td(days=i)
		#print a_date
		article_date = a_date.strftime("%Y/%m/%d")
		print article_date
		webpage = "http://seekingalpha.com/analysis/all/all/" + str(article_date)

		#print webpage

		try:

			cj = CookieJar()
			opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
			opener.addheaders = [('User-agent', 'Mozilla/5.0')]

			webpage = opener.open(webpage).read()

			try:

				patFinderLink = re.compile("<a class='article_title' href='(.*)' ")

				findPatLink = re.findall(patFinderLink, webpage)

				#print findPatLink

				try:

					for item in findPatLink:
						split_item = item.split(", ")

						try:

							for link in split_item:
								print link

								try:

									source = "http://seekingalpha.com" + str(link)

									source = opener.open(source).read()

									try:

										patFindDate = re.compile('<span itemprop="datePublished".*">(.*)</span>')

										findPatDate = re.findall(patFindDate, source)

									except:
										findPatDate = "NA"


									try:

										patFinderTitle = re.compile('<span itemprop="headline">(.*)</span>')

										findPatTitle = re.findall(patFinderTitle, source)

										#print findPatTitle[0]

									except:
										findPatTitle = "NA"

									try:
										patFinderPrimaryStock = re.compile('about_primary_stocks.*"(.*)" title')

										findPatPrimaryStock = re.findall(patFinderPrimaryStock, source)

										findPatPrimaryStock = 'http://seekingalpha.com' + findPatPrimaryStock[0]

										#print findPatPrimaryStock
									except:
										pass

									try:

										patFinderTicker = re.compile("about_primary_stocks'.*/symbol/(.*)\" title=")

										findPatTicker = re.findall(patFinderTicker, source)

										try:

											end_date = a_date + datetime.timedelta(days=1)

											value = Share(findPatTicker[0])

											initial_stock_value = value.get_historical(str(a_date), str(end_date))

											initial_stock_value = initial_stock_value[0]['Adj_Close']

										except:
											initial_stock_value = "NA"

										try:

											try:

												value = Share(findPatTicker[0])

											except:
												print "no value!!!!!!!!!!!!!"

											#current_stock_value = value.get_price()

											try:

												end_date1 = a_date + datetime.timedelta(days=1)
												end_date5 = a_date + datetime.timedelta(days=5)
												end_date10 = a_date + datetime.timedelta(days=10)
												end_date30 = a_date + datetime.timedelta(days=30)
												end_date90 = a_date + datetime.timedelta(days=90)

												current_stock_value1 = value.get_historical(str(a_date), str(end_date1))[0]['Adj_Close']
												current_stock_value5 = value.get_historical(str(a_date), str(end_date5))[0]['Adj_Close']
												current_stock_value10 = value.get_historical(str(a_date), str(end_date10))[0]['Adj_Close']
												current_stock_value30 = value.get_historical(str(a_date), str(end_date30))[0]['Adj_Close']
												current_stock_value90 = value.get_historical(str(a_date), str(end_date90))[0]['Adj_Close']

											except:
												print "not working!!!!!!!!!!!!!"


											try:

												end_date1 = end_date1.strftime("%m-%d-%Y")
												print "yoooooo", end_date1

												row1 = sp500_df[(sp500_df.index == str(end_date1))]
												sp500_value1 = float(row1["Adjusted Close"])

												print "1", sp500_value1

											except:
												end_date1 = end_date1 - datetime.timedelta(days=3)
												print "Except end_date1", end_date1
												row1 = sp500_df[(sp500_df.index == str(end_date1))]
												sp500_value1 = float(row1["Adjusted Close"])

											try:
												print end_date5

												row5 = sp500_df[(sp500_df.index == str(end_date5))]
												sp500_value5 = float(row5["Adjusted Close"])

												print "5", sp500_value5

											except:
												end_date5 = end_date5 - datetime.timedelta(days=3)
												print "Except end_date5", end_date5
												row5 = sp500_df[(sp500_df.index == str(end_date5))]
												#print "row5!!!!", row5
												sp500_value5 = float(row5["Adjusted Close"])
												print "sp500_5!!!!", sp500_value5

											try:

												print "end_date10!!!!!", end_date10

												row10 = sp500_df[(sp500_df.index == str(end_date10))]
												sp500_value10 = float(row10["Adjusted Close"])

												print "10", sp500_value10

											except:
												end_date10 = end_date10 - datetime.timedelta(days=3)
												print "Except end_date10", end_date10
												row10 = sp500_df[(sp500_df.index == str(end_date10))]
												sp500_value10 = float(row10["Adjusted Close"])

											try:

												row30 = sp500_df[(sp500_df.index == str(end_date30))]
												sp500_value30 = float(row30["Adjusted Close"])

												print '30', sp500_value30

											except:
												end_date30 = end_date30 - datetime.timedelta(days=3)
												print "Except end_date30", end_date30
												row30 = sp500_df[(sp500_df.index == str(end_date30))]
												sp500_value30 = float(row30["Adjusted Close"])

											try:

												row90 = sp500_df[(sp500_df.index == str(end_date90))]
												sp500_value90 = float(row90["Adjusted Close"])

												print '90', sp500_value90

											except:
												end_date90 = end_date90 - datetime.timedelta(days=3)
												print "Except end_date90", end_date90
												row90 = sp500_df[(sp500_df.index == str(end_date90))]
												sp500_value90 = float(row90["Adjusted Close"])

										except:
											print "this sucks!!!!"
											current_stock_value1 = 'NA'
											current_stock_value5 = 'NA'
											current_stock_value10 = 'NA'
											current_stock_value30 = 'NA'
											current_stock_value90 = 'NA'


											sp500_value1 = "NA"
											sp500_value5 = "NA"
											sp500_value10 = "NA"
											sp500_value30 = "NA"
											sp500_value90 = "NA"


									except:
										findPatTicker = ["NA"]


									try:

										patFinderDisclosure = re.compile("<strong>Disclosure: </strong>The author (.*) <span")

										findPatDisclosure = re.findall(patFinderDisclosure, source)

										#print findPatDisclosure

										if "long" in findPatDisclosure[0]:
											#print "long"
											direction = "long"
										elif "short" in findPatDisclosure[0]:
											#print "short"
											direction = "short"
										elif "no position" in findPatDisclosure[0]:
											#print "no position"
											direction = "no position"
									except:
										direction = "NA"

									try:

										patFinderMCap = re.compile('primaryMarketCap = (.*);')

										findPatMCap = re.findall(patFinderMCap, source)

									except:
										findPatMCap = "NA"

									'''
									try:
										patFindPopular = re.compile('<meta name="twitter:site" content="@sa_(.*)">')
										findPatPopular = re.findall(patFindPopular, source)
										if findPatPopular[0] == "popular":
											findPatPopular = "Popular"
										else:
											findPatPopular = "Not Popular"

									except:
										findPatPopular = "NA"
									'''
									try:
										patFindFollowers = re.compile("class='follow_clicks_author'>(.*)</span>")
										findPatFollowers = re.findall(patFindFollowers, source)

									except:
										findPatFollowers = ["NA"]

									try:
										patFindEditor = re.compile('<meta name="news_keywords" content="(.*) Picks"')
										findPatEditor = re.findall(patFindEditor, source)
										if "Editors'" in str(findPatEditor):
											findPatEditor = "Editors Pick"
										else:
											findPatEditor = "Regular"
									except:
										findPatEditor = "NA"

									try:
										df = df.append({'Date': str(findPatDate[0]), 'Ticker': str(findPatTicker[0]), 'Title': str(findPatTitle[0]), 'Direction': direction, 'Market Cap': str(findPatMCap[0]), 'Editor-Picks': findPatEditor, 'Author-Followers': findPatFollowers[0], 'Initial-Stock-Price': str(initial_stock_value), 'Current-Stock-Price1': str(current_stock_value1), 'Current-Stock-Price5': str(current_stock_value5), 'Current-Stock-Price10': str(current_stock_value10), 'Current-Stock-Price30': str(current_stock_value30), 'Current-Stock-Price90': str(current_stock_value90), 'sp500-Price1': str(sp500_value1), 'sp500-Price5': str(sp500_value5), 'sp500-Price10': str(sp500_value10), 'sp500-Price30': str(sp500_value30), 'sp500-Price90': str(sp500_value90)}, ignore_index=True)

									except Exception as e:
										print "DF Error!", e
										pass

								except Exception as e:
									print "Source Error", e

						except Exception as e:
							print "omg!", e
							pass

				except Exception as e:
					print "What!!", e
					pass

			except Exception as e:
				print "No Pattern", e
				pass

		except Exception as e:
			print 'No Webpage', e
			pass

		df.to_csv("seeking_alpha_stats.csv")

pull_data()
