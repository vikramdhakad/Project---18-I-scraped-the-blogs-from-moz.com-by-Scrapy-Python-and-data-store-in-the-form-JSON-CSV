import scrapy
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor


class ScraperSpider(scrapy.Spider):
    name = "scraper"
    allowed_domains = ["moz.com"]
    start_urls = ["https://moz.com/blog"]

    def parse(self, response):
       
        for pas in response.xpath("//h2[@class='h3 font-lato mb-2 mb-md-4']/a"):
            urls = pas.xpath("@href").get()
            yield response.follow(url=urls,callback=self.data_parser)
            
        for page in range(1,526):
            ur = response.xpath("//a[@aria-label='next']/@href").get()
            yield response.follow(url=ur, callback=self.parse)
            
    def data_parser(self, response):
        yield{
            "Blog Title":response.xpath("//h1/text()").get(),
            "Blog Categories":response.xpath("//div[@class='categories mb-2']/a/text()").get(),
            "Blog Contain": response.xpath("(//p[@dir='ltr'])[1]/text()").get()
        }
    
