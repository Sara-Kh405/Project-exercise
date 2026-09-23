from playwright.sync_api import sync_playwright
import pandas as pd
import time

def main():
    p = sync_playwright().start()
    browser = p.chromium.launch(
        executable_path="C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
        headless=False,
        slow_mo=300
    )
    page = browser.new_page()
    page.goto("https://www.agoda.com/en-gb/?ds=QUmYTN%2FF9%2FnyYn0k",
            wait_until="domcontentloaded",
            timeout=60000)
    time.sleep(5)
    
    # بستن پنجره تبلیغات
    try:
        break_box = page.get_by_role('button', name="Close").click(timeout=5000)
        time.sleep(1)
    except:
        pass
    
    # جستجوی نیویورک
    search_input = page.locator('#textInput')
    search_input.click()
    search_input.fill("New York")
    time.sleep(2)
    page.locator('li[data-key="0"]').click()
    time.sleep(1)
    
    # انتخاب تاریخ‌ها
    page.locator('span[data-selenium-date="2026-08-19"]').click()
    time.sleep(1)
    page.locator('span[data-selenium-date="2026-09-09"]').click()
    time.sleep(1)
    
    # تنظیم تعداد بزرگسالان
    number_of_adults = page.locator('div[data-component="desktop-occ-adult-value"]')  
    button_minus = page.locator('button[aria-label="Subtract Adults"]')
    
    for _ in range(5):
        if number_of_adults.text_content() != "1":
            button_minus.click()
            time.sleep(0.5)
        else:
            break
    
    for _ in range(4):
        button_plus = page.locator('button[aria-label*="Add Adult"]')
        button_plus.click()
        time.sleep(0.5)
    
    # کلیک روی دکمه جستجو
    click_search = page.locator('button[data-element-name="search-button"]')
    click_search.click()
    
    # صبر برای لود شدن نتایج
    try:
        page.wait_for_selector('div[data-element-name="property-card-info"]', timeout=20000)
        print("نتایج پیدا شد!")
    except:
        print("نتایج پیدا نشد!")
        browser.close()
        return
    
    time.sleep(3)
    
    # =============== فیلتر ستاره ===============
    try:
        more_button = page.locator('button[data-element-name="filter-more-starratingwithluxury"]')
        if more_button.count() > 0:
            more_button.click()
            time.sleep(2)
            print("دکمه More کلیک شد")
    except:
        pass
    
    for star_value in [3, 4]:
        try:
            star_element = page.locator(f'label[data-element-value="{star_value}"]')
            if star_element.count() > 0:
                star_element.first.click()
                print(f"ستاره {star_value} انتخاب شد")
                time.sleep(2)
        except Exception as e:
            print(f"خطا در انتخاب ستاره {star_value}: {e}")
    
    # =============== مرتب‌سازی بر اساس قیمت ===============
    try:
        click_box = page.locator('button[data-element-name="search-sort-dropdown"]')
        if click_box.count() > 0:
            click_box.click()
            time.sleep(2)
            click_price_box = page.locator('li[data-element-index="1"]')
            if click_price_box.count() > 0:
                click_price_box.click()
                print("مرتب‌سازی بر اساس قیمت انجام شد")
                time.sleep(5)
    except Exception as e:
        print(f"خطا در مرتب‌سازی: {e}")
    
    # =============== اسکرول هوشمند با محدودیت ===============
    print("\nشروع اسکرول برای لود هتل‌های بیشتر...")
    time.sleep(3)
    
    all_hotels_data = []
    seen_hotels = set()
    
    MAX_HOTELS = 30
    MAX_SCROLLS = 20
    MAX_NO_NEW = 5
    
    scroll_count = 0
    no_new_hotels_count = 0
    
    while scroll_count < MAX_SCROLLS and no_new_hotels_count < MAX_NO_NEW:
        try:
            page.evaluate("window.scrollBy(0, 600)")
            time.sleep(2)
            
            hotel_elements = page.locator('li[data-selenium="hotel-item"]')


            current_count = hotel_elements.count()
            print(f"تعداد هتل‌های بارگذاری شده: {current_count}")
            
            new_hotels_found = False
            
            for i in range(current_count):
                try:
                    if len(all_hotels_data) >= MAX_HOTELS:
                        print(f"\n✅ به حد کافی هتل ({MAX_HOTELS}) رسیدیم!")
                        break
                    
                    hotel_item = hotel_elements.nth(i)
                    
                    # استخراج نام هتل
                    try:
                        hotel_name = hotel_item.locator('a[data-selenium="hotel-name"]').text_content(timeout=3000)
                        if not hotel_name or hotel_name.strip() == "":
                            continue
                        hotel_name = hotel_name.strip()
                    except:
                        continue
                    
                    if hotel_name in seen_hotels:
                        continue
                    
                    # استخراج قیمت
                    try:
                        hotel_price = hotel_item.locator('span[data-selenium="display-price"]').text_content(timeout=3000)
                        if not hotel_price or hotel_price.strip() == "":
                            hotel_price = "نامشخص"
                        else:
                            hotel_price = hotel_price.strip()
                    except:
                        hotel_price = "نامشخص"
                    
                    # =============== استخراج امتیاز با روش‌های مختلف ===============
                    hotel_score = "نامشخص"
                    
                    # روش 1: استفاده از aria-label که در کد اولیه شما کار میکرد
                    try:
                        # این همان روشی است که در کد اولیه شما بود
                        score_element = hotel_item.locator('a[aria-label="Location score"] p span:first-child')
                        if score_element.count() > 0:
                            hotel_score = score_element.first.text_content(timeout=3000)
                            if hotel_score and hotel_score.strip():
                                hotel_score = hotel_score.strip()
                    except:
                        pass
                    
                    # روش 2: اگر روش اول جواب نداد، از selectorهای جایگزین استفاده کن
                    if hotel_score == "نامشخص":
                        try:
                            # پیدا کردن هر المانی که شبیه امتیاز باشد
                            selectors = [
                                'a[aria-label*="score"] p span:first-child',
                                'a[aria-label*="Score"] p span:first-child',
                                '[data-element-name="review-score"] span',
                                '.ReviewScore span:first-child',
                                'span[data-element-name="review-score"]',
                                'div[data-element-name="review-score"] span'
                            ]
                            
                            for selector in selectors:
                                score_element = hotel_item.locator(selector)
                                if score_element.count() > 0:
                                    temp_score = score_element.first.text_content(timeout=3000)
                                    if temp_score and temp_score.strip():
                                        hotel_score = temp_score.strip()
                                        break
                        except:
                            pass
                    
                    # روش 3: جستجوی کلی در المنت برای پیدا کردن عدد با ممیز (مثل 8.7)
                    if hotel_score == "نامشخص":

                        try:
                            # تمام متن‌های داخل هتل را بگیر
                            all_text = hotel_item.text_content(timeout=3000)
                            if all_text:
                                # دنبال الگوی عدد با ممیز بگرد (مثل 8.7, 9.2, و غیره)
                                import re
                                # الگوی عدد با ممیز بین 0 تا 10
                                match = re.search(r'(\d+\.\d+)', all_text)
                                if match:
                                    score = match.group(1)
                                    # اگر عدد بین 0 تا 10 بود، احتمالا امتیاز است
                                    if 0 <= float(score) <= 10:
                                        hotel_score = score
                        except:
                            pass
                    
                    all_hotels_data.append([hotel_name, hotel_price, hotel_score])
                    seen_hotels.add(hotel_name)
                    new_hotels_found = True
                    print(f"✅ هتل {len(all_hotels_data)}: {hotel_name} - قیمت: {hotel_price} - امتیاز: {hotel_score}")
                    
                except Exception as e:
                    if "closed" in str(e).lower():
                        print("صفحه بسته شد، خروج از حلقه...")
                        break
                    continue
            
            if len(all_hotels_data) >= MAX_HOTELS:
                break
            
            if not new_hotels_found:
                no_new_hotels_count += 1
                print(f"⚠️ هتل جدیدی پیدا نشد. تلاش {no_new_hotels_count} از {MAX_NO_NEW}")
            else:
                no_new_hotels_count = 0
            
            scroll_count += 1
            
        except Exception as e:
            if "closed" in str(e).lower():
                print("صفحه بسته شد، خروج از حلقه...")
                break
            print(f"خطا در اسکرول: {e}")
            break
    
    print(f"\n📊 جمع کل هتل‌های استخراج شده: {len(all_hotels_data)}")
    
    # =============== ذخیره در فایل CSV ===============
    if all_hotels_data:
        try:
            df = pd.DataFrame(all_hotels_data, columns=['Hotel Name', 'Hotel Price', 'Hotel Score'])
            df.to_csv('hotel_results.csv', index=False, encoding='utf-8-sig')
            print(f"\n✅ فایل CSV ذخیره شد با {len(all_hotels_data)} هتل")
            
            print("\n📋 نمونه هتل‌های استخراج شده:")
            print(df.head(10))
            
            print(f"\n📊 آمار:")
            print(f"تعداد کل هتل‌ها: {len(df)}")
            print(f"تعداد هتل‌های دارای قیمت: {df[df['Hotel Price'] != 'نامشخص'].shape[0]}")
            print(f"تعداد هتل‌های دارای امتیاز: {df[df['Hotel Score'] != 'نامشخص'].shape[0]}")
            
            # نمایش هتل‌های دارای امتیاز
            if df[df['Hotel Score'] != 'نامشخص'].shape[0] > 0:
                print("\n⭐ هتل‌های دارای امتیاز:")
                print(df[df['Hotel Score'] != 'نامشخص'][['Hotel Name', 'Hotel Score']].head(10))
            
        except Exception as e:
            print(f"❌ خطا در ذخیره فایل: {e}")
    else:
        print("❌ هیچ هتلی استخراج نشد!")
    
    try:
        page.screenshot(path='debug_screenshot.png')
        print("\n📸 اسکرین‌شات ذخیره شد: debug_screenshot.png")
    except:
        print("⚠️ امکان ذخیره اسکرین‌شات وجود ندارد")
    
    print("\n⏳ در حال بستن مرورگر...")
    time.sleep(2)
    browser.close()
    p.stop()
    print("✅ پایان برنامه")

if __name__ == "__main__":
    main()