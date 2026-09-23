
from selenium import webdriver
from selenium.webdriver.chrome.service import Service 
from selenium.webdriver.common.by import By 
from booking.booking_filteration import BookingFiltration
from booking.booking_report import BookingReport
import pandas as pd
import time
from booking.constants import BASE_URL, PATH_DRIVER


class Booking(webdriver.Chrome):       
    def __init__(self, driver_path = PATH_DRIVER, teardown=False):
        self.teardown = teardown #بستن مرورگر
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])  #ندیدن warning
        service = Service(driver_path)
        super().__init__(service=service)
        self.implicitly_wait(15)
        self.maximize_window()
    

    def __exit__(self, exc_type, exc, traceback):
        if self.teardown:
            self.quit()
    
    def land_first_page(self):
        self.get(BASE_URL)
        time.sleep(5)

    def change_currency(self, currency):

        if currency == "USD":
            print("USD is default!")
            return True

        currency_element = self.find_element(
            By.CSS_SELECTOR, 'div[data-element-name="currency-container-selected-currency"]')

        currency_element.click()
        time.sleep(2)
        

        selected_currency_element = self.find_element(
            By.CSS_SELECTOR, f'div[data-value="{currency}"]'
        )
        
        selected_currency_element.click()


    def choose_city(self, ans):

        target = self.find_element(By.ID, 'textInput')
        target.click()
        target.clear()
        time.sleep(2)
        target.send_keys(ans)
        target_final = self.find_element(By.CSS_SELECTOR, 'li[data-key="0"]')
        time.sleep(1)
        target_final.click()
        

    def select_dates(self, check_in_date, check_out_date):
        check_in_element = self.find_element(By.CSS_SELECTOR, f'span[data-selenium-date="{check_in_date}"]')
        check_in_element.click()

        check_out_element = self.find_element(By.CSS_SELECTOR, f'span[data-selenium-date="{check_out_date}"]')
        check_out_element.click()


    def select_adults(self, count):

        number_of_adults = self.find_element(By.CSS_SELECTOR, 'div[data-component="desktop-occ-adult-value"]')  
        button_minus = self.find_element(By.CSS_SELECTOR, 'button[aria-label="Subtract Adults"]')

        while number_of_adults.text != "1":
            button_minus.click()
            
        for _ in range(count - 1):
            button_plus = self.find_element(By.CSS_SELECTOR, 'button[aria-label*="Add Adult"]')
            button_plus.click()

    def search_button(self):
        click_search = self.find_element(By.CSS_SELECTOR, 'button[data-element-name="search-button"]')
        click_search.click()

    def apply_filterations(self):
        filteration = BookingFiltration(driver=self)
        filteration.apply_star_rating(3)
        filteration.sort_price_lowest_first(1)

    def report_results(self):
        hotel_list = self.find_element(By.CSS_SELECTOR, 'ol[class="hotel-list-container"]')
        report = BookingReport(self, hotel_list)
        titles = report.pull_deal_box_attributes()
        print(titles)

        df = pd.DataFrame(titles, columns=['Hotel Name', 'Hotel Price', 'Hotel Score'])
        df.to_csv('hotel_results.csv', index=False)
        print("فایل اکسل ذخیره شد: hotel_results.csv")


