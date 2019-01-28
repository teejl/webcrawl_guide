# WebCrawl
# by TeeJ
# 01-26-2019

# Goal: The purpose of this program is to exploit the internet by grabbing data.
# I aim to run this throughout the day on my Raspberry Pi and collect pricing
# data on items that I am interested in. For fun.

# import packages
from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
import time

# establish variables
# site = "http://www.example.com"
# site = "https://www.amazon.com"
# site = "https://www.pandora.com"

# simple example


search_word = "Data Science"

# boss battle 
site = "https://www.amazon.com/s/ref=nb_sb_noss_2?url=search--alias%3Daps&field-keywords=Data+Science&rh=i%3Aaps%2Ck%3AData+Science"
#site = 'https://www.amazon.com/s/ref=sr_pg_3?rh=i%3Aaps%2Ck%3AData+Science&page=3&keywords=Data+Science&ie=UTF8&qid=1548565321'
# then hypothetically it would repeat for the rest of the 20 pages
# program 1 run here input: link, dataframe; output: dataframe
def scrape_amzn(search_word, page=1, df=pd.DataFrame(columns = ['Name', 'Price', 'Link']), tries=3):
	'''
	input: search_word, page, dataframe
	output: dataframe
	'''
	# establish link
	if not page-1:
		site = "https://www.amazon.com/s/ref=nb_sb_noss_2?url=search--alias%3Daps&field-keywords=" + search_word.replace(" ", "+") + "&rh=i%3Aaps%2Ck%3A" + search_word.replace(" ", "+") 
	else:
		print("Going to page " + str(page) + "...")
		site = 'https://www.amazon.com/s/ref=sr_pg_' + str(page) + '?rh=i%3Aaps%2Ck%3A' + search_word + '&page=' + str(page) + '&keywords=' + search_word + '&ie=UTF8' 

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
					,'Link':line['href']}, ignore_index=True) # update the link
	# print off data frame
	if len(df_old.index) == len(df.index):
		if tries:
			print('Something went wrong! Retrying ' + str(tries) + ' more times...')
			return(scrape_amzn(search_word,page,df, tries-1))
		else:
			return(df)
	else:
		print('Waiting to search for next web page...')
		time.sleep(15)
		return(scrape_amzn(search_word, page+1, df))

# establish search word
search_word = "Data Science"
final = scrape_amzn(search_word)
print(final)

# output as csv
final.to_csv('data/' + search_word.replace(" ", "_").lower()+'_amzn_scrape.csv') 

# prompt everything worked
print("Successfully ran!")
