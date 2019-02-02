# WebCrawl
# by TeeJ
# 01-26-2019

# Goal: The purpose of this program is to exploit the internet by grabbing data.
# I aim to run this throughout the day on my Raspberry Pi and collect pricing
# data on items that I am interested in. For fun.

# in order to run this script please type the following
# > python3 amznscrape.py "Data Science"
# note: "Data Science" can be replaced with any item you would like to scrape amazon with


# import packages
from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
import time
import sys
import datetime as dt

# QA parameters
search_word = "Data Science"
site = "https://www.amazon.com/s/ref=nb_sb_noss_2?url=search--alias%3Daps&field-keywords=Data+Science&rh=i%3Aaps%2Ck%3AData+Science"
site = 'https://www.amazon.com/s/ref=sr_pg_3?rh=i%3Aaps%2Ck%3AData+Science&page=3&keywords=Data+Science&ie=UTF8&qid=1548565321'


# Code Below
def main():
	'''
	type >sudo python3 amznscrape.py {search_word}
	to kick off program
	output: file in data/ directory
	'''
	# invoke header
	print('~|~|~|'*10)
	print('><> '*4 + 'Running Amznscrape by TeeJ' + ' <><'*4)
	print('~|~|~|'*10)

	# establish search word
	search_word = sys.argv[1]
	final = scrape_amzn(search_word, tries=int(sys.argv[2]))
	print(final)

	# output as csv
	final.to_csv('data/' + search_word.replace(" ", "_").lower()+'_amznscrape_' + str(dt.date.today()) + '.csv') 

	print()
	print('Results...')
	print(final[['Name', 'Paperback', 'Price']][final.notnull()])

	# prompt everything worked
	print('~|~|~|'*10)
	print("Successfully ran!")
	print('~|~|~|'*10)

def scrape_amzn(search_word, page=1, df=pd.DataFrame(columns = ['Name', 'Price','Recorded_On','Search_Word', 'Link']), tries=100):
	'''
	input: search_word, page, dataframe
	output: dataframe [Name, Price, Link] of amzn search
	'''
	print() # blank line for sanity
	# establish link
	if not page-1:
		site = "https://www.amazon.com/s/ref=nb_sb_noss_2?url=search--alias%3Daps&field-keywords=" + search_word.replace(" ", "+") + "&rh=i%3Aaps%2Ck%3A" + search_word.replace(" ", "+") 
	else:
		print("Going to page " + str(page) + "...")
		site = 'https://www.amazon.com/s/ref=sr_pg_' + str(page) + '?rh=i%3Aaps%2Ck%3A' + search_word.replace(" ","+") + '&page=' + str(page) + '&keywords=' + search_word.replace(" ","+") + '&ie=UTF8' 

	# extract data from the site
	html = requests.get(site).text
	soup = BeautifulSoup(html, 'html5lib')

	# search for results
	print('Scraping ' + site + ' for data...')
	scrape = soup.find_all('div', id=re.compile('result'))
	#print('The html code has been successfully downloaded...')

	# filter down results
	result = []
	for div in scrape:
		result.extend(div.find_all('a' , {'class': re.compile('.*.')})) # '.a*normal*.'	

	print('Parsing the data from the webscrape for the amount and link of the item...')

	# create dataframe
	# df = pd.DataFrame(columns=['Name','Price', 'Link'])
	df_old = df
	# add data to the data frame
	for line in result:
		if line.find_all('span', {'class':'a-offscreen'}) and line.text.split()[0][:4] != "from":
			try:
				skip_dict = skip_scrape(line['href'], tries = int(sys.argv[2]))
			except:
				print()
				print("!!	Skip Scrape Failed	!!")
				print(line['href'])
				print('The format of the html site does not match the data we are scraping for.')
				print()
				skip_dict = {'Failed SS': 'True'}
			df = df.append({ 'Name': line['href'].split('/')[3] # update the name by splitting the link
					,'Price': line.text.split()[0] # update the price
					,'Recorded_On' :str(dt.date.today())
					,'Search_Word' :search_word
					,'Link':line['href']
					, **skip_dict
					}, ignore_index=True)
	# print off data frame
	if len(df_old.index) == len(df.index):
		if tries: # retry on error (sometimes connection ends recursion)
			print('Something went wrong! Retrying ' + str(tries) + ' more times...')
			time.sleep(5)
			return(scrape_amzn(search_word,page,df, tries-1))
		else:
			time.sleep(5)
			return(df)
	else:
		print('Waiting to search for next web page...')
		for i in range(4): print('+++++++++++++++++++++++++++++++++++++++++++++')
		time.sleep(5)
		return(scrape_amzn(search_word, page+1, df))



def skip_scrape(site, tries=100):
	'''
	Input: Site and number of tries
	Output: Dictionary with more data
	'''
	# QA Inputs:
	#filepath = 'data/data_science_amzn_scrape_2019-01-29.csv'
	#df = pd.read_csv(filepath)
	#site = df['Link'][0]
	print('Attempting to find more data through a skip scrape for the following site:')
	print(site)

	result = []
	i = 0
	# pull site for specified number of tries {potential failed connection}
	while result == []:
		print()
		print("Skip scrape try " + str(i+1))
		# extract data from the site
		html = requests.get(site).text
		soup = BeautifulSoup(html, 'html5lib')
		# print(soup)
		# search for results
		print('Skip Scraping ' + site + ' for data...')
		scrape = soup.find_all('div', {'class': "content"})
		#print('The html code has been successfully downloaded...')

		# filter down results

		for div in scrape:
			result.extend(div.find_all('li'))
		i = i + 1
		if i == tries:
			print()
			print("!! XXXXXXXXXXXXXXXXXXXXX - ERROR - XXXXXXXXXXXXXXXXXXXXX !!")
			print("Unable to grab data for " + str(site))
			break
		#print(result)
		time.sleep(5)

	# pull in the extra data
	data = {'Link': site}
	for i in range(5):
		# clean the data
		item = str(result[i]).replace('<li><b>', '').replace('</li>', '').split("</b> ")
		data[item[0][:-1]] = item[1]
	print("The additional data has been added by skip scrape:")
	print(data)
	print()
	return(data)
	# print('Parsing the data from the webscrape for the amount and link of the item...')
	# add newly found data to data table
	#df = pd.DataFrame()
	#df = df.append(data, ignore_index=True)
	#print(df)
#skip_scrape('dummy', 12) #test script: SUCCESS

# Execute Script Here
main()
