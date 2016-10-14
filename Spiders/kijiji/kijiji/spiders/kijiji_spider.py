import scrapy

class KijijiSpider(scrapy.Spider):
	name = "kijiji"
	start_urls = ['http://www.kijiji.ca/b-jobs/ottawa/c45l1700185',
	]

	def parse(self, response):
    	
		for job in response.xpath('//td[@class="description"]'):
            
			yield {
				'Job': job.xpath('normalize-space(./a/text())').extract_first(),
				'Link': job.xpath('./a/@href').extract_first(),
			}
		
		next_page = response.xpath('//*[@id="MainContainer"]/div[4]/div[2]/div/div[12]/div/a[10]/@href').extract_first()
		if next_page is not None:
			next_page = response.urljoin(next_page)
			yield scrapy.Request(next_page, callback=self.parse)