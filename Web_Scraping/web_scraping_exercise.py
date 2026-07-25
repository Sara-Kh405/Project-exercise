#SELENIUM


#from selenium import webdriver
#from selenium.webdriver.chrome.service import Service
#from selenium.webdriver.chrome.options import Options
#
#options = Options()
#options.add_argument("--headless")
##options.add_argument("--no-sandbox")
#
#service = Service(r'chromedriver.exe')
#driver = webdriver.Chrome(service=service)
#url = 'http://www.google.com/'
#driver.get(url)
#print(driver.page_source)
#
#driver.quit()

#HTTP.CLIENT

"""
import http.client
host = "docs.python.org"
conn = http.client.HTTPSConnection(host)
conn.request("GET", "/3/", headers={"Host": host})
response = conn.getresponse()
print(response.status, response.reason)

"""
#REQUESTS

"""
import requests

url = "http://www.google.com/"
try:

    response = requests.get(url)
    print(response.status_code)

except:

    print("I can not found the URL!!")
"""

#from bs4 import BeautifulSoup
#import requests

#url = "https://pypi.org/"
#response = requests.get(url)
#soup = BeautifulSoup(response.text, 'html.parser')
"""
links = soup('a')
for i in links:
    print(i['href'])
"""

"""
links = soup('a', attrs={'class' : 'skip-to-content'})
print(links)

"""
#CHILDREN
"""
div1 = soup('div')
chi = div1[0].children
for i in chi:
    print(i)
"""
#PARENT
"""
div1 = soup('div')
print(div1[0].parent)
"""

#links = soup('a')
#print(links[0].get('class'))

#****************************
#****************************
#****************************

from bs4 import BeautifulSoup
import requests
"""
with open('sample.html') as html_file:
    soup = BeautifulSoup(html_file, 'lxml')
"""
#print(soup.prettify())
#***********************
"""
match1 = soup.title.text
match2 = soup.title.string
print(match1, ' ,', match2)
"""
#*************************
#print(soup.find('div', class_ = 'footer'))

#*************************

#article = soup.find('div', class_ = 'article')
#print(article)

#************************
#headline = article.h2.a.text
#print(headline)
#************************
"""
summary = article.p.text
print(summary)
"""
#************************
"""
for article in soup.find_all('div', class_ = 'article'):
    headline = article.h2.a.text
    print(headline)

    summary = article.p.text
    print(summary)
"""
url = "https://www.python.org/"
response = requests.get(url).text
soup = BeautifulSoup(response, 'lxml')
print(soup.prettify())

title = soup.find('div', class_ = 'slide-copy')
#print(title.h1.text)

link = soup.find('div', class_ = 'medium-widget event-widget last')
result = link.find_all('li')[2]
#print(result.a['href'])