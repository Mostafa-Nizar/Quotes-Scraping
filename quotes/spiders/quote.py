# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest

class QuoteSpider(scrapy.Spider):
    name = 'quote'
    allowed_domains = ['quotes.toscrape.com/js']

    script = '''
    function main(splash, args)
      assert(splash:go(args.url))
      assert(splash:wait(0.5))
      return {
      html = splash:html(),
      png = splash:png(),
      har = splash:har(),
     }
    end

  '''
    def start_requests(self):
        yield SplashRequest(url="http://quotes.toscrape.com/js/",callback=self.parse,endpoint="execute",args={
            'lua_source':self.script
        })




    def parse(self, response):
        for quotes in response.xpath("//div[@class='quote']"):
            yield{
                'text':quotes.xpath(".//span[@class='text']/text()").get(),
                'author':quotes.xpath(".//span/small/text()").get(),
                'tgs':quotes.xpath(".//div[@class='tags']/a/text()").getall()

            }
        