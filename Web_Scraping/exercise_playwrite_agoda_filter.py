from playwright.sync_api import Page, Browser
import time

class Filter:
    
    def __init__(self, page:Page, browser:Browser):
        self.page = page
        self.browser = browser

        #Close advertisement
        try:
            page.get_by_role('button', name="Close").click(timeout=5000)
            time.sleep(1)
        except:
            pass

    def Choose_city(self, city):
        search_input = self.page.locator('#textInput')
        search_input.click()
        search_input.fill(city)
        time.sleep(2)
        self.page.locator('li[data-key="0"]').click()
        time.sleep(1)
    

    def Choose_dates(self, check_in_date, check_out_date):
        self.page.locator(f'span[data-selenium-date="{check_in_date}"]').click()
        time.sleep(1)
        self.page.locator(f'span[data-selenium-date="{check_out_date}"]').click()
        time.sleep(1)

    def Choose_number_of_adults(self, count):
        number_of_adults = self.page.locator('div[data-component="desktop-occ-adult-value"]')  
        button_minus = self.page.locator('button[aria-label="Subtract Adults"]')
    
        while number_of_adults.text_content() != "1":
            button_minus.click()
            time.sleep(0.5)
        
    
        for _ in range(int(count)):
            button_plus = self.page.locator('button[aria-label*="Add Adult"]')
            button_plus.click()
            time.sleep(0.5)

    def Search_click(self):
        click_search = self.page.locator('button[data-element-name="search-button"]')
        click_search.click()

        try:
            self.page.wait_for_selector('li[data-selenium="hotel-item"]', timeout=45000)
            print("Results found!")
            return True
        except Exception as e:
            print(f"No results found! خطا: {e}")
            self.browser.close()
            return False

    #    try:
    #        self.page.wait_for_selector('div[data-element-name="property-card-info"]', timeout=45000)
    #        print("Results found!")
    #        return True
    #    except:
    #        print("No results found!")
    #        self.browser.close()
    #        return False
    #        
    #    time.sleep(3)


    def Stars_box(self, *stars):
        try:
            more_button = self.page.locator('button[data-element-name="filter-more-starratingwithluxury"]')
            if more_button.count() > 0:
                more_button.click()
                time.sleep(2)
        except:
            pass
        
        for star_value in list(stars):
            try:
                star_element = self.page.locator(f'label[data-element-value="{star_value}"]')
                if star_element.count() > 0:
                    star_element.first.click()
                    print(f"Star {star_value} selected")
                    time.sleep(2)
            except Exception as e:
                print(f"Error selecting star {star_value}: {e}")

    def Sort_price(self, sort_box):
        try:
            click_box = self.page.locator('button[data-element-name="search-sort-dropdown"]')
            if click_box.count() > 0:
                click_box.click()
                time.sleep(2)
                click_price_box = self.page.locator(f'li[data-element-index="{sort_box}"]')
                if click_price_box.count() > 0:
                    click_price_box.click()
                    print("Sorted by price")
                    time.sleep(5)
        except Exception as e:
            print(f"Error in sorting: {e}")
        