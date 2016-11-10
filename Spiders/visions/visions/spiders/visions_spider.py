import scrapy

class VisionsSpider(scrapy.Spider):
	name = "visions"
	start_urls = ['http://www.visions.ca/',]

	#Gathers links to the categories and yields the categories
	def parse(self, response):
		for category in response.xpath('//ul[@id="mastermenu-dropdown"]/li/a')[:-1]:
			yield {
				"Categories" : category.xpath('./span/text()').extract_first(),
			}

			category_url = category.xpath('./@href').extract_first()
			category_url = response.urljoin(category_url)

			yield scrapy.Request(category_url,callback=self.get_brand)

	#Takes category links, gathers the links to brand , yields url to brand page
	def get_brand(self, response):
		#import ipdb; ipdb.set_trace()
		brand_url = response.xpath('//div[@class="itembox-name"]/a/@href').extract_first()
		brand_url = response.urljoin(brand_url)
		
		yield scrapy.Request(brand_url,callback=self.get_item)

	#Takes brand links, gathers link to first product and price of product, yields price and product URL
	def get_item(self, response):
		item_url = response.xpath('//div[@class="contentright"]/h2/a/@href').extract_first()
		item_url = response.urljoin(item_url)
		
		#Gather the price here because of xpath difficulties with ctl00_ContentPlaceHolder1
		yield {"Product Price" : response.xpath('//div[@style="float:right;"]/span/text()').extract_first(),}
		yield scrapy.Request(item_url,callback=self.get_info)

	#Takes product URL, gathers product title, SKU, and availability, yields title, SKU, and availability
	def get_info(self, response):
		yield{
			"Product Title" : response.xpath('//div/h1/span/text()').extract()[0],
			"SKU" : response.xpath('//div/h1/span/text()').extract()[1],
		}

		if response.xpath('//div[@class="productresult-itembox"][1]//div[@style="float:right;"]/a').extract_first() != None :
			yield{
			"Product Availability" : "Available"
			}

#The Spider works, but for some reason the csv generator isn't working
#Also, all the products are not in order, I have no idea why
#Code is messy

#TODO:

#Implement item fields for easier data gathering
#Yield a whole finished product at the end
