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

# tested with below parameters
search_word = "Data Science"
site = "https://www.amazon.com/s/ref=nb_sb_noss_2?url=search--alias%3Daps&field-keywords=Data+Science&rh=i%3Aaps%2Ck%3AData+Science"
site = 'https://www.amazon.com/s/ref=sr_pg_3?rh=i%3Aaps%2Ck%3AData+Science&page=3&keywords=Data+Science&ie=UTF8&qid=1548565321'


def scrape_amzn(search_word, page=1, df=pd.DataFrame(columns = ['Name', 'Price','Recorded_On','Search_Word', 'Link']), tries=20):
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
	print('The html code has been successfully downloaded...')

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
			df = df.append({ 'Name': line['href'].split('/')[3] # update the name by splitting the link
					,'Price': line.text.split()[0] # update the price
					,'Recorded_On' :str(dt.date.today())
					,'Search_Word' :search_word
					,'Link':line['href']
					}, ignore_index=True)
	# print off data frame
	if len(df_old.index) == len(df.index):
		if tries: # retry on error (sometimes connection ends recursion)
			print('Something went wrong! Retrying ' + str(tries) + ' more times...')
			time.sleep(20)
			return(scrape_amzn(search_word,page,df, tries-1))
		else:
			time.sleep(20)
			return(df)
	else:
		print('Waiting to search for next web page...')
		for i in range(4): print('+++++++++++++++++++++++++++++++++++++++++++++')
		time.sleep(45)
		return(scrape_amzn(search_word, page+1, df))



def main():
	# establish search word
	search_word = sys.argv[1]
	final = scrape_amzn(search_word)
	print(final)

	# output as csv
	final.to_csv('data/' + search_word.replace(" ", "_").lower()+'_amznscrape_' + str(dt.date.today()) + '.csv') 

	# prompt everything worked
	print("Successfully ran!")

def test():
	# read file
	filepath = 'data/data_science_amzn_scrape_2019-01-29.csv'
	df = pd.read_csv(filepath)

	# loop through "Link" column
	#for site in df['Link']:
		#print (site)
	# dummy initial condition to continue algo
	site = df['Link'][0]
	print(site)

	# extract data from the site
	html = requests.get(site).text
	soup = BeautifulSoup(html, 'html5lib')

	# search for results
	print('Scraping ' + site + ' for data...')
	scrape = soup.find_all('div', {'class': "content"})
	print('The html code has been successfully downloaded...')
	#print(scrape)
	# filter down results
	result = []

	for div in scrape:
		result.extend(div.find_all('li')) # , {'class': re.compile('.*.')})) # '.a*normal*.'
	# print(result[:7])

	# WATCH OUT FOR WHENEVER RESULTS RETURNS [] MIGHT NEED TO RETRY A COUPLE TIMES AS A SAFEGAURD!!!!

	# generate more data
	data = {'Link': site}
	for i in range(5):
		# clean the data
		item = str(result[i]).replace('<li><b>', '').replace('</li>', '').split("</b> ")
		data[item[0][:-1]] = item[1]
	print(data)
	# print('Parsing the data from the webscrape for the amount and link of the item...')
	# add newly found data to data table
	df = pd.DataFrame()
	df = df.append(data, ignore_index=True)
	print(df)

test()
