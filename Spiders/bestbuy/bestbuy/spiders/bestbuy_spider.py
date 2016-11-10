import scrapy
import json
import requests


searchItem = str(raw_input("What are you looking for?: "))
QUERY_URL = 'http://www.bestbuy.ca/api/v2/json/search?lang=en&include=facets,resources,relatedcategories,relatedqueries,promotions,redirects&query='


class bestbuySpider(scrapy.Spider):
	name = "bestbuy"
	start_urls = [QUERY_URL + '%s&page=1&pageSize=32&sortBy=relevance&sortDir=desc' % (searchItem)]
	

	#TODO: Multiple Parse functions
	#def parse(self, response):
	#	for x in range (0,32):
			

	def parse(self, response):
		
		url = QUERY_URL + '%s&page=1&pageSize=32&sortBy=relevance&sortDir=desc' % (searchItem)

		requestsData = requests.get(url)

		totalPages = requestsData.json()['totalPages']
		pageNumber = requestsData.json()['currentPage']
		pageSize = requestsData.json()['pageSize']

		if pageNumber != 1:
			url = rl = QUERY_URL + '%s&page=%d1&pageSize=32&sortBy=relevance&sortDir=desc' % (searchItem,pageNumber)

		for items in range(0,pageSize):
			yield {
				'SKU' : requestsData.json()['products'][items]['sku'],
				'Title': requestsData.json()['products'][items]['name'],
				'Sale Price' : requestsData.json()['products'][items]['salePrice']
			}

		if pageNumber <= totalPages:
			yield Request()


#The rest of the URL %s&page=1&pageSize=32&sortBy=relevance&sortDir=desc' % (searchItem)

# r = requests.get('http://www.bestbuy.ca/api/v2/json/search?lang=en&include=facets,resources,relatedcategories,relatedqueries,promotions,redirects&query=burgers&page=2&pageSize=32&sortBy=relevance&sortDir=desc')
# q = r.json()['products'][parameter]