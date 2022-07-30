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
for page in pages:
    r = requests.get(page)
    soup = BeautifulSoup(r.content, 'html.parser')
    
    rows = soup.select('.quote')
    for i in range(len(rows)):
        d = dict()
        row = rows[i]
        d['quote'] = row.select_one('.text').text.strip()
        d['author'] = row.select_one('.author').text.strip()
        d['tags'] = row.find('meta')['content'].split(",")
        data.append(d)
    sleep(10)
    
quotes = dict()
quotes['quotes'] = data

with open('quotes.json', 'w') as f:
    json.dump(quotes, f)

with open('quotes.json', 'r') as f:
    quotes = json.load(f)
print(quotes)

