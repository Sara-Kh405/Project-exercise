"""
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time

service = Service(r'chromedriver.exe')

driver = webdriver.Chrome(service=service)

url = "https://auth.digikala.com/realms/dk-group/protocol/openid-connect/auth?client_id=digikala-web-public&redirect_uri=https%3A%2F%2Fwww.digikala.com%2Fsso-redirect%2F%3Fback-url%3D%252F&state=66d9233b-a607-40a5-984a-1da2ef0e4fcd&response_mode=fragment&response_type=code&scope=openid&nonce=925922d0-73bd-4788-b9f0-87b87bb749ac&code_challenge=U_IdP95IqkiUKysEsOvAJtoVGrasGs1OPcypT4zJnHQ&code_challenge_method=S256"
driver.get(url)
user_name_field = driver.find_element(By.NAME, "username")
user_name_field.clear()
user_name_field.send_keys("09913893486")
login_botton = driver.find_element(By.ID, "dk-login")
login_botton.click()

time.sleep(5)
driver.quit()
"""

