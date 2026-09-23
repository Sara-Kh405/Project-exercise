"""
اجرا:
    python price_alert.py
"""

import os
import sqlite3

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "divar_prices.db")


def get_price_drops():
    """
    برای هر token، دو آخرین رکورد (بر اساس scraped_at) رو می‌گیره
    و اگه قیمت دومی (جدیدتر) کمتر از اولی (قدیمی‌تر) بود، گزارشش می‌کنه.
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    # برای هر token، همه‌ی رکوردهاش رو مرتب‌شده بر اساس زمان می‌گیریم
    cur.execute("""
        SELECT token, title, price_value, scraped_at, url
        FROM price_history
        WHERE price_value IS NOT NULL
        ORDER BY token, scraped_at ASC
    """)
    rows = cur.fetchall()
    conn.close()

    # گروه‌بندی رکوردها بر اساس token
    history_by_token = {}
    for row in rows:
        history_by_token.setdefault(row["token"], []).append(row)

    drops = []
    for token, records in history_by_token.items():
        if len(records) < 2:
            continue  # هنوز فقط یک‌بار دیده شده، چیزی برای مقایسه نیست

        previous = records[-2]
        latest = records[-1]

        if latest["price_value"] < previous["price_value"]:
            drops.append({
                "token": token,
                "title": latest["title"],
                "old_price": previous["price_value"],
                "new_price": latest["price_value"],
                "drop_amount": previous["price_value"] - latest["price_value"],
                "url": latest["url"],
            })

    return drops


if __name__ == "__main__":
    drops = get_price_drops()

    if not drops:
        print("هیچ افت قیمتی پیدا نشد.")
    else:
        print(f"{len(drops)} مورد افت قیمت پیدا شد:\n")
        for d in drops:
            print(f"🔻 {d['title']}")
            print(f"   قیمت قبلی : {d['old_price']:,} تومان")
            print(f"   قیمت جدید : {d['new_price']:,} تومان")
            print(f"   میزان افت: {d['drop_amount']:,} تومان")
            print(f"   لینک: {d['url']}")
            print()