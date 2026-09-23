import requests
from bs4 import BeautifulSoup

url = "https://news.ycombinator.com/"

response = requests.get(url)

soup = BeautifulSoup(response.text, 'lxml')

part_title = soup.find_all('span', class_='titleline')

count = 1
for part in part_title:
    print(f"{count} - The text is : {part.text}\nThe link is : {part.find('a')['href']}")
    count += 1