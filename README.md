# A Guide for Crawling the Web with Python
by TeeJ

## Introduction

Sometimes the easiest way to gather data is scraping the web! 

## Scraping Amazon

Lucky for you I have built some semi-professional (a lot of improvements can be made I'm sure) scripts that scrape the data from searches on amazon. In order to scrape Amazon for all "Playstation3" search results then follow the shell commands below:
```shell
# setup environment (only need to be ran once)
sudo git clone "https://github.com/teejl/webscrape_guide.git"
cd webscrape_guide
sudo chmod u+x webscrape.init

# run search (can run after init for different items)
sudo python3 amznscrape.py "Playstation3"
```
The raspberry pi will scrape for the results found form a "Playstation3" search result on Amazon and save the results in the data folder.
