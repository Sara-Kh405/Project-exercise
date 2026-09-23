from playwright.sync_api import sync_playwright
import pandas as pd
import time


with sync_playwright() as pw:
    browser = pw.chromium.launch(
        executable_path="C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
        headless=False,
        #slow_mo=2000
        )
    page = browser.new_page()
    page.goto("https://jobvision.ir/", wait_until="domcontentloaded", timeout=60000)
    time.sleep(8)

    #جهت بستن تبلیغ
    #try:
    #    page.frame_locator("iframe").locator("button#deny").click(timeout=5000)
    #except Exception as e:
    #    print(e)
    
    page.get_by_placeholder("عنوان شغلی یا شرکت …").click()
    page.keyboard.type("مهندسی کشاورزی")
    page.wait_for_timeout(1000)
    
    page.get_by_placeholder("شهر").click()
    page.keyboard.type("تهران")
    page.wait_for_timeout(1000)

    page.get_by_text("تمامی شهرهای تهران", exact=True).first.click()

    page.get_by_text(" جستجو در مشاغل ", exact=True).click()
    time.sleep(5)
    
    ls = []
    for i in range(1, 3):
        page.locator("a.page-link").get_by_text(f"{i}").click()
        time.sleep(5)
        results = page.locator("job-card.jvt-w-full.jvt-flex.jvt-flex-wrap.jvt-cursor-pointer.ng-star-inserted").all()
        for item in results:
            text = item.inner_text()
            lines = [line.strip() for line in text.split("\n") if line.strip()]
            link = item.locator("a.desktop-job-card").get_attribute("href")
            if link and link.startswith("/"):
                link = "https://jobvision.ir" + link
            ls.append({"lines": lines, "link": link})
            print(text)
            print(link)
            print("-" * 30)

df = pd.DataFrame(ls)
#df.to_csv("result_of_jobvision.csv", index=False, encoding="utf-8-sig")
df.to_json("result_of_jobvision.json", orient="records", force_ascii=False, indent=2)
