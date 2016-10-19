import scrapy

class KijijiSpider(scrapy.Spider):
	name = "kijiji"
	start_urls = ['http://www.kijiji.ca/b-jobs/ottawa/c45l1700185',
	]

	def parse(self, response):
    	
		for job in response.xpath('//td[@class="description"]'):

			Link = job.xpath('./a/@href').extract_first() #In case of non kijiji job sites
			if '/v' in Link:
				yield {
					'Job': job.xpath('normalize-space(./a/text())').extract_first(),
					'Link': "http://www.kijiji.ca" + Link, #Kijiji gives partial urls, so the first half of the yeild url is hard coded
				}
			else:
				yield {
					'Job': job.xpath('normalize-space(./a/text())').extract_first(),
					'Link': Link,
				}
		
		next_page = response.xpath('//div[@class="pagination"]/a[@title = "Next"]/@href').extract_first()
		if next_page is not None:
			next_page = response.urljoin(next_page)
			yield scrapy.Request(next_page, callback=self.parse)
