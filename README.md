# A Guide for Crawling the Web with Python
by TeeJ

## Introduction

Sometimes the easiest way to gather data is scraping the web! 

## Scraping Amazon

Lucky for you I have built some semi-professional (a lot of improvements can be made) scripts that scrape the data from searches on amazon. In order to scrape Amazon for all "Playstation3" search results then follow the shell commands below:
```shell
# setup environment (only need to be ran once)
sudo git clone "https://github.com/teejl/webscrape_guide.git"
cd webscrape_guide
sudo chmod u+x webscrape.init
./webscrape.init

# run search (can run after init for different items)
sudo python3 amznscrape.py "Data Science" 10
```
The raspberry pi will scrape for the results found from a "Data Science" search result on Amazon (retrying 10 times if a connection to the html file from the website cannot be established) and save the results in the data folder.

# Automating many searches:
```shell
sudo chmod u+x data.load
sudo nano data.load # add the searches you want to find
./data.load
```
