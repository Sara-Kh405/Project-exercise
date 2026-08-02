
from playwright.sync_api import sync_playwright
import pandas as pd

pw = sync_playwright().start()

browser = pw.chromium.launch(
        executable_path="C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
        headless=False,
        #slow_mo=2000
        )
page = browser.new_page()
page.goto("https://arxiv.org/search/")
page.get_by_placeholder('Search term...').fill(
    "neural network"
)

page.get_by_role("button").get_by_text("Search").click()

page.wait_for_load_state("networkidle")
"""
links = page.locator(
    "xpath=//a[contains(@href, 'arxiv.org/pdf')]"
).all()

result = []
for link in links:
    result.append(link.get_attribute("href"))
"""

#results = page.locator("li.arxiv-result").all()

###first way
#*****************************************************

pdf_links = []
for _ in range(3):
    results = page.locator("li.arxiv-result").all()

    for result in results:
        link = result.locator("a[href*='/pdf/']").first
        name = result.locator("p.title.is-5.mathjax").first

        if link.count() > 0 and name.count() > 0:
            pdf_links.append({
                "link" : link.get_attribute("href"),
                "name" : name.text_content().strip()
                })

    print(len(pdf_links))
    page.get_by_role("link", name="Next").first.click()
    page.wait_for_load_state("networkidle")

#******************************************************
###second way
"""
pdf_links = []
base_url = "https://arxiv.org/search/?query=neural+network&searchtype=all&abstracts=show&order=-announced_date_first&size=50"

for page_num in range(5):
    start = page_num * 50
    page.goto(f"{base_url}&start={start}")
    page.wait_for_load_state("networkidle")
    
    results = page.locator("li.arxiv-result").all()
    for result in results:
        link = result.locator("a[href*='/pdf/']").first
        if link.count() > 0:
            pdf_links.append(link.get_attribute("href"))
    
    print(f"page {page_num + 1}:  the links = {len(pdf_links)}")
"""
df = pd.DataFrame(pdf_links)
df.to_csv(path_or_buf=".\\Web_Scraping\\The_links_by_pdf_links.csv", index=False)

browser.close()
