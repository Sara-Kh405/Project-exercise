"""import scrapy
import re

def clean_price(price_text):
    digits = re.sub(r"[^\d]", "", price_text)  # فقط ارقام (فارسی یا انگلیسی) رو نگه دار
    return int(digits) if digits else None

class Scrapysite(scrapy.Spider):
    name = 'divar_info'
    min_price = 1_000_000_000
    max_price = 5_000_000_000

    allowed_domains = ["divar.ir"]
    start_urls = [f"https://divar.ir/s/isfahan/car?price={min_price}-{max_price}"]

    def parse(self, response):

        for item in response.css("a.kt-post-card__action"):
            title = item.css("h2.kt-post-card__title::text").get()
            price = item.css("div.kt-post-card__description::text").getall()[1]
            link = response.urljoin(item.css("::attr(href)").get())

            yield {
                "title": title,
                "price_text" : price.strip(),
                "price_value": clean_price(price.strip()),
                "url": link,
            }
"""


import json
import re
import scrapy


def clean_price(price_text):
    """تبدیل متن قیمت (فارسی/انگلیسی، با کاما و 'تومان') به عدد صحیح."""
    if not price_text:
        return None
    digits = re.sub(r"[^\d]", "", price_text)
    return int(digits) if digits else None


class DivarInfo(scrapy.Spider):
    name = "divar_info"
    allowed_domains = ["api.divar.ir"]

    async def start(self):
        payload = self.build_payload()
        yield scrapy.Request(
            url="https://api.divar.ir/v8/postlist/w/search",
            method="POST",
            body=json.dumps(payload),
            headers={"Content-Type": "application/json"},
            callback=self.parse,
        )

    def build_payload(self, pagination_data=None):
        payload = {
            "city_ids": ["4"],
            "disable_recommendation": False,
            "search_data": {
                "form_data": {
                    "data": {
                        "category": {"str": {"value": "light"}},
                        "price": {
                            "number_range": {
                                "minimum": "1000000000",
                                "maximum": "5000000000",
                            }
                        },
                    }
                }
            },
            "source_view": "FILTER",
        }
        if pagination_data:
            payload["pagination_data"] = pagination_data
        return payload

    def parse(self, response):
        data = json.loads(response.text)

        for widget in data.get("list_widgets", []):
            post = widget.get("data", {})
            token = post.get("token")
            price_text = post.get("middle_description_text")

            yield {
                "title": post.get("title"),
                "price_text": price_text,
                "price_value": clean_price(price_text),  # <-- همون تابع قبلی، فقط الان روی فیلد جدید
                "km_text": post.get("top_description_text"),
                "token": token,
                "url": f"https://divar.ir/v/-/{token}" if token else None,
            }

        pagination = data.get("pagination", {})
        if pagination.get("has_next_page"):
            next_payload = self.build_payload(pagination_data=pagination.get("data"))
            yield scrapy.Request(
                url="https://api.divar.ir/v8/postlist/w/search",
                method="POST",
                body=json.dumps(next_payload),
                headers={"Content-Type": "application/json"},
                callback=self.parse,
            )