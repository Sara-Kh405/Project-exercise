from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import time

with sync_playwright() as p:
    browser = p.chromium.launch(
        executable_path="C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
        headless=False,
        slow_mo=50
    )
    page = browser.new_page()
    page.goto("https://sess.sku.ac.ir/Sess/12321840132")
    page.fill("#edId", "*******")
    page.fill("#edPass", "*******")
    page.click("#edEnter")
    time.sleep(5)
    html = page.inner_html(".col-lg-10 ")
    #print(html)
    soup = BeautifulSoup(html, "lxml")
    #print(soup.find_all("div", class_="col-lg-2 col-xs-6"))
    #print(soup.find_all("h1")[2].text)
    page.get_by_text("سایر امور").click()