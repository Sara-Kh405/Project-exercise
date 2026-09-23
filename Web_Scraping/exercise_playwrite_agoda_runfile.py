
#star_child_elements = page.locator('label[data-component="search-filter-starratingwithluxury"]').all()
from playwright.sync_api import sync_playwright
import time
from exercise_playwrite_agoda_filter import Filter
from exercise_playwrite_agoda_scroll import Scroll



with sync_playwright() as p:
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

    hotel_filter = Filter(page, browser)
    hotel_filter.Choose_city(input("What is your city: "))
    hotel_filter.Choose_dates(
        check_in_date = input("Enter check_in : "),
        check_out_date = input("Enter check_out : ")
    )
    hotel_filter.Choose_number_of_adults(input("How many adults : "))
    hotel_filter.Search_click()
    stars_input = input("How many stars ? ")
    hotel_filter.Stars_box(*list(stars_input))
    hotel_filter.Sort_price(input("Enter sort_box : "))

    scroll = Scroll(page)
    scroll.select_name_price_score()
    
    


