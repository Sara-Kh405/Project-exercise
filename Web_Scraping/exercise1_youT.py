import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://www.python.org/"

response = requests.get(url).text

soup = BeautifulSoup(response, 'lxml')
count = 0
result = []

divs = soup.find_all('div', class_ = 'shrubbery')
for div in divs:
    lis = div.find_all('li')
    
    for li in lis:
        if count < 10:
            text = li.a.text.strip()
            link = li.a['href'].strip()
            result.append([count, text, link])
            print(f'{count} - text : {text}\nlink : {link}')
            count += 1


            print('Every element printed!!')
        

df = pd.DataFrame(result, columns=['id', 'text', 'link'])
df.to_csv('cms_scrapers.csv', index=False)


