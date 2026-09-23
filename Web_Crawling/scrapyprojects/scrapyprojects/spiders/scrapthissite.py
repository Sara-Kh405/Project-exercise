import scrapy

class Scrapspider(scrapy.Spider):
    name = "example"
    start_urls = ["https://www.python.org/"]

    def parse(self, response):
        #for item in response.css("div.page"):
        #    yield{
        #        "title" : item.css("h3.page-title a::text").get(),
        #        "text" : item.css("p.lead.session-desc::text").get()
        #    }
#*********************************************************************
#*********************************************************************


        #print(response.css('title')) ----> selector
        #print(response.css('title').extract())
        #print(response.css('title::text').extract())
        #print(response.css('title::text').extract()[0])


#*********************************************************************
#*********************************************************************

        #print(response.css('span.tag-wrapper>.tag::text').extract())

        #general = response.css('span.tag-wrapper')
        #print(general.css('a.tag::text').getall())

        #print(response.css('a.tag::text').getall())

#*********************************************************************
#*********************************************************************

        #print(response.css('#content > div > section > div:nth-child(3) > div.medium-widget.applications-widget.last > div > ul > li:nth-child(1) > b::text').get())

#*********************************************************************
#*********************************************************************

        #print(response.xpath('//title/text()').get())
        #print(response.xpath('//a/text()').getall())
        ##print(response.xpath('//nav[@id="mainnav"]//ul[@class="navigation menu"]/li/a/text()').getall())
        print(response.xpath('//div[@id="success-story-930"]//a/text()').getall())

