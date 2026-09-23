"""
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class ScrapyprojectsPipeline:
    def process_item(self, item):
        return item
    
"""

import os
import sqlite3
from datetime import datetime, timezone

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "divar_prices.db")


class SQLitePipeline:
    def open_spider(self, spider):
        self.conn = sqlite3.connect(DB_PATH)   # <-- اینجا فرق کرد
        self.cur = self.conn.cursor()
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS price_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                token TEXT,
                title TEXT,
                price_text TEXT,
                price_value INTEGER,
                km_text TEXT,
                url TEXT,
                scraped_at TEXT
            )
        """)
        self.conn.commit()

    def close_spider(self, spider):
        self.conn.close()

    def process_item(self, item, spider):
        self.cur.execute(
            """INSERT INTO price_history
               (token, title, price_text, price_value, km_text, url, scraped_at)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (
                item.get("token"),
                item.get("title"),
                item.get("price_text"),
                item.get("price_value"),
                item.get("km_text"),
                item.get("url"),
                datetime.now(timezone.utc).isoformat(),
            ),
        )
        self.conn.commit()
        return item