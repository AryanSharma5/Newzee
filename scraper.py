from bs4 import BeautifulSoup
import requests
from utils import urls
import pandas as pd
import os

class Scraper():
	'''
	Scrapes google news site for latest news headlines along 
	with their category.
	'''
	def __init__(self):	

		self.df = pd.DataFrame(columns = ['news', 'category'])
		print('-'*70)
		print('Scraper initialisation successfull !!')
		print('-'*70)

	def scrape(self, category, sub_category):

		'''
		method name : scrape
		params : category :- takes in string, which denotes
							 category out of {business, 
							 technology, sports, science, health,
							 entertainment.}
				 sub_category :- takes in string, which denotes
				 				sub category of the category. e.g.,
				 				mobile is sub category for category.
		rtype : None
		'''

		page = requests.get(urls[category][sub_category]).text
		soup = BeautifulSoup(page, 'html.parser')
		ROIs = soup.find('div', {'class' : 'lBwEZb BL5WZb GndZbb',
											'jsname' : 'esK7Lc'})
		jscontrollers = ROIs.findAll('div', {'jscontroller' : 'd0DtYd',
														'jsmodel' : 'DLq0be hT8rr'})
		jslogs = ROIs.findAll('div', {'class' : 'NiLAwe y6IFtc R7GTQ keNKEd j7vNaf nID9nc',
											'jslog' : '93789'})
		articles = []
		for i in range(len(jscontrollers)):
			articles.append(jscontrollers[i].find('div', {'jsname' : 'gKDw6b',
															'class' : 'xrnccd F6Welf R7GTQ keNKEd j7vNaf'}).article.h3.a.text)
		for i in range(len(jslogs)):
			articles.append(jslogs[i].find('div', {'class' : 'xrnccd'}).article.h3.a.text)
		self.store_results(articles, category, sub_category)

	def store_results(self, articles, category, sub_category):
		self.df['news'] = articles
		self.df['category'] = [category]*len(articles)
		print('saving results....')
		if not os.path.isdir('data'):
			os.mkdir('data/')
		self.df.to_csv(f'data/{category}_{sub_category}.csv', index = False)
		print(f'{category}_{sub_category}.csv saved in data folder !!')


CATEGORIES = urls.keys()

for category in CATEGORIES:
	SUB_CATEGORIES = urls[category].keys()
	for sub_category in SUB_CATEGORIES:
		scraper = Scraper()
		print(f'scraping data for category {category} with {sub_category} sub category !!')
		scraper.scrape(category, sub_category)
		print(f'data has been scraped successfully for {category} with {sub_category} sub category !!')

print('scraping done !!')