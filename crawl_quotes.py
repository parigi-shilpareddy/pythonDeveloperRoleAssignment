import requests 
from time import sleep
from bs4 import BeautifulSoup 
import json

pages = [
    'http://quotes.toscrape.com/page/1/',
    'http://quotes.toscrape.com/page/2/',
    'http://quotes.toscrape.com/page/3/',
    'http://quotes.toscrape.com/page/4/',
    'http://quotes.toscrape.com/page/5/',
    'http://quotes.toscrape.com/page/6/',
    'http://quotes.toscrape.com/page/7/',
    'http://quotes.toscrape.com/page/8/',
    'http://quotes.toscrape.com/page/9/',
    'http://quotes.toscrape.com/page/10/'
]


data = []
authorsData = []
for page in pages:
    r = requests.get(page)
    soup = BeautifulSoup(r.content, 'html.parser')
    
    rows = soup.select('.quote')
    for i in range(len(rows)):
        d = dict()
        a = dict()
        row = rows[i]
        d['quote'] = row.select_one('.text').text.strip()
        d['author'] = row.select_one('.author').text.strip()
        d['tags'] = row.find('meta')['content'].split(",")
        quotes_page = row.select_one('.quote a')['href']
        quotes_page = 'http://quotes.toscrape.com/' + quotes_page+'/'
        author_request = requests.get(quotes_page)
        author_soup = BeautifulSoup(author_request.content,'html.parser')
        authors_born_date = author_soup.select_one('.author-born-date').text.strip()
        authors_born_country = author_soup.select_one('.author-born-location').text.strip()
        born = authors_born_date+' '+authors_born_country
        a['name'] = row.select_one('.author').text.strip() 
        a['born'] = born
        a['reference'] = quotes_page
        data.append(d)
        authorsData.append(a)
    sleep(10)
    
quotes = dict()
quotes['quotes'] = data
quotes['authors'] = list(set(authorsData))

with open('quotes.json', 'w') as f:
    json.dump(quotes, f)

with open('quotes.json', 'r') as f:
    quotes = json.load(f)

