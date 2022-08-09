import requests 
from bs4 import BeautifulSoup 
import json

def getting_all_the_pages():

    pages = ["http://quotes.toscrape.com/page/1"]
    page_url = "http://quotes.toscrape.com/"
    to_append_pages = True
    while to_append_pages:
        try:
            r = requests.get(page_url)
            soup = BeautifulSoup(r.content, 'html.parser')
            pager = soup.find('nav')
            page = pager.select_one('.next a')['href']
            page_url = "http://quotes.toscrape.com"+page
        except TypeError as e:
            to_append_pages = False
        if page_url not in pages:
            pages.append(page_url)
    return pages
#print(pages)

def getting_quotes_authors_data(pages):
    quotesData = []
    authors = []
    authorsData = []
    tags = []
    quotes = dict()
    for page in pages:
        request_the_url = requests.get(page)
        soup = BeautifulSoup(request_the_url.content, 'html.parser')
    
        rows = soup.select('.quote')
        for i in range(len(rows)):
            quotes_data_dict = dict()
            author_data_dict = dict()
            row = rows[i]
            quotes_data_dict['quote'] = row.select_one('.text').text.strip().encode("ascii", "ignore").decode('utf-8')
            quotes_data_dict['author'] = row.select_one('.author').text.strip()
            tagsText = row.find('meta')['content'].split(",")
            quotes_data_dict['tags'] = tagsText
            tags += tagsText
            author_reference = row.select_one('.quote a')['href']
            author_reference_url = 'http://quotes.toscrape.com/' + author_reference+'/'
            author_request = requests.get(author_reference_url)
            author_soup = BeautifulSoup(author_request.content,'html.parser')
            authors_born_date = author_soup.select_one('.author-born-date').text.strip()
            authors_born_country = author_soup.select_one('.author-born-location').text.strip()
            born = authors_born_date+' '+authors_born_country
            author = row.select_one('.author').text.strip() 
            if author not in authors:
                authors.append(author)
                author_data_dict['name'] = author
                author_data_dict['born'] = born
                author_data_dict['reference'] = author_reference_url
                authorsData.append(author_data_dict)
            quotesData.append(quotes_data_dict)
    quotes['quotes'] = quotesData
    quotes['authors'] = authorsData
    tags = list(set(tags))
    tags.remove('')
    quotes['tags'] = tags
    return quotes
    

def converting_data_json_file(quotes):
    with open('quotes.json', 'w') as f:
     json.dump(quotes, f, indent=4)

    with open('quotes.json', 'r') as f:
        quotes = json.load(f)

def main():
    pages = getting_all_the_pages()
    quotes_dict = getting_quotes_authors_data(pages)
    converting_data_json_file(quotes_dict)
    print(quotes_dict['tags'])
    print(len(quotes_dict['tags']))

main()