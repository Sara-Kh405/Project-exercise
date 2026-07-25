#This file will include a class with instance method.
# That will be responsaible to intract our website
# After we have some results, to apply filterations
 
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
class BookingFiltration:
    def __init__(self, driver:WebDriver):
        self.driver = driver

    def apply_star_rating(self, *star_values):
        self.driver.find_element(By.ID, 'filter-menu-StarRatingWithLuxury')
        star_child_elements = self.driver.find_elements(By.CSS_SELECTOR, 'label[data-component="search-filter-starratingwithluxury"]')
        #print(len(star_child_elements))
        time.sleep(2)
     
        for star_value in star_values:
            for star_element in star_child_elements:
                val = star_element.get_attribute('data-element-value')
                if val == str(star_value) :
                    star_element.click()
        time.sleep(2)          

    def sort_price_lowest_first(self, index):
        
        click_box = self.driver.find_element(By.CSS_SELECTOR, 'button[data-element-name="search-sort-dropdown"]')
        click_box.click()
        click_price_box = self.driver.find_element(By.CSS_SELECTOR, f'li[data-element-index="{index}"]')
        click_price_box.click()
          