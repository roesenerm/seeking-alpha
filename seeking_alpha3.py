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

	df = pd.DataFrame(columns = ['Date', 'Ticker', 'Title', 'Direction', 'Direction_Num', 'Market Cap', 'Editor-Picks', 'Author-Followers', 'Initial-Stock-Price', 'Current-Stock-Price10', 'Current-Stock-Price30', 'Current-Stock-Price90', 'sp500-Price10', 'sp500-Price30', 'sp500-Price90', 'stock_change10', 'stock_change30', 'stock_change90', 'sp500_change10', 'sp500_change30', 'sp500_change90', 'difference10', 'difference30', 'difference90', 'status10', 'status30', 'status90'])

	sp500_df = pd.DataFrame.from_csv("YAHOO-INDEX_GSPC.csv")

	d1 = date(2014, 1, 1)
	d2 = date(2014, 12, 31)

	delta = d2 - d1

	value_list = []

	for i in range(delta.days + 1):
		a_date = d1 + td(days=i)
		#print a_date
		article_date = a_date.strftime("%Y/%m/%d")
		#print article_date
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
								#print link

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

										#print findPatTicker

										findPatTicker = str(findPatTicker[0])

										#print findPatTicker

										try:

											try:

												value = Share(findPatTicker)

											except:
												print "no value!!!!!!!!!!!!!"

											try:

												end_date = a_date + datetime.timedelta(days=1)

												value = Share(findPatTicker)


												initial_stock_value = value.get_historical(str(a_date), str(end_date))

												#print "Value Historical:", initial_stock_value

												initial_stock_value = initial_stock_value[0]['Adj_Close']

												#print "Initial Stock Value: ", initial_stock_value

												try:

													row = sp500_df[(sp500_df.index == str(end_date))]
													initial_sp500_value = float(row["Adjusted Close"])

													#print "sp500 Value", sp500_value

												except:
													end_date = end_date - datetime.timedelta(days=3)
													#print "Except end_date", end_date
													row = sp500_df[(sp500_df.index == str(end_date))]
													initial_sp500_value = float(row["Adjusted Close"])

												try:

													end_date10 = a_date + datetime.timedelta(days=10)
													end_date30 = a_date + datetime.timedelta(days=30)
													end_date90 = a_date + datetime.timedelta(days=90)

													current_stock_value10 = value.get_historical(str(a_date), str(end_date10))[0]['Adj_Close']
													current_stock_value30 = value.get_historical(str(a_date), str(end_date30))[0]['Adj_Close']
													current_stock_value90 = value.get_historical(str(a_date), str(end_date90))[0]['Adj_Close']

													try:
														#print "okay?"
														stock_change10 = ((float(current_stock_value10) - float(initial_stock_value)) / float(initial_stock_value)) * 100
														stock_change30 = ((float(current_stock_value30) - float(initial_stock_value)) / float(initial_stock_value)) * 100
														stock_change90 = ((float(current_stock_value90) - float(initial_stock_value)) / float(initial_stock_value)) * 100
														#print "yes"

													except:
														stock_change10 = "NA"
														stock_change30 = "NA"
														stock_change90 = "NA"

												except:
													print "no current stock value!!!!!!!!!!!!!"
													pass


												try:

													row10 = sp500_df[(sp500_df.index == str(end_date10))]
													sp500_value10 = float(row10["Adjusted Close"])

													sp500_change10 = ((float(sp500_value10) - float(initial_sp500_value)) / float(initial_sp500_value)) * 100

													#print "10", sp500_value10

												except:
													end_date10 = end_date10 - datetime.timedelta(days=3)
													#print "Except end_date10", end_date10
													row10 = sp500_df[(sp500_df.index == str(end_date10))]
													sp500_value10 = float(row10["Adjusted Close"])

													sp500_change10 = ((float(sp500_value10) - float(initial_sp500_value)) / float(initial_sp500_value)) * 100

												try:

													row30 = sp500_df[(sp500_df.index == str(end_date30))]
													sp500_value30 = float(row30["Adjusted Close"])

													sp500_change30 = ((float(sp500_value30) - float(initial_sp500_value)) / float(initial_sp500_value)) * 100

													#print '30', sp500_value30

												except:
													end_date30 = end_date30 - datetime.timedelta(days=3)
													#print "Except end_date30", end_date30
													row30 = sp500_df[(sp500_df.index == str(end_date30))]
													sp500_value30 = float(row30["Adjusted Close"])

													sp500_change30 = ((float(sp500_value30) - float(initial_sp500_value)) / float(initial_sp500_value)) * 100

												try:

													row90 = sp500_df[(sp500_df.index == str(end_date90))]
													sp500_value90 = float(row90["Adjusted Close"])

													sp500_change90 = ((float(sp500_value90) - float(initial_sp500_value)) / float(initial_sp500_value)) * 100

													#print '90', sp500_value90

												except:
													end_date90 = end_date90 - datetime.timedelta(days=3)
													#print "Except end_date90", end_date90
													row90 = sp500_df[(sp500_df.index == str(end_date90))]
													sp500_value90 = float(row90["Adjusted Close"])

													sp500_change90 = ((float(sp500_value90) - float(initial_sp500_value)) / float(initial_sp500_value)) * 100

												try:

													try:

														patFinderDisclosure = re.compile("<strong>Disclosure: </strong>(.*) <span")

														findPatDisclosure = re.findall(patFinderDisclosure, source)

														if "long" in findPatDisclosure[0]:
															#print "long"
															direction = "long"
															direction_num = 1
														elif "short" in findPatDisclosure[0]:
															#print "short"
															direction = "short"
															direction_num = 2
														elif "no position" or "no positions" in findPatDisclosure[0]:
															#print "no position"
															direction = "no position"
															direction_num = 3

													except:

														patFinderDisclosure = re.compile("<strong>Disclosure: </strong>(.*)</p>")

														findPatDisclosure = re.findall(patFinderDisclosure, source)

														if "long" in findPatDisclosure[0]:
															#print "long"
															direction = "long"
															direction_num = 1
														elif "short" in findPatDisclosure[0]:
															#print "short"
															direction = "short"
															direction_num = 2
														elif "no position" or "no positions" in findPatDisclosure[0]:
															#print "no position"
															direction = "no position"
															direction_num = 3


												except:
													print "not working?"
													direction = "NA"
													direction_num = 4

												try:

													patFinderMCap = re.compile('primaryMarketCap = (.*);')

													findPatMCap = re.findall(patFinderMCap, source)

												except:
													findPatMCap = "NA"

												try:
													patFindFollowers = re.compile("class='follow_clicks_author'>(.*)</span>")
													findPatFollowers = re.findall(patFindFollowers, source)

												except:
													findPatFollowers = ["NA"]

												try:
													patFindEditor = re.compile('<meta name="news_keywords" content="(.*) Picks"')
													findPatEditor = re.findall(patFindEditor, source)
													if "Editors'" in str(findPatEditor):
														findPatEditor = 1 #"Editor"
													else:
														findPatEditor = 2 #"Regular"
												except:
													findPatEditor = 3 #"NA"

												try:
													difference10 = stock_change10 - sp500_change10
													difference30 = stock_change30 - sp500_change30
													difference90 = stock_change90 - sp500_change90

													if difference10 > 5 and direction == "long":
														status10 = 1
													elif difference10 < 5 and direction == "short":
														status10 = 1
													elif difference10 > 5 and direction == "no position":
														status10 = 1
													elif difference10 > 5 and direction == "NA":
														status10 = 1
													else:
														status10 = 0

													if difference30 > 5 and direction == "long":
														status30 = 1
													elif difference30 < 5 and direction == "short":
														status30 = 1
													elif difference30 > 5 and direction == "no position":
														status30 = 1
													elif difference30 > 5 and direction == "NA":
														status30 = 1
													else:
														status30 = 0

													if difference90 > 5 and direction == "long":
														status90 = 1
													elif difference10 < 5 and direction == "short":
														status90 = 1
													elif difference90 > 5 and direction == "no position":
														status90 = 1
													elif difference90 > 5 and direction == "NA":
														status90 = 1
													else:
														status90 = 0

												except:
													pass

												try:
													tokenize = "test"

												except:
													pass

												try:
													df = df.append({'Date': str(findPatDate[0]), 'Ticker': findPatTicker, 'Title': str(findPatTitle[0]), 'Direction': direction, 'Direction_Num':direction_num, 'Market Cap': str(findPatMCap[0]), 'Editor-Picks': findPatEditor, 'Author-Followers': findPatFollowers[0], 'Initial-Stock-Price': str(initial_stock_value), 'Current-Stock-Price10': str(current_stock_value10), 'Current-Stock-Price30': str(current_stock_value30), 'Current-Stock-Price90': str(current_stock_value90), 'sp500-Price10': str(sp500_value10), 'sp500-Price30': str(sp500_value30), 'sp500-Price90': str(sp500_value90), 'stock_change10': stock_change10, 'stock_change30': stock_change30, 'stock_change90': stock_change90, 'sp500_change10': sp500_change10, 'sp500_change30':sp500_change30, 'sp500_change90': sp500_change90, 'difference10':difference10, 'difference30':difference30, 'difference90':difference90, 'status10':status10, 'status30':status30, 'status90':status90}, ignore_index=True)

													print "Complete DF"

												except Exception as e:
													print "DF Error!", e

													print 'Date', str(findPatDate[0])
													print 'Ticker', str(findPatTicker[0])
													print 'Title', str(findPatTitle[0])
													print 'Direction', direction
													print 'Market Cap', str(findPatMCap[0])
													print 'Editor-Picks', findPatEditor
													print 'Author-Followers', findPatFollowers[0]
													print 'Initial-Stock-Price', str(initial_stock_value)
													print 'Current-Stock-Price10', str(current_stock_value10)
													print 'Current-Stock-Price30', str(current_stock_value30)
													print 'Current-Stock-Price90', str(current_stock_value90)
													print 'sp500-Price10', str(sp500_value10)
													print 'sp500-Price30', str(sp500_value30)
													print 'sp500-Price90', str(sp500_value90)
													print 'stock_change10', stock_change10
													print 'stock_change30', stock_change30
													print 'stock_change90', stock_change90
													print "Error Complete"
													pass


											except Exception as e:
												print "No Initial Stock Value", e

										except:
											print "NA everything"

									except:
										print "No Ticker"
										pass


								except Exception as e:
									print "Source Error", e
									pass

						except Exception as e:
							print "No Link", e
							pass

				except Exception as e:
					print "No item in Link Pattern", e
					pass

			except Exception as e:
				print "No Pattern", e
				pass

		except Exception as e:
			print 'No Webpage', e
			pass

		df.to_csv("seeking_alpha_stats_enhanced2.csv")

	print "Complete File"

pull_data()