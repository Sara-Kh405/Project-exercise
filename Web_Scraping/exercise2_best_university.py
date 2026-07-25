from bs4 import BeautifulSoup
import requests

url = 'https://demoqa.com/progress-bar'
response = requests.get(url)
soup = BeautifulSoup(response, 'lxml')
part1 = soup.find('section', class_ = 'news-container headlines')
print(soup.prettify())