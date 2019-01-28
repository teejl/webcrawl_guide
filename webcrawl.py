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

# establish variables
# site = "http://www.example.com"
# site = "https://www.amazon.com"
# site = "https://www.pandora.com"

# simple example


search_word = "Data Science"

# boss battle 
site = "https://www.amazon.com/s/ref=nb_sb_noss_2?url=search--alias%3Daps&field-keywords=Data+Science&rh=i%3Aaps%2Ck%3AData+Science"
#site = 'https://www.amazon.com/s/ref=sr_pg_2?rh=i%3Aaps%2Ck%3AData+Science&page=2&keywords=Data+Science&ie=UTF8&qid=1548564295' 
#site = 'https://www.amazon.com/s/ref=sr_pg_3?rh=i%3Aaps%2Ck%3AData+Science&page=3&keywords=Data+Science&ie=UTF8&qid=1548565321'
# then hypothetically it would repeat for the rest of the 20 pages
site = "https://www.amazon.com/s/ref=nb_sb_noss_2?url=search--alias%3Daps&field-keywords=" + search_word.replace(" ", "+") + "&rh=i%3Aaps%2Ck%3A" + search_word.replace(" ", "+") 

# extract data from the site
html = requests.get(site).text
soup = BeautifulSoup(html, 'html5lib')

# find out more about what soup really is
# print(type(soup))
# print(soup.find_all('div', id=re.compile ('result'))) # bs4.element.resultset
# print(type(soup.select('div[id^=result]'))) # list

# let us try this once more
print('Scraping ' + site + ' for data...')
scrape = soup.find_all('div', id=re.compile('result'))
print('The website scraping was a success!')

result = []
#result2 = []
#result3 = []
#result4 = []
for div in scrape:
	result.extend(div.find_all('a', {'class': re.compile('.*a*normal*.')}))	
	#result.extend(div.find_all('a', {'class': "a-link-normal a-text-normal"}))
	#
	#result2.extend(div.find_all('a', {'class': re.compile('*a-text-normal*')}))
	#result3.extend(link['href'] for link in div.findAll('a', href=re.compile('www.amazon.com/'))) # all the links
	#result4.extend(div.find_all('span', {'class': 'a-offscreen'})) # find price
#print(result)

print()
print('Parsing the data from the webscrape for the amount and link of the item...')
i = 1
for line in result:
	if line.find_all('span', {'class':'a-offscreen'}) and line.text.split()[0][:4] != "from":
		print('Item: ' + str(i))
		print('Price: ', line.text.split()[0])
		print('Link: ',  line['href'])
		#for i in range(4):
		print ("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
		i = i + 1
# print(result3) links (a lot of redundant links)
# print(result4) prices (i am not sure if i grabbed them all)

# lets try to grab specifics
#print(soup.find('p', {'Data Science'})) # find all <p> {text} </p>
#print(soup.div.p.text.split()) # turn p into a list
#print(soup.p.get('id'))
#print(soup('p'))

# prompt everything worked
print("Successfully ran!")

# lets dig into another webpage huh?
#site = "https://www.amazon.com/What-Data-Science-Mike-Loukides-ebook/dp/B007R8BHAK"
#html = requests.get(site).text
#soup = BeautifulSoup(html, 'html5lib')
#scrape = soup.find_all('div')
#print(soup)

