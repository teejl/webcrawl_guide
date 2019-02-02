# Explore Data
# by TeeJ

# the purpose of this program is to explore the data I have been collecting via beautifulsoup4 (amazon)

# import packages
import pandas as pd
import glob
import os

# set variables

# import data
# print('Reading file ' + 'data/' + search_word.replace(" ", "_").lower() + '_amzn_scrape_2019-01.29.csv ...')
# df = pd.read_csv('data/' + search_word.replace(" ", "_").lower() + '_amzn_scrape_2019-01-29.csv')

# join data together
def join_data(filepath='data'):
	'''
	input: filepath
	output: pandas dataframe of all csv files unioned together
	'''
	print() # blank line for sanity
	# define the path of all the files
	print("Looking for all of the files in the directory " + os.path.join(filepath) + " ...")
	all_files = glob.glob(os.path.join(filepath, '*.csv'))
	print("Joining all of the csv files together...")
	df = pd.concat((pd.read_csv(f) for f in all_files), ignore_index = True)

	# df.to_csv('dummy.csv') # saving the results to a specific file
	return(df)

df = join_data()
#print(df.dtypes)

# format the data
df['Price'] = df['Price'].str.replace(",", '').str.replace("Free", "$0.00").str[1:].astype(float) # convert price to a number
print(df)

#print(df['Price'].astype(str)[1:])
#print(df)


