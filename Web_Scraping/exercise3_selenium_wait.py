from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.common.keys import Keys


service = Service(r'chromedriver.exe')
driver = webdriver.Chrome(service=service)
"""
url = 'https://demoqa.com/progress-bar'
driver.get(url)
driver.implicitly_wait(30)  #time.sleep(30)
botton = driver.find_element(By.ID, 'startStopButton')
botton.click()
print(botton.text == 'Reset')

WebDriverWait(driver, 30).until(
    EC.text_to_be_present_in_element(
        (By.ID, 'resetButton'),# Element filteration
        'Progress Bar'          # The expected text
    )
)
print("Done!")
driver.quit()
#print(botton.text == 'Reset')

"""
url = 'https://demoqa.com/progress-bar'
driver.get(url)
driver.implicitly_wait(30)  #time.sleep(30)
botton = driver.find_element(By.ID, 'startStopButton')
botton.click()
print(botton.text == 'Reset')

wait = WebDriverWait(driver, 30)
wait.until(lambda d:d.find_element(By.CLASS_NAME, 'progress-bar').get_attribute('aria-valuenow') == '100')

print("Done!")

element1 = driver.find_element(By.CLASS_NAME, 'header-right')
element1.click()

element2 = driver.find_element(By.CLASS_NAME, 'text')
element2.click()

username = driver.find_element(By.ID, 'userName')
username.send_keys("SaraKh")

useremail = driver.find_element(By.ID, 'userEmail')
useremail.send_keys('SaraKH138@email.com')

submit = driver.find_element(By.ID, 'submit')
submit.send_keys(Keys.ENTER)

show = driver.find_element(By.ID, 'output')

print(show.text)
driver.quit()


