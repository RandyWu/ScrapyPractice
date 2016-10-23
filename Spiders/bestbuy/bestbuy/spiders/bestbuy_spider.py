import scrapy

searchItem = str(raw_input("What are you looking for?: "))

class bestbuySpider(scrapy.Spider):
	name = "bestbuy"
	start_urls = ['http://www.bestbuy.ca/Search/SearchResults.aspx?path=ca77b9b4beca91fe414314b86bb581f8en20&query=%s' % (searchItem)
	]

	def parse(self, response):

		for products in response.xpath('//div[@class="item-inner clearfix"]'):
			yield {
				'Title' : products.xpath('./div[@class="prod-info"]//h4[@class="prod-title"]/a/text()').extract_first(),
				'Price': products.xpath('./div[@class="prod-info"]//span[@class="amount"]/text()').extract_first(),
			}

#How it works now:
#Make the starting url http://www.bestbuy.ca/Search/SearchResults.aspx?type=product&page=1&sortBy=relevance&sortDir=desc&query=searchItem
#This is the easiest, but doesn't account for search redirects.

#How I want it to work
#Find a way to input text into the search box and search
#retrieve the URL, and have the resulting URL be the spider start_url