#This file is going to include method that will parse
#The specific data that we need from each one of the deal boxes


from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
from selenium.webdriver.common.by import By
import time

class BookingReport:
    def __init__(self, driver:WebDriver, boxes_section_element:WebElement):
        self.driver = driver
        self.boxes_section_element = boxes_section_element
        #self.deal_boxes = self.pull_deal_boxes()

    def pull_deal_boxes(self):
        return self.boxes_section_element.find_elements(By.CSS_SELECTOR,
                                                 'li[data-selenium="hotel-item"]'
                                                 )
    
    def pull_deal_box_attributes(self):
        
        last_height = 0
        while True:
            self.driver.execute_script('window.scrollBy(0, 800)')
            time.sleep(1)

            new_height = self.driver.execute_script("return document.body.scrollHeight")
            print(str(new_height) + "-" + str(last_height))

            if new_height == last_height:
                break
            else:
                last_height = new_height

        # حالا که اسکرول تموم شد و کل صفحه لود شده، بریم سراغ استخراج اسم‌ها
        collection = []
        boxes = self.pull_deal_boxes()
        for box in boxes:
            try:
                hotel_name = box.find_element(
                    By.CSS_SELECTOR, 'a[data-selenium="hotel-name"]'
                ).text

            except (StaleElementReferenceException, NoSuchElementException):
                continue

            try:
                hotel_price = box.find_element(
                    By.CSS_SELECTOR, 'span[data-selenium="display-price"]'
                ).text

            except (StaleElementReferenceException, NoSuchElementException):
                hotel_price = "N/A"

            try:
                hotel_score = box.find_element(
                    By.CSS_SELECTOR, 'a[aria-label="Location score"] p span:first-child'
                ).text
                
            except (StaleElementReferenceException, NoSuchElementException):
                hotel_score = "N/A"

            collection.append([hotel_name, hotel_price, hotel_score])

        return collection

        #print(combination)
        