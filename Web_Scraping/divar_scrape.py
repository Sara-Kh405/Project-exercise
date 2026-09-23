from camoufox.sync_api import Camoufox
import pandas as pd

def loading_page(page):
    page.wait_for_load_state('networkidle')
    page.wait_for_timeout(5000)


with Camoufox() as browser:
    page = browser.new_page()
    page.goto("https://divar.ir/s/isfahan/auto")
    loading_page(page)

    page.get_by_placeholder("جستجو در خودرو").click()
    page.keyboard.type("تویوتا")
    page.keyboard.press('Enter')
    loading_page(page)

    page.locator('input#price-minimum').click()
    page.keyboard.type('1_000_000_000')
    page.locator('input#price-maximum').click()
    page.keyboard.type('5_000_000_000')
    page.keyboard.press('Enter')
    loading_page(page)

    ls = []
    seen_texts = set()

    results = page.locator('div.widget-col-d2306').all()
    print("count of results are : ", len(results))
    for item in results:
        text = item.inner_text()
        if text not in seen_texts:
            seen_texts.add(text)
            ls.append(text)
        #print(item.inner_text())
        #print('-'*30)

    #scrolling
    
    for _ in range(5):  # مثلا ۵ بار اسکرول کن
        page.evaluate("window.scrollBy(0, document.body.scrollHeight)")
        loading_page(page)

        items = page.locator('div.widget-col-d2306').all()  # هر بار دوباره می‌گیریم
        for item in items:
            text = item.inner_text()
            if text not in seen_texts:
                seen_texts.add(text)
                ls.append(text)
                #print(text)
                #print('-'*30)

    #page.evaluate("window.scrollBy(0, document.body.scrollHeight)")
    #loading_page(page)

df = pd.DataFrame(ls, columns=["results"])
df.to_csv('results_of_divar.csv', index=False, encoding='utf-8-sig')

