import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = [
        'http://quotes.toscrape.com/page/1/',
    ]

    def parse(self, response):
        for quote in response.css('div.quote'):
           
            text = quote.css('span.text::text').extract_first()
            author = quote.css('span small::text').extract_first()
            tags = quote.css('div.tags a.tag::text').extract()
            
            if "Albert Einstein" not in author:
                yield {
                    'text': None,
                    'author': None,
                    'tags': None,
                }
            
            else :
                yield {
                    'text':text, 
                    'author':author, 
                    'tags' :tags
                }
            
        next_page = response.css('li.next a::attr(href)').extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)