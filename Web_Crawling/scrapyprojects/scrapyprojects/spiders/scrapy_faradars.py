"""
 خام صفحه HTML استخراج از 
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapyprojects.items import ScrapyprojectsItem

class FaradarsPythonSpider(CrawlSpider):
    name = "scrapy_faradars"
    start_urls = ["https://faradars.org/how-to-learn/python-programming"]
    rules = [
        Rule(LinkExtractor(allow=(r'courses')), callback='parse_item', follow=False)
    ]

    def parse_item(self, response):
        #print(response.css('p::text').get())
        url = response.url

        item = ScrapyprojectsItem()
        item.url = url
        yield item
        

"""
#*******************************************
#*******************************************
#*******************************************

"""
import scrapy
import json

class FaradarsJsonSpider(scrapy.Spider):
    name = "faradars_json"
    start_urls = ["https://faradars.org/how-to-learn/python-programming"]

    def parse(self, response):
        script = response.css('script#__NEXT_DATA__::text').get()
        if script:
            data = json.loads(script)
            with open("faradars_data.json", "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print("✅ فایل JSON با موفقیت ذخیره شد!")
        else:
            print("❌ تگ __NEXT_DATA__ پیدا نشد!")"""

"""
import scrapy
import json

class FaradarsApiSpider(scrapy.Spider):
    name = "faradars_api"
    start_urls = [
        "https://faradars.org/api/client/v2/landings/632531/products?page=1&limit=20"
    ]

    def parse(self, response):
        data = json.loads(response.text)
        print(json.dumps(data, indent=2, ensure_ascii=False)[:3000])"""

import scrapy
import json
from scrapyprojects.items import ScrapyprojectsItem

class FaradarsApiSpider(scrapy.Spider):
    name = "faradars_api"
    start_urls = [
        "https://faradars.org/api/client/v2/landings/632531/products?page=1&limit=20"
    ]

    def parse(self, response):
        data = json.loads(response.text)
        products = data.get("products", [])

        for product in products:
            instructors = product.get("instructors", [])
            instructor_name = None
            if instructors:
                instructor_name = f"{instructors[0].get('first_name', '')} {instructors[0].get('last_name', '')}".strip()

            item = ScrapyprojectsItem(
                title=product.get("title"),
                url=product.get("url"),
                price=product.get("price"),
                student_count=product.get("student_count"),
                rating=product.get("rating"),
                instructor=instructor_name
            )
            yield item