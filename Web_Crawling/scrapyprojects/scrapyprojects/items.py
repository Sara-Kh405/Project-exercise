# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from dataclasses import dataclass


@dataclass
class ScrapyprojectsItem:
    # define the fields for your item here like:
    # name: str | None = None
    title: str | None = None
    url: str | None = None
    price: int | None = None
    student_count: int | None = None
    rating: float | None = None
    instructor: str | None = None
